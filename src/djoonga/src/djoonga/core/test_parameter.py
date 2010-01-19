# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from djoonga.core.parameter import JParameter

teststr = '''
option1=test1
2option=test2
option=test3

option5=test4
'''

class  JParameterTestCase(unittest.TestCase):

    def test_parse_parameters(self):
        params = JParameter(data=teststr)
        self.failUnless(params.get('option1') == 'test1', 'Expected "test1" but got %s'%params.get('option1'))

    def test_add_parameter(self):
        params = JParameter(data=teststr)
        params.set('newoption', 'worked')
        params.set('intoption', 3)
        newdata = str(params)
        newparams = JParameter(data=newdata)
        self.failUnless(params.get('newoption') == 'worked', 'Expected "worked" got %s'%params.get('newoption'))
        self.failUnless(params.get('intoption') == '3', 'Expected "3" got %s'%params.get('intoption'))

    def test_parameter_format(self):
        params = JParameter(data='hello=test')
        self.failUnless(str(params) == 'hello=test', 'Expected "hello=test" got "%s"'%str(params))
        params = JParameter(data='hello  = taras = again\nagain = test = agggain\nblah = 1')
        expected = 'blah=1\nhello=taras = again\nagain=test = agggain'
        self.failUnless(str(params) == expected, 'Expected "%s" got "%s"'%(expected, str(params)))
        expected = 'Hello=big\nhello=small'
        params = JParameter()
        params.set('Hello', 'big')
        params.set('hello', 'small')
        self.failUnless(params.get('Hello') == 'big' and params.get('hello') == 'small',\
        'Expected "%s" got "%s"'%(expected, str(params)))

if __name__ == '__main__':
    unittest.main()

