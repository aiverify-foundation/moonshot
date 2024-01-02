"""
This script tests :class:`.GitIgnoreSpec`.
"""

import unittest

from pathspec.gitignore import (
	GitIgnoreSpec)

from .util import (
	debug_results,
	get_includes)


class GitIgnoreSpecTest(unittest.TestCase):
	"""
	The :class:`GitIgnoreSpecTest` class tests the :class:`.GitIgnoreSpec` class.
	"""

	def test_01_reversed_args(self):
		"""
		Test reversed args for `.from_lines()`.
		"""
		spec = GitIgnoreSpec.from_lines('gitwildmatch', ['*.txt'])
		files = {
			'a.txt',
			'b.bin',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'a.txt',
		}, debug)

	def test_02_dir_exclusions(self):
		"""
		Test directory exclusions.
		"""
		spec = GitIgnoreSpec.from_lines([
			'*.txt',
			'!test1/',
		])
		files = {
			'test1/a.txt',
			'test1/b.bin',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/b.bin',
			'test2/c/c.txt',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'test1/a.txt',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/c/c.txt',
		}, debug)
		self.assertEqual(files - ignores, {
			'test1/b.bin',
			'test2/b.bin',
		}, debug)

	def test_02_file_exclusions(self):
		"""
		Test file exclusions.
		"""
		spec = GitIgnoreSpec.from_lines([
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

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		}, debug)
		self.assertEqual(files - ignores, {
			'X/b.txt',
			'Y/b.txt',
		}, debug)

	def test_02_issue_41_a(self):
		"""
		Test including a file and excluding a directory with the same name pattern,
		scenario A.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			'*.yaml',
			'!*.yaml/',
		])
		files = {
			'dir.yaml/file.sql',   # -
			'dir.yaml/file.yaml',  # 1:*.yaml
			'dir.yaml/index.txt',  # -
			'dir/file.sql',        # -
			'dir/file.yaml',       # 1:*.yaml
			'dir/index.txt',       # -
			'file.yaml',           # 1:*.yaml
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dir.yaml/file.yaml',
			'dir/file.yaml',
			'file.yaml',
		}, debug)
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		}, debug)

	def test_02_issue_41_b(self):
		"""
		Test including a file and excluding a directory with the same name pattern,
		scenario B.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			'!*.yaml/',
			'*.yaml',
		])
		files = {
			'dir.yaml/file.sql',   # 2:*.yaml
			'dir.yaml/file.yaml',  # 2:*.yaml
			'dir.yaml/index.txt',  # 2:*.yaml
			'dir/file.sql',        # -
			'dir/file.yaml',       # 2:*.yaml
			'dir/index.txt',       # -
			'file.yaml',           # 2:*.yaml
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

	def test_02_issue_41_c(self):
		"""
		Test including a file and excluding a directory with the same name pattern,
		scenario C.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			'*.yaml',
			'!dir.yaml',
		])
		files = {
			'dir.yaml/file.sql',   # -
			'dir.yaml/file.yaml',  # 1:*.yaml
			'dir.yaml/index.txt',  # -
			'dir/file.sql',        # -
			'dir/file.yaml',       # 1:*.yaml
			'dir/index.txt',       # -
			'file.yaml',           # 1:*.yaml
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dir.yaml/file.yaml',
			'dir/file.yaml',
			'file.yaml',
		}, debug)
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		}, debug)

	def test_03_subdir(self):
		"""
		Test matching files in a subdirectory of an included directory.
		"""
		spec = GitIgnoreSpec.from_lines([
			"dirG/",
		])
		files = {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}, debug)
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		}, debug)

	def test_03_issue_19_a(self):
		"""
		Test matching files in a subdirectory of an included directory, scenario A.
		"""
		spec = GitIgnoreSpec.from_lines([
			"dirG/",
		])
		files = {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}, debug)
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		}, debug)

	def test_03_issue_19_b(self):
		"""
		Test matching files in a subdirectory of an included directory, scenario B.
		"""
		spec = GitIgnoreSpec.from_lines([
			"dirG/*",
		])
		files = {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}, debug)
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		}, debug)

	def test_03_issue_19_c(self):
		"""
		Test matching files in a subdirectory of an included directory, scenario C.
		"""
		spec = GitIgnoreSpec.from_lines([
			"dirG/**",
		])
		files = {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		}, debug)
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		}, debug)

	def test_04_issue_62(self):
		"""
		Test including all files and excluding a directory.
		"""
		spec = GitIgnoreSpec.from_lines([
			'*',
			'!product_dir/',
		])
		files = {
			'anydir/file.txt',
			'product_dir/file.txt',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'anydir/file.txt',
			'product_dir/file.txt',
		}, debug)

	def test_05_issue_39(self):
		"""
		Test excluding files in a directory.
		"""
		spec = GitIgnoreSpec.from_lines([
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

	def test_06_issue_64(self):
		"""
		Test using a double asterisk pattern.
		"""
		spec = GitIgnoreSpec.from_lines([
			"**",
		])
		files = {
			'x',
			'y.py',
			'A/x',
			'A/y.py',
			'A/B/x',
			'A/B/y.py',
			'A/B/C/x',
			'A/B/C/y.py',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, files, debug)

	def test_07_issue_74(self):
		"""
		Test include directory should override exclude file.
		"""
		spec = GitIgnoreSpec.from_lines([
			'*',  # Ignore all files by default
			'!*/',  # but scan all directories
			'!*.txt',  # Text files
			'/test1/**',  # ignore all in the directory
		])
		files = {
			'test1/b.bin',
			'test1/a.txt',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/b.bin',
			'test2/c/c.txt',
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			'test1/b.bin',
			'test1/a.txt',
			'test1/c/c.txt',
			'test2/b.bin',
		}, debug)
		self.assertEqual(files - ignores, {
			'test2/a.txt',
			'test2/c/c.txt',
		}, debug)

	def test_08_issue_81_a(self):
		"""
		Test issue 81 whitelist, scenario A.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			"*",
			"!libfoo",
			"!libfoo/**",
		])
		files = {
			"ignore.txt",          # 1:*
			"libfoo/__init__.py",  # 3:!libfoo/**
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			"ignore.txt",
		}, debug)
		self.assertEqual(files - ignores, {
			"libfoo/__init__.py",
		}, debug)

	def test_08_issue_81_b(self):
		"""
		Test issue 81 whitelist, scenario B.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			"*",
			"!libfoo",
			"!libfoo/*",
		])
		files = {
			"ignore.txt",          # 1:*
			"libfoo/__init__.py",  # 3:!libfoo/*
		}

		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)

		self.assertEqual(ignores, {
			"ignore.txt",
		}, debug)
		self.assertEqual(files - ignores, {
			"libfoo/__init__.py",
		}, debug)

	def test_08_issue_81_c(self):
		"""
		Test issue 81 whitelist, scenario C.
		"""
		# Confirmed results with git (v2.42.0).
		spec = GitIgnoreSpec.from_lines([
			"*",
			"!libfoo",
			"!libfoo/",
		])
		files = {
			"ignore.txt",          # 1:*
			"libfoo/__init__.py",  # 1:*
		}
		results = list(spec.check_files(files))
		ignores = get_includes(results)
		debug = debug_results(spec, results)
		self.assertEqual(ignores, {
			"ignore.txt",
			"libfoo/__init__.py",
		}, debug)
		self.assertEqual(files - ignores, set())
