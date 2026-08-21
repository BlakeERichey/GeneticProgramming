import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

setup(name='tpcomp',
      version='0.0.1',
      packages=find_packages(),
      description='Topological Computing DES',
      long_description_content_type="text/markdown",
      author = 'Blake Richey',
      author_email='blake.e.richey@gmail.com',
      url='',
      license='MIT',
      python_requires='>=3.6',
      install_requires=[
      ],
    )