"""
This module provides utility functions shared by tests.
"""

import itertools
import os
import os.path
import pathlib

from typing import (
	Iterable,  # Replaced by `collections.abc.Iterable` in 3.9.
	List,  # Replaced by `set` in 3.9.
	Set,  # Replaced by `set` in 3.9.
	Tuple,  # Replaced by `tuple` in 3.9.
	cast)

from pathspec import (
	PathSpec,
	RegexPattern)
from pathspec.util import (
	CheckResult,
	TStrPath)


def debug_results(spec: PathSpec, results: Iterable[CheckResult[str]]) -> str:
	"""
	Format the check results message.

	*spec* (:class:`~pathspec.PathSpec`) is the path-spec.

	*results* (:class:`~collections.abc.Iterable` or :class:`~pathspec.util.CheckResult`)
	yields each file check result.

	Returns the message (:class:`str`).
	"""
	patterns = cast(List[RegexPattern], spec.patterns)

	pattern_table = []
	for index, pattern in enumerate(patterns, 1):
		pattern_table.append((f"{index}:{pattern.pattern}", repr(pattern.regex.pattern)))

	result_table = []
	for result in results:
		if result.index is not None:
			pattern = patterns[result.index]
			result_table.append((f"{result.index + 1}:{pattern.pattern}", result.file))
		else:
			result_table.append(("-", result.file))

	result_table.sort(key=lambda r: r[1])

	first_max_len = max((
		len(__row[0]) for __row in itertools.chain(pattern_table, result_table)
	), default=0)
	first_width = min(first_max_len, 20)

	pattern_lines = []
	for row in pattern_table:
		pattern_lines.append(f" {row[0]:<{first_width}}  {row[1]}")

	result_lines = []
	for row in result_table:
		result_lines.append(f" {row[0]:<{first_width}}  {row[1]}")

	return "\n".join([
		"\n",
		" DEBUG ".center(32, "-"),
		*pattern_lines,
		"-"*32,
		*result_lines,
		"-"*32,
	])


def get_includes(results: Iterable[CheckResult[TStrPath]]) -> Set[TStrPath]:
	"""
	Get the included files from the check results.

	*results* (:class:`~collections.abc.Iterable` or :class:`~pathspec.util.CheckResult`)
	yields each file check result.

	Returns the included files (:class:`set` of :class:`str`).
	"""
	return {__res.file for __res in results if __res.include}


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
