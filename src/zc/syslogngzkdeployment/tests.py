##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.testing import setupstack
import manuel.capture
import manuel.doctest
import manuel.testing
import mock
import unittest
import zc.zk.testing

def faux_call(*args):
    print 'subprocess.call', args

def setUp(test):
    zc.zk.testing.setUp(test, '', 'zookeeper:2181')
    setupstack.context_manager(test, mock.patch('subprocess.call', faux_call))

def test_suite():
    return unittest.TestSuite((
        manuel.testing.TestSuite(
            manuel.doctest.Manuel() + manuel.capture.Manuel(),
            'main.test',
            setUp=setUp, tearDown=setupstack.tearDown,
            ),
        ))

