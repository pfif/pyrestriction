from setuptools import setup

setup(
    name = "PyRestriction",
    description = "Tell it the amounts that you owe or want to save, and it will compute how much money is avaliable to you.",
    version = "1.1.1",
    author = "Pfif Zehirman",
    url = "https://github.com/pfif/pyrestriction/",
    packages = ["pyrestriction"],
    entry_points = {
        'console_scripts': [
            'pyrestriction = pyrestriction.entrypoint:entrypoint'
        ]
    },
    test_suite = "tests"
)

