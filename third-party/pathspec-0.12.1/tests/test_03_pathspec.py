"""
This script tests :class:`.PathSpec`.
"""

import pathlib
import shutil
import tempfile
import unittest
from typing import (
	Iterable)

from pathspec import (
	PathSpec)
from pathspec.patterns.gitwildmatch import (
	GitWildMatchPatternError)
from pathspec.util import (
	iter_tree_entries)

from .util import (
	CheckResult,
	debug_results,
	get_includes,
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
		files = {
			'/a.py',
			'/foo/a.py',
			'/x/a.py',
			'/x/foo/a.py',
			'a.py',
			'foo/a.py',
			'x/a.py',
			'x/foo/a.py',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'/foo/a.py',
			'/x/foo/a.py',
			'foo/a.py',
			'x/foo/a.py',
		}, debug)

	def test_01_absolute_dir_paths_2(self):
		"""
		Tests that absolute paths will be properly normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'/foo',
		])
		files = {
			'/a.py',
			'/foo/a.py',
			'/x/a.py',
			'/x/foo/a.py',
			'a.py',
			'foo/a.py',
			'x/a.py',
			'x/foo/a.py',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'/foo/a.py',
			'foo/a.py',
		}, debug)

	def test_01_check_file_1_include(self):
		"""
		Test checking a single file that is included.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		result = spec.check_file("include.txt")

		self.assertEqual(result, CheckResult("include.txt", True, 0))

	def test_01_check_file_2_exclude(self):
		"""
		Test checking a single file that is excluded.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		result = spec.check_file("test/exclude.txt")

		self.assertEqual(result, CheckResult("test/exclude.txt", False, 1))

	def test_01_check_file_3_unmatch(self):
		"""
		Test checking a single file that is unmatched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		result = spec.check_file("unmatch.bin")

		self.assertEqual(result, CheckResult("unmatch.bin", None, None))

	def test_01_check_file_4_many(self):
		"""
		Test that checking files one at a time yields the same results as checking
		multiples files at once.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		files = {
			'test1/a.txt',
			'test1/b.txt',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/b.txt',
			'test2/c/c.txt',
		}

		single_results = set(map(spec.check_file, files))
		multi_results = set(spec.check_files(files))

		self.assertEqual(single_results, multi_results)

	def test_01_check_match_files(self):
		"""
		Test that checking files and matching files yield the same results.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/**',
		])
		files = {
			'src/test1/a.txt',
			'src/test1/b.txt',
			'src/test1/c/c.txt',
			'src/test2/a.txt',
			'src/test2/b.txt',
			'src/test2/c/c.txt',
		}

		check_results = set(spec.check_files(files))
		check_includes = get_includes(check_results)
		match_files = set(spec.match_files(files))

		self.assertEqual(check_includes, match_files)

	def test_01_current_dir_paths(self):
		"""
		Tests that paths referencing the current directory will be properly
		normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		files = {
			'./src/test1/a.txt',
			'./src/test1/b.txt',
			'./src/test1/c/c.txt',
			'./src/test2/a.txt',
			'./src/test2/b.txt',
			'./src/test2/c/c.txt',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'./src/test2/a.txt',
			'./src/test2/b.txt',
			'./src/test2/c/c.txt',
		}, debug)

	def test_01_empty_path_1(self):
		"""
		Tests that patterns that end with an escaped space will be treated properly.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'\\ ',
			'abc\\ '
		])
		files = {
			' ',
			'  ',
			'abc ',
			'somefile',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			' ',
			'abc '
		}, debug)

	def test_01_empty_path_2(self):
		"""
		Tests that patterns that end with an escaped space will be treated properly.
		"""
		with self.assertRaises(GitWildMatchPatternError):
			# An escape with double spaces is invalid. Disallow it. Better to be safe
			# than sorry.
			PathSpec.from_lines('gitwildmatch', [
				'\\  ',
			])

	def test_01_match_file_1_include(self):
		"""
		Test matching a single file that is included.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		include = spec.match_file("include.txt")

		self.assertIs(include, True)

	def test_01_match_file_2_exclude(self):
		"""
		Test matching a single file that is excluded.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		include = spec.match_file("test/exclude.txt")

		self.assertIs(include, False)

	def test_01_match_file_3_unmatch(self):
		"""
		Test match a single file that is unmatched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			"*.txt",
			"!test/",
		])

		include = spec.match_file("unmatch.bin")

		self.assertIs(include, False)

	def test_01_match_files(self):
		"""
		Test that matching files one at a time yields the same results as matching
		multiples files at once.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		files = {
			'test1/a.txt',
			'test1/b.txt',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/b.txt',
			'test2/c/c.txt',
		}

		single_files = set(filter(spec.match_file, files))
		multi_files = set(spec.match_files(files))

		self.assertEqual(single_files, multi_files)

	def test_01_windows_current_dir_paths(self):
		"""
		Tests that paths referencing the current directory will be properly
		normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		files = {
			'.\\test1\\a.txt',
			'.\\test1\\b.txt',
			'.\\test1\\c\\c.txt',
			'.\\test2\\a.txt',
			'.\\test2\\b.txt',
			'.\\test2\\c\\c.txt',
		}

		results = list(spec.check_files(files, separators=['\\']))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'.\\test2\\a.txt',
			'.\\test2\\b.txt',
			'.\\test2\\c\\c.txt',
		}, debug)

	def test_01_windows_paths(self):
		"""
		Tests that Windows paths will be properly normalized and matched.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/',
		])
		files = {
			'test1\\a.txt',
			'test1\\b.txt',
			'test1\\c\\c.txt',
			'test2\\a.txt',
			'test2\\b.txt',
			'test2\\c\\c.txt',
		}

		results = list(spec.check_files(files, separators=['\\']))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'test2\\a.txt',
			'test2\\b.txt',
			'test2\\c\\c.txt',
		}, debug)

	def test_02_eq(self):
		"""
		Tests equality.
		"""
		first_spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/**',
		])
		second_spec = PathSpec.from_lines('gitwildmatch', [
			'*.txt',
			'!test1/**',
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
			'test.png',
			'test.txt',
		])
		second_spec = PathSpec.from_lines('gitwildmatch', [
			'test.html',
			'test.jpg',
		])
		combined_spec = first_spec + second_spec
		files = {
			'test.html',
			'test.jpg',
			'test.png',
			'test.txt',
		}

		results = list(combined_spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(combined_spec, results)

		self.assertEqual(includes, {
			'test.html',
			'test.jpg',
			'test.png',
			'test.txt',
		}, debug)

	def test_03_iadd(self):
		"""
		Test spec addition using :data:`+=` operator.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'test.png',
			'test.txt',
		])
		spec += PathSpec.from_lines('gitwildmatch', [
			'test.html',
			'test.jpg',
		])
		files = {
			'test.html',
			'test.jpg',
			'test.png',
			'test.txt',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'test.html',
			'test.jpg',
			'test.png',
			'test.txt',
		}, debug)

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
		includes = {
			__entry.path for __entry in spec.match_entries(entries)
		}

		self.assertEqual(includes, set(map(ospath, [
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
		files = {
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		}

		includes = set(filter(spec.match_file, files))

		self.assertEqual(includes, {
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
		files = {
			'X/a.txt',
			'X/b.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/b.txt',
			'Y/Z/c.txt',
		}

		includes = set(spec.match_files(files))

		self.assertEqual(includes, {
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

		includes = {
			__entry.path for __entry in spec.match_tree_entries(self.temp_dir)
		}

		self.assertEqual(includes, set(map(ospath, [
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

		includes = set(spec.match_tree_files(self.temp_dir))

		self.assertEqual(includes, set(map(ospath, [
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		])))

	def test_06_issue_41_a(self):
		"""
		Test including a file and excluding a directory with the same name pattern,
		scenario A.
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

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			#'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir/file.yaml',
			'file.yaml',
		}, debug)
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		}, debug)

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

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',
			'dir.yaml/index.txt',
			'dir/file.yaml',
			'file.yaml',
		}, debug)
		self.assertEqual(files - ignores, {
			'dir/file.sql',
			'dir/index.txt',
		}, debug)

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

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			#'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir/file.yaml',
			'file.yaml',
		}, debug)
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/file.yaml',  # Discrepancy with Git.
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		}, debug)

	def test_07_issue_62(self):
		"""
		Test including all files and excluding a directory.
		"""
		spec = PathSpec.from_lines('gitwildmatch', [
			'*',
			'!product_dir/',
		])
		files = {
			'anydir/file.txt',
			'product_dir/file.txt',
		}

		results = list(spec.check_files(files))
		includes = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(includes, {
			'anydir/file.txt',
		}, debug)

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

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'a.log',
			'trace.c',
		}, debug)
		self.assertEqual(files - ignores, {
			'b.txt',
			'important/d.log',
			'important/e.txt',
		}, debug)

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
