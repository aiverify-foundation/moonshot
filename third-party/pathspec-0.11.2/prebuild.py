"""
This script generates files required for source and wheel distributions,
and legacy installations.
"""

import argparse
import configparser
import sys

import tomli


def generate_readme_dist() -> None:
	"""
	Generate the "README-dist.rst" file from "README.rst" and
	"CHANGES.rst".
	"""
	print("Read: README.rst")
	with open("README.rst", 'r', encoding='utf8') as fh:
		output = fh.read()

	print("Read: CHANGES.rst")
	with open("CHANGES.rst", 'r', encoding='utf8') as fh:
		output += "\n\n"
		output += fh.read()

	print("Write: README-dist.rst")
	with open("README-dist.rst", 'w', encoding='utf8') as fh:
		fh.write(output)


def generate_setup_cfg() -> None:
	"""
	Generate the "setup.cfg" file from "pyproject.toml" in order to
	support legacy installation with "setup.py".
	"""
	print("Read: pyproject.toml")
	with open("pyproject.toml", 'rb') as fh:
		config = tomli.load(fh)

	print("Write: setup.cfg")
	output = configparser.ConfigParser()
	output['metadata'] = {
		'author': config['project']['authors'][0]['name'],
		'author_email': config['project']['authors'][0]['email'],
		'classifiers': "\n" + "\n".join(config['project']['classifiers']),
		'description': config['project']['description'],
		'license': config['project']['license']['text'],
		'long_description': f"file: {config['project']['readme']}",
		'long_description_content_type': "text/x-rst",
		'name': config['project']['name'],
		'url': config['project']['urls']['Source Code'],
		'version': "attr: pathspec._meta.__version__",
	}
	output['options'] = {
		'packages': "find:",
		'python_requires': config['project']['requires-python'],
		'setup_requires': "setuptools>=40.8.0",
		'test_suite': "tests",
	}
	output['options.packages.find'] = {
		'include': "pathspec, pathspec.*",
	}

	with open("setup.cfg", 'w', encoding='utf8') as fh:
		output.write(fh)


def main() -> int:
	"""
	Run the script.
	"""
	# Parse command-line arguments.
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args(sys.argv[1:])

	generate_readme_dist()
	generate_setup_cfg()

	return 0


if __name__ == '__main__':
	sys.exit(main())
