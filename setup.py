from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in asc/__init__.py
from asc import __version__ as version

setup(
	name="asc",
	version=version,
	description="ASC",
	author="Micromerger",
	author_email="m.haroon@pk.micromerger.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
