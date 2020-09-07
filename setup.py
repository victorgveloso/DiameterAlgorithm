from setuptools import setup, find_packages

setup(
    name='DiameterAlgorithm',
    version='1.0.0',
    packages=find_packages(include=['diameter', 'diameter.*']),
    package_dir={'': 'src'},
    url='',
    license='BSD-3-Clause',
    author='Victor Guerra Veloso',
    author_email='victorgvbh@gmail.com',
    description='',
    install_requires=[]
)
