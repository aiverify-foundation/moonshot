"""
This module provides utility functions shared by tests.
"""

import os
import os.path
import pathlib

from typing import (
	Iterable,
	Tuple)


def make_dirs(temp_dir: pathlib.Path, dirs: Iterable[str]) -> None:
	"""
	Create the specified directories.

	*temp_dir* (:class:`pathlib.Path`) is the temporary directory to use.

	*dirs* (:class:`Iterable` of :class:`str`) is the POSIX directory
	paths (relative to *temp_dir*) to create.
	"""
	for dir in dirs:
		os.mkdir(temp_dir / ospath(dir))


def make_files(temp_dir: pathlib.Path, files: Iterable[str]) -> None:
	"""
	Create the specified files.

	*temp_dir* (:class:`pathlib.Path`) is the temporary directory to use.

	*files* (:class:`Iterable` of :class:`str`) is the POSIX file paths
	(relative to *temp_dir*) to create.
	"""
	for file in files:
		mkfile(temp_dir / ospath(file))


def make_links(temp_dir: pathlib.Path, links: Iterable[Tuple[str, str]]) -> None:
	"""
	Create the specified links.

	*temp_dir* (:class:`pathlib.Path`) is the temporary directory to use.

	*links* (:class:`Iterable` of :class:`tuple`) contains the POSIX links
	to create relative to *temp_dir*. Each link (:class:`tuple`) contains
	the destination link path (:class:`str`) and source node path
	(:class:`str`).
	"""
	for link, node in links:
		src = temp_dir / ospath(node)
		dest = temp_dir / ospath(link)
		os.symlink(src, dest)


def mkfile(file: pathlib.Path) -> None:
	"""
	Creates an empty file.

	*file* (:class:`pathlib.Path`) is the native file path to create.
	"""
	with open(file, 'wb'):
		pass


def ospath(path: str) -> str:
	"""
	Convert the POSIX path to a native OS path.

	*path* (:class:`str`) is the POSIX path.

	Returns the native path (:class:`str`).
	"""
	return os.path.join(*path.split('/'))
