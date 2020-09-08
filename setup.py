try:
    from setuptools import setup, find_packages
    pkgs=find_packages(include=['diameter', 'diameter.*'])
except ImportError:
    from distutils.core import setup
    pkgs=['diameter','diameter.model','diameter.algorithms']


setup(
    name='DiameterAlgorithm',
    version='1.0.0',
    packages=pkgs,
    package_dir={'': 'src'},
    url='',
    license='BSD-3-Clause',
    author='Victor Guerra Veloso',
    author_email='victorgvbh@gmail.com',
    description='',
    install_requires=[]
)
