import numpy as np
from lmfit.lineshapes import lorentzian

def magnon(x, amplitude, center, sigma, res, kBT):
    """Return a 1-dimensional Antisymmeterized Lorenzian multiplied by Bose factor
    and convolved with resolution.
    magnon(x, amplitude, center, sigma, res, kBT) =
        convolve(antisymlorz(x, amplitude, center, sigma)*bose(x, kBT), kernal)
    """
    step = min(np.abs(np.mean(np.diff(x))), sigma, res) / 20
    x_magnon = np.arange(-res*20, res*20, step)
    kernal = make_gaussian_kernal(x_magnon, res)
    y_magnon = convolve(antisymlorz(x_magnon, amplitude, center, sigma)*bose(x_magnon, kBT), kernal)
    return np.interp(x, x_magnon, y_magnon)

def bose(x, kBT):
    """Return a 1-dimensinoal Bose factor function
    kBT should be in the same units as x
    bose(x, kBT) = 1 / (1 - exp(-x / kBT) )

    n.b. kB = 8.617e-5 eV/K
    """
    return np.real(1./ (1 - np.exp(-x / (kBT)) +0.00001*1j ))

def make_gaussian_kernal(x, sigma):
    """Return 1-dimensional normalized Gaussian kernal suitable for performing a convolution
    This ensures even steps mirroring x.
    make_gaussian_kernal(x, sigma) =
        exp(-x**2 / (2*sigma**2))
    """
    step = np.abs(np.mean(np.diff(x)))
    x_kern = np.arange(-sigma*10, sigma*10, step)
    y = np.exp(-x_kern**2/(2 * sigma**2))
    return y / np.sum(y)

def convolve(y, kernal):
    """ Convolve signal y with kernal. """
    return np.convolve(y, kernal, mode='same')

def zero2Linear(x, center=0, sigma=1, grad=1):
    """Return 1-dimension function that goes from zero << x0 to linear >> x0
    the cross over is smooth as controlled by gaussian convolution of width x
    zero2Linear(x, x0, sigma, grad) =
    0       : x<center
    (x-center)*grad  : x>center
    convolved by gaussian(x, sigma)
    """
    step = min(np.abs(np.mean(np.diff(x))), sigma) / 20
    x_linear = np.arange(-20*sigma+np.min(x), 20*sigma+np.max(x), step)
    y_linear = (x_linear-center)*grad
    y_linear[x_linear<center] = 0
    y_linear = convolve(y_linear, make_gaussian_kernal(x_linear, sigma))
    return np.interp(x, x_linear, y_linear)

def zero2Quad(x, center=0, sigma=1, quad=1):
    """Return 1-dimension function that goes from zero << x0 to quadratic >> x0
    the cross over is smooth as controlled by gaussian convolution of width x
    zero2Linear(x, x0, sigma, grad) =
    0                       : x<center
    (x-center)**2 * quad    : x>center
    convolved by gaussian(x, sigma)
    """
    step = min(np.abs(np.mean(np.diff(x))), sigma) / 20
    x_quad = np.arange(-20*sigma+np.min(x), 20*sigma+np.max(x), step)
    y_quad = (x_quad-center)**2 * quad
    y_quad[x_quad<center] = 0
    y_quad = convolve(y_quad, make_gaussian_kernal(x_quad, sigma))
    return np.interp(x, x_quad, y_quad)

def antisymlorz(x, amplitude=0.1, center=0.15, sigma=0.05):
    """ Return Antisymmeterized Lorentzian
    antisymlorz(x, amplitude, center, sigma) =
        lorentzian(x, amplitude, center, sigma) - lorentzian(x, amplitude, -center, sigma)
    """
    chi = lorentzian(x, amplitude, center, sigma) - lorentzian(x, amplitude, -center, sigma)
    return chi