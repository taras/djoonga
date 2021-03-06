from setuptools import setup, find_packages
import sys
import os

version = '0.1'

setup(name='djoonga.deployment',
      version=version,
      description="Djoonga Deployment Tools",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='djoonga depoloyment',
      author='Taras Mankovski',
      author_email='taras@positivesum.org',
      url='http://djoonga.org',
      license='BSD License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['djoonga'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'djoonga',
          'GitPython',
          'Schema-Sync==0.9'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
