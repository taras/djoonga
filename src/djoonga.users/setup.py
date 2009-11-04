from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djoonga.users',
      version=version,
      description="Django App to Administer Joomla Users (com_users)",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django joomla',
      author='Positive Sum',
      author_email='taras@positivesum.org',
      url='http://djoonga.com',
      license='BSD License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['djoonga'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'djoonga',          
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
