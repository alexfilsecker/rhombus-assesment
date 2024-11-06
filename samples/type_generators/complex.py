import numpy as np

from .numbers import generate_float64


def generate_complex():
    real, imag = (generate_float64() for _ in range(2))
    return str(np.complex128(real + 1j * imag))


def complex_generator():
    return ("complex", generate_complex)
