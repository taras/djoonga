import unittest
from djoonga.core.hacks import fix_datetime

class HacksTestCase(unittest.TestCase):

    def test_decorator_parameters(self):

        @fix_datetime(None, None)
        def decorated_function_missing_table():
            pass

        self.assertRaises(Exception, decorated_function_missing_table)

        @fix_datetime('jos_modules', None)
        def decorated_function_mising_field():
            pass

        self.assertRaises(Exception, decorated_function_mising_field)

        @fix_datetime('jos_modules', ())
        def decorated_function_empty_fields():
            pass

        self.assertRaises(Exception, decorated_function_empty_fields)

    def test_decorated_function_properties(self):

        @fix_datetime('jos_modules', 'checked_out_time')
        def function_with_docstring():
            "This is a docstring."
            pass

        self.assert_(function_with_docstring.__doc__ == "This is a docstring.", 'Docstrings did not match.')
        self.assert_(function_with_docstring.__name__ == "function_with_docstring", 'Expected function_with_docstring, got %s'%function_with_docstring.__name__)

    def test_decorated_function_with_parameter(self):

        @fix_datetime('jos_modules', 'checked_out_time')
        def function_with_parameter(item):
            return item

        expected = 'testing'
        result = function_with_parameter(expected)
        self.assert_(expected == result, 'Expected %s, got %s'%(expected, result))

    def test_decorated_method_class(self):

        class SampleClass(object):

            def __init__(self, arg1):
                self.s = arg1

            @fix_datetime('jos_modules', 'checked_out_time')
            def get(self):
                return self.s

        sc = SampleClass('hello')
        expected = 'hello'
        result = sc.get()
        self.assert_(expected == result, 'Expected %s, got %s'%(expected, result))

    def test_multiple_decoration(self):

        @fix_datetime('jos_content', ('created', 'modified'))
        def function_with_parameter(item):
            return item

        class SampleClass(object):

            def __init__(self, arg1):
                self.s = arg1

            @fix_datetime('jos_content', ('created', 'modified'))
            def get(self):
                return self.s

        sc = SampleClass('hello')
        expected = 'hello'
        result = sc.get()
        self.assert_(expected == result, 'Expected %s, got %s'%(expected, result))



