from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in quickfix/__init__.py
from quickfix import __version__ as version

setup(
	name="quickfix",
	version=version,
	description="for quick fix",
	author="hiba",
	author_email="hiba@claudion.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
