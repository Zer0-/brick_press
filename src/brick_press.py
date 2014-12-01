import os
import random
from enum import Enum
from base64 import urlsafe_b64encode
import sass
import coffeescript

def file_extension(filepath):
    return os.path.splitext(os.path.basename(filepath))[1:]

def concatenate(*strings):
    return ''.join(strings)

def urlsafe_bytestring(n):
    randint = lambda: random.randint(0, 255)
    bytestring = bytes([randint() for i in range(n)])
    return urlsafe_b64encode(bytestring)

def gen_filename(size):
    return urlsafe_bytestring(3*size).decode('ascii')

class StaticType(Enum):
    css = 1
    js = 2

class CompilerMplex(dict):
    def __init__(self):
        dict.__init__(self)

    def compile(self, filepath):
        with open(filepath, 'r') as f:
            source = f.read()
        return self[file_extension(filepath)].compile(source)

class StaticCompiler:
    depends_on = [BuilderMplex]
    build_file_extensions = ()
    target_type = Enum.css
    
    def __init__(self, mplex):
        for ext in self.build_file_extensions:
            mplex[ext] = self.target_type

    def compile(self, source_string):
        raise NotImplementedError()

class SassCompiler(StaticCompiler):
    build_file_extensions = ('scss',)

    def compile(self, source_string):
        return sass.compile_string(source_string)

class CoffeescriptCompiler(StaticCompiler):
    build_file_extensions = ('coffee',)

    def compile(self, source_string):
        return coffeescript.compile(source_string)

class GroupBuilder:
    requires_configured = ['json_settings']
    depends_on = [CompilerMplex]

    def __init__(self, settings, mplex):
        self.served_static_dir = settings['served_static_dir']
        self.static_url = settings['served_static_url']
        self.mplex = mplex

    def build_group(self, file_list):
        built_sources = []
        for f in file_list:
            with open(f, 'r') as sf:
                built_sources.append(self.mplex.compile(sf.read()))
        extension = self.mplex[file_extension(file_list[0])]
        filename = gen_filename(6) + '.' extension
        with open(filename, 'w') as out:
            out.write(concatenate(built_sources))
        return filename

    def build_groups(self, group_list):
        groups = [g.split() for g in group_list.split('\n\n')]
        return [self.build_group(g) for g in groups]
