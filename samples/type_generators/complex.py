import numpy as np

from .numbers import number_generator


def generate_complex():
    real, imag = (float(number_generator()[1]()) for _ in range(2))
    return str(np.complex128(real + 1j * imag))


def complex_generator():
    return ("complex", generate_complex)
