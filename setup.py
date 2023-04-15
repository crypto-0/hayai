from setuptools import setup
from setuptools import find_packages

setup(
        name = "hayai",
        version = "1.0.0",
        description = "This is an application to download movies or shows from  streaming websites",
        author = "crypto",
        license = "MIT Licence",
        url = "https://github.com/crypto-0/hayai",
        install_requires = ["PyQt5==5.15.9","providers @ git+https://github.com/crypto-0/providers.git"],
        packages = find_packages(exclude=[]),
)
