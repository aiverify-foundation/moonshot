"""
This script tests :class:`.GitIgnoreSpec`.
"""

import unittest

from pathspec.gitignore import (
	GitIgnoreSpec)


class GitIgnoreSpecTest(unittest.TestCase):
	"""
	The :class:`GitIgnoreSpecTest` class tests the :class:`.GitIgnoreSpec`
	class.
	"""

	def test_01_reversed_args(self):
		"""
		Test reversed args for `.from_lines()`.
		"""
		spec = GitIgnoreSpec.from_lines('gitwildmatch', ['*.txt'])
		results = set(spec.match_files([
			'a.txt',
			'b.bin',
		]))
		self.assertEqual(results, {
			'a.txt',
		})

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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'test1/a.txt',
			'test1/c/c.txt',
			'test2/a.txt',
			'test2/c/c.txt',
		})
		self.assertEqual(files - ignores, {
			'test1/b.bin',
			'test2/b.bin',
		})

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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'X/a.txt',
			'X/Z/c.txt',
			'Y/a.txt',
			'Y/Z/c.txt',
		})
		self.assertEqual(files - ignores, {
			'X/b.txt',
			'Y/b.txt',
		})

	def test_02_issue_41_a(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario A.
		"""
		spec = GitIgnoreSpec.from_lines([
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
			'dir.yaml/file.yaml',
			'dir/file.yaml',
			'file.yaml',
		})
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		})

	def test_02_issue_41_b(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario B.
		"""
		spec = GitIgnoreSpec.from_lines([
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

	def test_02_issue_41_c(self):
		"""
		Test including a file and excluding a directory with the same name
		pattern, scenario C.
		"""
		spec = GitIgnoreSpec.from_lines([
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
			'dir.yaml/file.yaml',
			'dir/file.yaml',
			'file.yaml',
		})
		self.assertEqual(files - ignores, {
			'dir.yaml/file.sql',
			'dir.yaml/index.txt',
			'dir/file.sql',
			'dir/index.txt',
		})

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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		})
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		})

	def test_03_issue_19_a(self):
		"""
		Test matching files in a subdirectory of an included directory,
		scenario A.
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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		})
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		})

	def test_03_issue_19_b(self):
		"""
		Test matching files in a subdirectory of an included directory,
		scenario B.
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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		})
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		})

	def test_03_issue_19_c(self):
		"""
		Test matching files in a subdirectory of an included directory,
		scenario C.
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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'dirG/dirH/fileI',
			'dirG/dirH/fileJ',
			'dirG/fileO',
		})
		self.assertEqual(files - ignores, {
			'fileA',
			'fileB',
			'dirD/fileE',
			'dirD/fileF',
		})

	def test_04_issue_62(self):
		"""
		Test including all files and excluding a directory.
		"""
		spec = GitIgnoreSpec.from_lines([
			'*',
			'!product_dir/',
		])
		results = set(spec.match_files([
			'anydir/file.txt',
			'product_dir/file.txt',
		]))
		self.assertEqual(results, {
			'anydir/file.txt',
			'product_dir/file.txt',
		})

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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, files)

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
		ignores = set(spec.match_files(files))
		self.assertEqual(ignores, {
			'test1/b.bin',
			'test1/a.txt',
			'test1/c/c.txt',
			'test2/b.bin',
		})
		self.assertEqual(files - ignores, {
			'test2/a.txt',
			'test2/c/c.txt',
		})
