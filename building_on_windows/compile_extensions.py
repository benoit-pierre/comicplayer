from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "Row detector in cython",
    ext_modules = cythonize("libs\\*.pyx"),
)
