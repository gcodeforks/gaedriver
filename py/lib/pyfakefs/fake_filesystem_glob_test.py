#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test for fake_filesystem_glob."""

import doctest
import os
import unittest

import fake_filesystem
import fake_filesystem_glob


class FakeGlobUnitTest(unittest.TestCase):

  def setUp(self):
    self.filesystem = fake_filesystem.FakeFilesystem()
    self.glob = fake_filesystem_glob.FakeGlobModule(self.filesystem)
    directory = './xyzzy'
    self.filesystem.CreateDirectory(directory)
    self.filesystem.CreateDirectory(os.path.join(directory, 'subdir'))
    self.filesystem.CreateDirectory(os.path.join(directory, 'subdir2'))
    self.filesystem.CreateFile(os.path.join(directory, 'subfile'))
    self.filesystem.CreateFile('[Temp]')

  def testGlobEmpty(self):
    self.assertEquals(self.glob.glob(''), [])

  def testGlobStar(self):
    self.assertEquals(['/xyzzy/subdir', '/xyzzy/subdir2', '/xyzzy/subfile'],
                      self.glob.glob('/xyzzy/*'))

  def testGlobQuestion(self):
    self.assertEquals(['/xyzzy/subdir', '/xyzzy/subdir2', '/xyzzy/subfile'],
                      self.glob.glob('/x?zz?/*'))

  def testGlobNoMagic(self):
    self.assertEquals(['/xyzzy'], self.glob.glob('/xyzzy'))
    self.assertEquals(['/xyzzy/subdir'], self.glob.glob('/xyzzy/subdir'))

  def testNonExistentPath(self):
    self.assertEquals([], self.glob.glob('nonexistent'))

  def testDocTest(self):
    self.assertFalse(doctest.testmod(fake_filesystem_glob)[0])

  def testMagicDir(self):
    self.assertEquals(['/[Temp]'], self.glob.glob('/*emp*'))

  def testRootGlob(self):
    self.assertEquals(['[Temp]', 'xyzzy'], self.glob.glob('*'))

  def testGlob1(self):
    self.assertEquals(['[Temp]'], self.glob.glob1('/', '*Tem*'))

  def testHasMagic(self):
    self.assertTrue(self.glob.has_magic('['))
    self.assertFalse(self.glob.has_magic('a'))


if __name__ == '__main__':
  unittest.main()
