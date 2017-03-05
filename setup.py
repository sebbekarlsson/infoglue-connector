from distutils.core import setup
import setuptools


setup(
        name='infoglueConnector',
        version='0.1',
        install_requires=[
            'requests',
            'watchdog',
            'bs4'
            ],
        packages=[
            'infogluelocal'
            ],
        entry_points={
            "console_scripts": [
                "infogluewatch = infogluelocal.infoglue_dog.__main__:watch",
                "infoglueget = infogluelocal.infoglue_dog.__main__:get"
                ]
            }
        )
