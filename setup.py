from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")



import re, ast

# get version from __version__ variable in erpnext/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('cloud/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


		
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
