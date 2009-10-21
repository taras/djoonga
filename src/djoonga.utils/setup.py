from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djoonga.utils',
      version=version,
      description="Utilities package for Djoonga project",
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
        'phpserialize == 1.2'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
