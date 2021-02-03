from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.8.20'
repo = "FreeTakServer/FreeTakServer"

setup(
    name='FreeTAKServer',         # How you named your package folder (MyLib)
    packages=[
        'FreeTAKServer',
        'FreeTAKServer.controllers',
        'FreeTAKServer.controllers.configuration',
        'FreeTAKServer.controllers.model'
    ],   # Chose the same as "name"
    version=version,
    license='MIT',
    description='An open source server for the TAK family of applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ghosty 1008',
    author_email='your.email@domain.com',
    url=f"https://github.com/{ repo }",
    download_url=f"https://github.com/{ repo }/archive/v{ version }.tar.gz",
    keywords=[
        'TAK',
        'OPENSOURCE'
    ],
    install_requires=[
        'flask',
        'lxml',
        'pyopenssl'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
