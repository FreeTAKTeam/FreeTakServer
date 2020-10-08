from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FreeTAKServer',
    packages=find_packages(include = ['FreeTAKServer', 'FreeTAKServer.*']),
    version='1.1',
    license='MIT',
    description='An open source server for the TAK family of applications.',

    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ghosty 1008',
    author_email='your.email@domain.com',
    url='https://github.com/Tapawingo/FreeTakServer',
    download_url='https://github.com/Tapawingo/FreeTakServer/archive/v0.8.4-Beta.tar.gz',
    keywords=['TAK', 'OPENSOURCE'],
    install_requires=[
        'flask',
        'lxml',
        'pathlib',
        'tabulate',
        'sqlalchemy',
        'setuptools',
        'Flask_SQLAlchemy'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)