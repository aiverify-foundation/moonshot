"""
This script tests :class:`.PathSpec`.
"""

import os
import os.path
import pathlib
import shutil
import tempfile
import unittest
from typing import (
	Iterable)

from pathspec import (
	PathSpec)
from pathspec.util import (
	iter_tree_entries)
from pathspec.patterns.gitwildmatch import GitWildMatchPatternError
from tests.util import (
	make_dirs,
	make_files,
	ospath)


class PathSpecTest(unittest.TestCase):
	"""
	The :class:`PathSpecTest` class tests the :class:`.PathSpec` class.
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
		return make_files(self.temp_dir, files)

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

	def test_01_absolute_dir_paths_1(self):
		"""
		Tests that absolute paths will be properly normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'foo',
		])
		results = set(spec.match_files([
			'/a.py',
			'/foo/a.py',
			'/x/a.py',
			'/x/foo/a.py',
			'a.py',
			'foo/a.py',
			'x/a.py',
			'x/foo/a.py',
		]))
		self.assertEqual(results, {
			'/foo/a.py',
			'/x/foo/a.py',
			'foo/a.py',
			'x/foo/a.py',
		})

	def test_01_absolute_dir_paths_2(self):
		"""
		Tests that absolute paths will be properly normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'/foo',
		])
		results = set(spec.match_files([
			'/a.py',
			'/foo/a.py',
			'/x/a.py',
			'/x/foo/a.py',
			'a.py',
			'foo/a.py',
			'x/a.py',
			'x/foo/a.py',
		]))
		self.assertEqual(results, {
			'/foo/a.py',
			'foo/a.py',
		})

	def test_01_current_dir_paths(self):
		"""
		Tests that paths referencing the current directory will be properly
		normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		results = set(spec.match_files([
			'./src/test1/a.txt',
			'./src/test1/b.txt',
			'./src/test1/c/c.txt',
			'./src/test2/a.txt',
			'./src/test2/b.txt',
			'./src/test2/c/c.txt',
		]))
		self.assertEqual(results, {
			'./src/test2/a.txt',
			'./src/test2/b.txt',
			'./src/test2/c/c.txt',
		})

	def test_01_empty_path(self):
		"""
		Tests that patterns that end with an escaped space will be treated properly.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'\\ ',
			'abc\\ '
		])
		test_files = [
			' ',
			'  ',
			'abc ',
			'somefile',
		]
		results = list(filter(spec.match_file, test_files))
		self.assertEqual(results, [
			' ',
			'abc '
		])

		# An escape with double spaces is invalid.
		# Disallow it. Better to be safe than sorry.
		self.assertRaises(GitWildMatchPatternError, lambda: PathSpec.from_lines('gitwildmatch', [
			'\\  '
		]))

	def test_01_match_files(self):
		"""
		Tests that matching files one at a time yields the same results as
		matching multiples files at once.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		test_files = [
			'src/test1/a.txt',
			'src/test1/b.txt',
			'src/test1/c/c.txt',
			'src/test2/a.txt',
			'src/test2/b.txt',
			'src/test2/c/c.txt',
		]
		single_results = set(filter(spec.match_file, test_files))
		multi_results = set(spec.match_files(test_files))
		self.assertEqual(single_results, multi_results)

	def test_01_windows_current_dir_paths(self):
		"""
		Tests that paths referencing the current directory will be properly
		normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		results = set(spec.match_files([
			'.\\src\\test1\\a.txt',
			'.\\src\\test1\\b.txt',
			'.\\src\\test1\\c\\c.txt',
			'.\\src\\test2\\a.txt',
			'.\\src\\test2\\b.txt',
			'.\\src\\test2\\c\\c.txt',
		], separators=('\\',)))
		self.assertEqual(results, {
			'.\\src\\test2\\a.txt',
			'.\\src\\test2\\b.txt',
			'.\\src\\test2\\c\\c.txt',
		})

	def test_01_windows_paths(self):
		"""
		Tests that Windows paths will be properly normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		results = set(spec.match_files([
			'src\\test1\\a.txt',
			'src\\test1\\b.txt',
			'src\\test1\\c\\c.txt',
			'src\\test2\\a.txt',
			'src\\test2\\b.txt',
			'src\\test2\\c\\c.txt',
		], separators=('\\',)))
		self.assertEqual(results, {
			'src\\test2\\a.txt',
			'src\\test2\\b.txt',
			'src\\test2\\c\\c.txt',
		})

	def test_02_eq(self):
		"""
		Tests equality.
		"""
		first_spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		second_spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		self.assertEqual(first_spec, second_spec)

	def test_02_ne(self):
		"""
		Tests inequality.
		"""
		first_spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
		])
		second_spec = PathSpec.from_lines('gitwildmatch', [
			'!*.txt',
		])
		self.assertNotEqual(first_spec, second_spec)

	def test_03_add(self):
		"""
		Test spec addition using :data:`+` operator.
		"""
		first_spec = PathSpec.from_lines('gitwildmatch', [
			'test.txt',
			'test.png'
		])
		second_spec = PathSpec.from_lines('gitwildmatch', [
			'test.html',
			'test.jpg'
		])
		combined_spec = first_spec + second_spec
		results = set(combined_spec.match_files([
			'test.txt',
			'test.png',
			'test.html',
			'test.jpg'
		]))
		self.assertEqual(results, {
			'test.txt',
			'test.png',
			'test.html',
			'test.jpg'
		})

	def test_03_iadd(self):
		"""
		Test spec addition using :data:`+=` operator.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'test.txt',
			'test.png'
		])
		spec += PathSpec.from_lines('gitwildmatch', [
			'test.html',
			'test.jpg'
		])
		results = set(spec.match_files([
			'test.txt',
			'test.png',
			'test.html',
			'test.jpg'
		]))
		self.assertEqual(results, {
			'test.txt',
			'test.png',
			'test.html',
			'test.jpg'
		})

	def test_04_len(self):
		"""
		Test spec length.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'foo',
			'bar',
		])
		self.assertEqual(len(spec), 2)

	def test_05_match_entries(self):
		"""
		Test matching files collectively.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!b.txt',
		])
		self.make_dirs([
			'X',
			'X/Z',
			'Y',
			'Y/Z',
		])
		self.make_files([
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		])
		entries = iter_tree_entries(self.temp_dir)
		results = {
			__entry.path
			for __entry in spec.match_entries(entries)
		}
		self.assertEqual(results, set(map(ospath, [
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		])))

	def test_05_match_file(self):
		"""
		Test matching files individually.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!b.txt',
		])
		results = set(filter(spec.match_file, [
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

	def test_05_match_files(self):
		"""
		Test matching files collectively.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!b.txt',
		])
		results = set(spec.match_files([
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

	def test_05_match_tree_entries(self):
		"""
		Test matching a file tree.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!b.txt',
		])
		self.make_dirs([
			'X',
			'X/Z',
			'Y',
			'Y/Z',
		])
		self.make_files([
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		])
		results = {
			__entry.path
			for __entry in spec.match_tree_entries(self.temp_dir)
		}
		self.assertEqual(results, set(map(ospath, [
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		])))

	def test_05_match_tree_files(self):
		"""
		Test matching a file tree.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!b.txt',
		])
		self.make_dirs([
			'X',
			'X/Z',
			'Y',
			'Y/Z',
		])
		self.make_files([
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		])
		results = set(spec.match_tree_files(self.temp_dir))
		self.assertEqual(results, set(map(ospath, [
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		])))

	def test_06_issue_41_a(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario A.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.yaml',
			'!*.yaml/',
		])
		files = {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/file.yaml',
			'dir/index.txt',
			'file.yaml',
		}
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			#'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir/file.yaml',
			'file.yaml',
		})
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		})

	def test_06_issue_41_b(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario B.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'!*.yaml/',
			'*.yaml',
		])
		files = {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/file.yaml',
			'dir/index.txt',
			'file.yaml',
		}
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',
			'dir.yaml/index.txt',
			'dir/file.yaml',
			'file.yaml',
		})
		self.assertEqual(files - ignores, {
			'dir/file.sql',
			'dir/index.txt',
		})

	def test_06_issue_41_c(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario C.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.yaml',
			'!dir.yaml',
		])
		files = {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/file.yaml',
			'dir/index.txt',
			'file.yaml',
		}
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			#'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir/file.yaml',
			'file.yaml',
		})
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		})

	def test_07_issue_62(self):
		"""
		Test including all files and excluding a directory.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*',
			'!product_dir/',
		])
		results = set(spec.match_files([
			'anydir/file.txt',
			'product_dir/file.txt'
		]))
		self.assertEqual(results, {
			'anydir/file.txt',
		})

	def test_08_issue_39(self):
		"""
		Test excluding files in a directory.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.log',
			'!important/*.log',
			'trace.*',
		])
		files = {
			'a.log',
			'b.txt',
			'important/d.log',
			'important/e.txt',
			'trace.c',
		}
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'a.log',
			'trace.c',
		})
		self.assertEqual(files - ignores, {
			'b.txt',
			'important/d.log',
			'important/e.txt',
		})

	def test_09_issue_80_a(self):
		"""
		Test negating patterns.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'build',
			'*.log',
			'.*',
			'!.gitignore',
		])
		files = {
			'.c-tmp',
			'.gitignore',
			'a.log',
			'b.txt',
			'build/d.log',
			'build/trace.bin',
			'trace.c',
		}
		keeps = set(spec.match_files(files, negate=True))
		self.assertEqual(keeps, {
			'.gitignore',
			'b.txt',
			'trace.c',
		})

	def test_09_issue_80_b(self):
		"""
		Test negating patterns.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'build',
			'*.log',
			'.*',
			'!.gitignore',
		])
		files = {
			'.c-tmp',
			'.gitignore',
			'a.log',
			'b.txt',
			'build/d.log',
			'build/trace.bin',
			'trace.c',
		}
		keeps = set(spec.match_files(files, negate=True))
		ignores = set(spec.match_files(files))
		self.assertEqual(files - ignores, keeps)
		self.assertEqual(files - keeps, ignores)
