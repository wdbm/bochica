#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "bochica",
        version          = "2017.01.31.0155",
        description      = "GNU Privacy Guard encryption-decryption graphical user interface",
        long_description = long_description(),
        url              = "https://github.com/wdbm/bochica",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "bochica"
                           ],
        install_requires = [
                           "docopt",
                           "propyte",
                           "shijian"
                           ],
        scripts          = [
                           "bochica.py"
                           ],
        entry_points     = """
            [console_scripts]
            bochica = bochica:bochica
        """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
