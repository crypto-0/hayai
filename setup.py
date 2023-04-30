from setuptools import setup
from setuptools import find_packages

setup(
        name = "hayai",
        version = "1.0.0",
        description = "This is an application to stream movies or shows from  streaming websites",
        author = "crypto",
        license = "MIT Licence",
        url = "https://github.com/crypto-0/hayai",
        install_requires = ["PyQt6==6.5.0","pycryptodomex==3.17","lxml==4.9.2","setuptools==67.6.1","cssselect"],
        packages = find_packages(exclude=[]),
)
