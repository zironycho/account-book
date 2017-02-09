from setuptools import setup, find_packages

setup(
    name='account-book',
    version='0.1',
    py_modules=find_packages(),
    install_requires=[],
    entry_points='''
        [console_scripts]
        acbook=cli:report
    ''',
)
