from setuptools import setup

setup(
    # Application name:
    name = "egs",

    # Version number:
    version = "0.1.0",

    # Application author details:
    author = "Brahm Lower",
    author_email = "bplower@gmail.com",

    # License
    license = "",

    # Packages:
    py_modules = ["egs"],

    # Dependant packages:
    install_requires = [
        "aiohttp",
        "python-socketio"
    ]
)