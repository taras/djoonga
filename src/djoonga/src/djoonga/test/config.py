"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import subprocess

class JConfigTest(TestCase):

    def test_php_in_path(self):
        """
        Verify that PHP executable is in PATH
        """
        cmd = ['which', 'php']
        retcode = subprocess.call(cmd, stdout=subprocess.PIPE)
        self.assertFalse(retcode)

    def test_php_cli_available(self):
        """
        Verify that PHP cli is available
        """
        cmd = ['php', '-r', 'echo "test";']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        self.assertEqual(out, 'test')


