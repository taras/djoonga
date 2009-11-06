from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djoonga.reports',
        version=version,
        description="CLI tool that scrapes a website and generates a file of all links on a site.",
        long_description=open('README.rst').read(),
        classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        keywords='',
        author='Taras Mankovski',
        author_email='tarasm@gmail.com',
        url='http://djoonga.com',
        license='BSD License',
        packages=find_packages('src'),
        package_dir = {'': 'src'},
        namespace_packages = ['djoonga'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'scrapy==0.7'
        ],
        entry_points="""
        # -*- Entry points: -*-
        [console_scripts]
        reports=djoonga.reports:main
        """,
        )
