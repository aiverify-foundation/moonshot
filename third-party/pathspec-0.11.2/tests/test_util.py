"""
This script tests utility functions.
"""

import errno
import os
import os.path
import pathlib
import shutil
import tempfile
import unittest
from functools import (
	partial)
from typing import (
	Iterable,
	Tuple)

from pathspec.patterns.gitwildmatch import (
	GitWildMatchPattern)
from pathspec.util import (
	RecursionError,
	iter_tree_entries,
	iter_tree_files,
	match_file,
	normalize_file)
from tests.util import (
	make_dirs,
	make_files,
	make_links,
	mkfile,
	ospath)


class MatchFileTest(unittest.TestCase):
	"""
	The :class:`MatchFileTest` class tests the :meth:`.match_file`
	function.
	"""

	def test_1_match_file(self):
		"""
		Test matching files individually.
		"""
		patterns = list(map(GitWildMatchPattern, [
			'*.txt',
			'!b.txt',
		]))
		results = set(filter(partial(match_file, patterns), [
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		]))
		self.assertEqual(results, {
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		})


class IterTreeTest(unittest.TestCase):
	"""
	The :class:`IterTreeTest` class tests :meth:`.iter_tree_entries` and
	:meth:`.iter_tree_files` functions.
	"""

	def make_dirs(self, dirs: Iterable[str]) -> None:
		"""
		Create the specified directories.
		"""
		make_dirs(self.temp_dir, dirs)

	def make_files(self, files: Iterable[str]) -> None:
		"""
		Create the specified files.
		"""
		make_files(self.temp_dir, files)

	def make_links(self, links: Iterable[Tuple[str, str]]) -> None:
		"""
		Create the specified links.
		"""
		make_links(self.temp_dir, links)

	def require_realpath(self) -> None:
		"""
		Skips the test if `os.path.realpath` does not properly support
		symlinks.
		"""
		if self.broken_realpath:
			raise unittest.SkipTest("`os.path.realpath` is broken.")

	def require_symlink(self) -> None:
		"""
		Skips the test if `os.symlink` is not supported.
		"""
		if self.no_symlink:
			raise unittest.SkipTest("`os.symlink` is not supported.")

	def setUp(self) -> None:
		"""
		Called before each test.
		"""
		self.temp_dir = pathlib.Path(tempfile.mkdtemp())

	def tearDown(self) -> None:
		"""
		Called after each test.
		"""
		shutil.rmtree(self.temp_dir)

	def test_1_files(self):
		"""
		Tests to make sure all files are found.
		"""
		self.make_dirs([
			'Empty',
			'Dir',
			'Dir/Inner',
		])
		self.make_files([
			'a',
			'b',
			'Dir/c',
			'Dir/d',
			'Dir/Inner/e',
			'Dir/Inner/f',
		])
		results = set(iter_tree_files(self.temp_dir))
		self.assertEqual(results, set(map(ospath, [
			'a',
			'b',
			'Dir/c',
			'Dir/d',
			'Dir/Inner/e',
			'Dir/Inner/f',
		])))

	def test_2_0_check_symlink(self):
		"""
		Tests whether links can be created.
		"""
		# NOTE: Windows Vista and greater supports `os.symlink` for Python
		# 3.2+.
		no_symlink = None
		try:
			file = self.temp_dir / 'file'
			link = self.temp_dir / 'link'
			mkfile(file)

			try:
				os.symlink(file, link)
			except (AttributeError, NotImplementedError, OSError):
				no_symlink = True
			else:
				no_symlink = False

		finally:
			self.__class__.no_symlink = no_symlink

	def test_2_1_check_realpath(self):
		"""
		Tests whether `os.path.realpath` works properly with symlinks.
		"""
		# NOTE: Windows does not follow symlinks with `os.path.realpath`
		# which is what we use to detect recursion. See <https://bugs.python.org/issue9949>
		# for details.
		broken_realpath = None
		try:
			self.require_symlink()
			file = self.temp_dir / 'file'
			link = self.temp_dir / 'link'
			mkfile(file)
			os.symlink(file, link)

			try:
				self.assertEqual(os.path.realpath(file), os.path.realpath(link))
			except AssertionError:
				broken_realpath = True
			else:
				broken_realpath = False

		finally:
			self.__class__.broken_realpath = broken_realpath

	def test_2_2_links(self):
		"""
		Tests to make sure links to directories and files work.
		"""
		self.require_symlink()
		self.make_dirs([
			'Dir',
		])
		self.make_files([
			'a',
			'b',
			'Dir/c',
			'Dir/d',
		])
		self.make_links([
			('ax', 'a'),
			('bx', 'b'),
			('Dir/cx', 'Dir/c'),
			('Dir/dx', 'Dir/d'),
			('DirX', 'Dir'),
		])
		results = set(iter_tree_files(self.temp_dir))
		self.assertEqual(results, set(map(ospath, [
			'a',
			'ax',
			'b',
			'bx',
			'Dir/c',
			'Dir/cx',
			'Dir/d',
			'Dir/dx',
			'DirX/c',
			'DirX/cx',
			'DirX/d',
			'DirX/dx',
		])))

	def test_2_3_sideways_links(self):
		"""
		Tests to make sure the same directory can be encountered multiple
		times via links.
		"""
		self.require_symlink()
		self.make_dirs([
			'Dir',
			'Dir/Target',
		])
		self.make_files([
			'Dir/Target/file',
		])
		self.make_links([
			('Ax', 'Dir'),
			('Bx', 'Dir'),
			('Cx', 'Dir/Target'),
			('Dx', 'Dir/Target'),
			('Dir/Ex', 'Dir/Target'),
			('Dir/Fx', 'Dir/Target'),
		])
		results = set(iter_tree_files(self.temp_dir))
		self.assertEqual(results, set(map(ospath, [
			'Ax/Ex/file',
			'Ax/Fx/file',
			'Ax/Target/file',
			'Bx/Ex/file',
			'Bx/Fx/file',
			'Bx/Target/file',
			'Cx/file',
			'Dx/file',
			'Dir/Ex/file',
			'Dir/Fx/file',
			'Dir/Target/file',
		])))

	def test_2_4_recursive_links(self):
		"""
		Tests detection of recursive links.
		"""
		self.require_symlink()
		self.require_realpath()
		self.make_dirs([
			'Dir',
		])
		self.make_files([
			'Dir/file',
		])
		self.make_links([
			('Dir/Self', 'Dir'),
		])
		with self.assertRaises(RecursionError) as context:
			set(iter_tree_files(self.temp_dir))

		self.assertEqual(context.exception.first_path, 'Dir')
		self.assertEqual(context.exception.second_path, ospath('Dir/Self'))

	def test_2_5_recursive_circular_links(self):
		"""
		Tests detection of recursion through circular links.
		"""
		self.require_symlink()
		self.require_realpath()
		self.make_dirs([
			'A',
			'B',
			'C',
		])
		self.make_files([
			'A/d',
			'B/e',
			'C/f',
		])
		self.make_links([
			('A/Bx', 'B'),
			('B/Cx', 'C'),
			('C/Ax', 'A'),
		])
		with self.assertRaises(RecursionError) as context:
			set(iter_tree_files(self.temp_dir))

		self.assertIn(context.exception.first_path, ('A', 'B', 'C'))
		self.assertEqual(context.exception.second_path, {
			'A': ospath('A/Bx/Cx/Ax'),
			'B': ospath('B/Cx/Ax/Bx'),
			'C': ospath('C/Ax/Bx/Cx'),
		}[context.exception.first_path])

	def test_2_6_detect_broken_links(self):
		"""
		Tests that broken links are detected.
		"""
		def reraise(e):
			raise e

		self.require_symlink()
		self.make_links([
			('A', 'DOES_NOT_EXIST'),
		])
		with self.assertRaises(OSError) as context:
			set(iter_tree_files(self.temp_dir, on_error=reraise))

		self.assertEqual(context.exception.errno, errno.ENOENT)

	def test_2_7_ignore_broken_links(self):
		"""
		Tests that broken links are ignored.
		"""
		self.require_symlink()
		self.make_links([
			('A', 'DOES_NOT_EXIST'),
		])
		results = set(iter_tree_files(self.temp_dir))
		self.assertEqual(results, set())

	def test_2_8_no_follow_links(self):
		"""
		Tests to make sure directory links can be ignored.
		"""
		self.require_symlink()
		self.make_dirs([
			'Dir',
		])
		self.make_files([
			'A',
			'B',
			'Dir/C',
			'Dir/D',
		])
		self.make_links([
			('Ax', 'A'),
			('Bx', 'B'),
			('Dir/Cx', 'Dir/C'),
			('Dir/Dx', 'Dir/D'),
			('DirX', 'Dir'),
		])
		results = set(iter_tree_files(self.temp_dir, follow_links=False))
		self.assertEqual(results, set(map(ospath, [
			'A',
			'Ax',
			'B',
			'Bx',
			'Dir/C',
			'Dir/Cx',
			'Dir/D',
			'Dir/Dx',
			'DirX',
		])))

	def test_3_entries(self):
		"""
		Tests to make sure all files are found.
		"""
		self.make_dirs([
			'Empty',
			'Dir',
			'Dir/Inner',
		])
		self.make_files([
			'a',
			'b',
			'Dir/c',
			'Dir/d',
			'Dir/Inner/e',
			'Dir/Inner/f',
		])
		results = {entry.path for entry in iter_tree_entries(self.temp_dir)}
		self.assertEqual(results, set(map(ospath, [
			'a',
			'b',
			'Dir',
			'Dir/c',
			'Dir/d',
			'Dir/Inner',
			'Dir/Inner/e',
			'Dir/Inner/f',
			'Empty',
		])))

	def test_4_normalizing_pathlib_path(self):
		"""
		Tests normalizing a :class:`pathlib.PurePath` as argument.
		"""
		first_spec = normalize_file(pathlib.PurePath('a.txt'))
		second_spec = normalize_file('a.txt')
		self.assertEqual(first_spec, second_spec)
