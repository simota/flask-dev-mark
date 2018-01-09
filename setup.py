from setuptools import setup, find_packages

setup(
    name='flask-dev-mark-middleware',
    version='0.0.1',
    description='Show dev mark on flask app',
    license='MIT',
    author='simota',
    author_email='simota@me.com',
    url='https://github.com/simota/flask-dev-mark.git',
    keywords='flask-dev-mark',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.10',
    ],
    test_suite='tests',
)
