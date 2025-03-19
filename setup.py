#run 'python setup.py build_ext --inplace' to compile
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("DSPcmath.pyx")
)