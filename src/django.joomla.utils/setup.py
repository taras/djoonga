from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django.joomla.utils',
      version=version,
      description="Python package with supporting packages for Django Joomla applications",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django joomla',
      author='Positive Sum',
      author_email='taras@positivesum.org',
      url='http://github.com/taras/django.joomla',
      license='BSD License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['django', 'django.joomla'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
