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
    version="0.2.1.0",
    license="EPL-2.0",
    description="An open source server for the TAK family of applications.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="FreeTAKTeam",
    author_email="FreeTakTeam@gmail.com",
    url="https://github.com/FreeTAKTeam/FreeTakServer",
    download_url="https://github.com/FreeTAKTeam/FreeTakServer/releases",
    keywords=["TAK", "OPENSOURCE"],
    include_package_data=True,
    install_requires=[
        "bitarray",
        "blinker>=1.6.2",  # Required for flask 2.3.2
        "click==8.1.3",  # Bumping from 8.0.4 for flask 2.3.2
        "colorama==0.4.4",
        "cryptography==36.0.2",
        "bcrypt==3.1.7",
        "defusedxml==0.7.1",
        "dnspython==2.2.1",
        "eventlet==0.33.1",
        "Flask==2.3.2",
        "Flask-Cors==3.0.9",
        "Flask-HTTPAuth==4.8.0",
        "Flask-Login==0.6.3",  # Upgrading from 0.5.0 for flask 2.3.2 and Werkzeug 2.3.3
        "Flask-SocketIO==5.3.6",
        "Flask-SQLAlchemy==3.1.1",  # Upgrading from 2.4.4 for flask 2.3.2
        "geographiclib==1.52",
        "geopy==2.2.0",
        "greenlet==2.0.2",
        "itsdangerous==2.1.2",  # Upgrading from 2.0.1 for flask 2.3.2
        "testresources==2.0.1",
        "Jinja2==3.1.2",  # Upgrading from 2.11.2 for flask 2.3.2
        "lxml",
        "MarkupSafe==2.1.1",  # Upgrading from 2.0.1 for Flask 2.3.2 and Werkzeug 2.3.3
        "monotonic==1.6",
        "pathlib2==2.3.7.post1",
        "protobuf==3.18.3",
        "psutil==5.9.4",
        "pykml==0.2.0",
        "python-engineio==4.8.0",
        "python-socketio==5.10.0",
        "PyYAML==6.0",
        "ruamel.yaml==0.17.21",
        "ruamel.yaml.clib==0.2.7",
        "six==1.16.0",
        "SQLAlchemy==2.0.16",  # Upgrading from 1.3.20 for flask 2.3.2
        "tabulate==0.8.7",
        "Werkzeug==2.3.3",  # Upgrading from 2.0.3 for flask 2.3.2
        "WTForms==2.3.3",
        "pyOpenSSL==22.0.0",
        "qrcode==7.3.1",
        "pillow==9.3.0",
        "asyncio==3.4.3",
        "xmltodict",
        "pyzmq",
        "digitalpy>=0.3.13.2",
        "opentelemetry-sdk",
        "PyJWT"
    ],
    extras_require={
        "ui": ["FreeTAKServer_UI"],
        "dev": ["pytak==5.4.1", "pytest==7.2.0", "pytest-asyncio==0.20.1"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Programming Language :: Python :: 3.8",
    ],
)
