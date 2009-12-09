from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djoonga.recipe.joomla',
      version=version,
      description="Buildout recipe for intalling and updating Joomla! sites",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='joomla djoonga buildout recipe',
      author='Taras Mankovski',
      author_email='taras@positivesum.org',
      url='http://github.com/taras/djoonga/src/djoonga.recipe.joomla',
      license='GNU General Public License',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['djoonga', 'djoonga.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
