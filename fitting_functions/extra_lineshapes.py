import numpy as np

def bose(x, kBT):
    """ Bose factor
    kBT should be in the same units as x
    kB = 8.617e-5 eV/K """
    return np.real(1./ (1 - np.exp(-x / (8.6173303e-2 * T)) +0.00001*1j ))

def make_gaussian_kernal(x, sigma):
    """ Return normalized Gaussian kernal suitable for performing a convolution
    This ensures even steps mirroring x."""
    step = np.abs(np.mean(np.diff(x)))
    x_kern = np.arange(-sigma*5, sigma*5, step)
    y = np.exp(-x**2/(2 * sigma**2))
    return y / np.sum(y)

def convolve(y, kernal):
    """ Convolve signal y with kernal. """
    return np.convolve(y, kernal, mode='same')

def Lorenzian(x, amplitude, center, sigma):
    """ Lorentizan defined by peak height """
    return amplitude/((x-center)**2+sigma**2)

def antisymlorz(x, center=0.15, amplitude=0.1, sigma=0.05, kBT=8.617e-5*100):
    """Antisymmeterized Lorentzian
    """
    def lor(x, center, amplitude, sigma):
        return amplitude / (1. + ((x - center) / sigma)**2)

    chi = Lorenzian(x, amplitude, center, sigma) - Lorenzian(x, amplitude, center, sigma)
    return chi
