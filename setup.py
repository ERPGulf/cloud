from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cloud/__init__.py
from cloud import __version__ as version

setup(
	name="cloud",
	version=version,
	description="cloud",
	author="cloud",
	author_email="deepak@htsqatar",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
