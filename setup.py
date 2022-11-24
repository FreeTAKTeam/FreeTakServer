import glob
from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()
setup(
    name="FreeTAKServer",
    packages=find_packages(
        include=["FreeTAKServer", "FreeTAKServer.*", "*.json", "*.ini", "*.conf"]
    ),
    version='1.9.10.6',
    license="EPL-2.0",
    description="An open source server for the TAK family of applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FreeTAKTeam",
    author_email="FreeTakTeam@gmail.com",
    url="https://github.com/FreeTAKTeam/FreeTakServer",
    download_url="https://github.com/FreeTAKTeam/FreeTakServer/releases",
    keywords=["TAK", "OPENSOURCE"],
    include_package_data=True,
    install_requires=[
        'click==8.0.4',
        'colorama==0.4.4',
        'cryptography==36.0.2',
        'bcrypt==3.1.7',
        'defusedxml==0.7.1',
        'dnspython==2.2.1',
        'eventlet==0.33.1',
        'Flask==1.1.2',
        'Flask-Cors==3.0.9',
        'Flask-HTTPAuth==4.2.0',
        'Flask-Login==0.5.0',
        'Flask-SocketIO==4.3.1',
        'Flask-SQLAlchemy==2.4.4',
        'geographiclib==1.52',
        'geopy==2.2.0',
        'greenlet==2.0.0',
        'itsdangerous==2.0.1',
        'testresources==2.0.1',
        'Jinja2==2.11.2',
        'lxml==4.9.1',
        'MarkupSafe==2.0.1',
        'monotonic==1.6',
        'pathlib2==2.3.7.post1',
        'protobuf==3.14.0',
        'psutil==5.9.0',
        'pykml==0.2.0',
        'python-engineio==3.13.2',
        'python-socketio==4.6.0',
        'PyYAML==6.0',
        'ruamel.yaml==0.17.21',
        'ruamel.yaml.clib==0.2.7',
        'six==1.16.0',
        'SQLAlchemy==1.3.20',
        'tabulate==0.8.7',
        'Werkzeug==2.0.3',
        'WTForms==2.3.3',
        'pyOpenSSL==22.0.0',
        'qrcode==7.3.1',
        'pillow==9.1.1',
        'asyncio==3.4.3',
        'xmltodict',
        'pyzmq',
        'digitalpy'
    ],
    extras_require = {
        'ui': [
            'FreeTAKServer_UI'
        ],
        'dev': [
            'pytak==5.4.1',
            'pytest==7.2.0',
            'pytest-asyncio==0.20.1'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Programming Language :: Python :: 3.8",
    ],
)
