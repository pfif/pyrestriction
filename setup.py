from setuptools import setup

setup(
    name = "PyRestriction",
    description = "Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.",
    version = "1.0",
    author = "Pfif Zehirman",
    url = "https://github.com/pfif/pyrestriction/",
    packages = ["pyrestriction"],
    entry_points = {
        'console_scripts': [
            'pyrestriction = pyrestriction.parser:parse'
        ]
    },
    test_suite = "tests"
)

