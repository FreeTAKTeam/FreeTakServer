from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = "1.5.10"

setup(
    name="FreeTAKServer",  # How you named your package folder (MyLib)
    packages=[
        "FreeTAKServer",
        "FreeTAKServer.controllers",
        "FreeTAKServer.controllers.configuration",
        "FreeTAKServer.model",
    ],  # Chose the same as "name"
    version=version,  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="An open source server for the TAK family of applications.",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brother Corvo",  # Type in your name
    author_email="your.email@domain.com",  # Type in your E-Mail
    url="https://github.com/Tapawingo/FreeTakServer",  # Provide either the link to your github or to your website
    download_url=f"https://github.com/FreeTAKTeam/FreeTakServer/archive/{ version }.tar.gz",  # I explain this later on
    keywords=["TAK", "OPENSOURCE"],  # Keywords that define your package best
    install_requires=[
        "eventlet",
        "flask",
        "flask_cors",
        "flask_httpauth",
        "flask_login",
        "flask_sqlalchemy",
        "flask_socketio",
        "google",
        "lxml",
        "protobuf",
        "sqlalchemy"    
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.8",
    ],
)