from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()
setup(
    name='FreeTAKServer',
    packages=find_packages(include = ['FreeTAKServer', 'FreeTAKServer.*']),
    version='1.9',
    license='Eclipse License',
    description='An open source server for the TAK family of applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='FreeTAKTeam',
    author_email='your.email@domain.com',
    url='https://github.com/FreeTAKTeam/FreeTakServer',
    download_url='https://github.com/Tapawingo/FreeTakServer/archive/v0.8.4-Beta.tar.gz',
    keywords=['TAK', 'OPENSOURCE'],
    install_requires=[
        'flask==1.1.2',
        'lxml==4.6.1',
        'pathlib==1.0.1',
        'tabulate==0.8.7',
        'sqlalchemy==1.3.20',
        'setuptools',
        'Flask_SQLAlchemy==2.4.4',
        'flask-cors==3.0.9',
        'flask-socketio==4.3.1',
        'eventlet==0.29.0',
        'flask_httpauth==4.2.0',
        'protobuf==3.14.0',
        'python-socketio==4.6.0',
        'python-engineio==3.13.2',
        'Jinja2==2.11.2',
        'psutil',
        'PyYAML',
        'defusedxml',
        'geopy',
        'ruamel.yaml',
        'pykml'
    ],
    extras_require = {'ui': ['FreeTAKServer_UI']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
