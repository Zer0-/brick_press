from setuptools import setup

requires = [
    'bricks',
    'scss',
    'csscompressor',
    'CoffeeScript',
]

links = [
    'git+https://github.com/Zer0-/bricks.git#egg=bricks',
]

setup(
    name='brick_press',
    version='0.0',
    description='Static Asset Builder',
    author='Philipp Volguine',
    author_email='phil.volguine@gmail.com',
    packages=['src'],
    include_package_data=True,
    install_requires=requires,
    dependency_links=links,
)
