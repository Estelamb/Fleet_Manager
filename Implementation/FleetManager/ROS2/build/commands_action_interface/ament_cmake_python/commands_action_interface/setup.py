from setuptools import find_packages
from setuptools import setup

setup(
    name='commands_action_interface',
    version='0.0.0',
    packages=find_packages(
        include=('commands_action_interface', 'commands_action_interface.*')),
)
