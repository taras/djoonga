from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djoonga',
      version=version,
      description="Main Djoonga Package",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Taras Mankovski',
      author_email='taras@positivesum.org',
      url='http://djoonga.com',
      license='BSD License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Django >=1.1',
          'phpserialize >= 1.2'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      development=djoonga.main:development
      production=djoonga.main:production
      """,
      )
