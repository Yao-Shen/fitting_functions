from lmfit.model import Model
from lmfit.models import guess_from_peak, update_param_vals

from .extra_lineshapes import paramagnon, magnon, zero2Linear, zero2Quad


COMMON_DOC = """

Parameters
----------
independent_vars: list of strings to be set as variable names
missing: None, 'drop', or 'raise'
    None: Do not check for null or missing values.
    'drop': Drop null or missing observations in data.
        Use pandas.isnull if pandas is available; otherwise,
        silently fall back to numpy.isnan.
    'raise': Raise a (more helpful) exception when data contains null
        or missing values.
prefix: string to prepend to paramter names, needed to add two Models that
    have parameter names in common. None by default.
"""

class ParaMagnonModel(Model):
    __doc__ = paramagnon.__doc__ + COMMON_DOC if magnon.__doc__ else ""
    def __init__(self, *args, **kwargs):
        super(ParaMagnonModel, self).__init__(magnon, *args, **kwargs)
        self.set_param_hint('sigma', min=0)
        self.set_param_hint('res', min=0)
        self.set_param_hint('kBT', min=0)

    def guess(self, data, x=None, negative=False, **kwargs):
        pars = guess_from_peak(self, data, x, negative, ampscale=0.5, amp_area=False)
        pname = "%s%s" % (self.prefix, 'res')
        pars[pname].value = .1
        pname = "%s%s" % (self.prefix, 'kbT')
        pars[pname].value = .01
        return update_param_vals(pars, self.prefix, **kwargs)

class MagnonModel(Model):
    __doc__ = magnon.__doc__ + COMMON_DOC if magnon.__doc__ else ""
    def __init__(self, *args, **kwargs):
        super(MagnonModel, self).__init__(magnon, *args, **kwargs)
        self.set_param_hint('sigma', min=0)
        self.set_param_hint('res', min=0)
        self.set_param_hint('kBT', min=0)

    def guess(self, data, x=None, negative=False, **kwargs):
        pars = guess_from_peak(self, data, x, negative, ampscale=0.5, amp_area=False)
        pname = "%s%s" % (self.prefix, 'res')
        pars[pname].value = .1
        pname = "%s%s" % (self.prefix, 'kbT')
        pars[pname].value = .01
        return update_param_vals(pars, self.prefix, **kwargs)

class Zero2LinearModel(Model):
    __doc__ = zero2Linear.__doc__ + COMMON_DOC if magnon.__doc__ else ""
    def __init__(self, *args, **kwargs):
        super(Zero2LinearModel, self).__init__(zero2Linear, *args, **kwargs)
        self.set_param_hint('sigma', min=0)

class Zero2QuadModel(Model):
    __doc__ = zero2Quad.__doc__ + COMMON_DOC if magnon.__doc__ else ""
    def __init__(self, *args, **kwargs):
        super(Zero2QuadModel, self).__init__(zero2Quad, *args, **kwargs)
        self.set_param_hint('sigma', min=0)

    #Is guess needed?
    #def guess(self, data, x=None, negative=False, **kwargs):
    #    pars = guess_from_peak(self, data, x, negative, ampscale=0.5, amp_area=False)
    #    return update_param_vals(pars, self.prefix, **kwargs)

# stuff from Vivek
# class LorentzianSquaredModel(Model):
#     __doc__ = lorentzian_squared.__doc__ + COMMON_DOC if lorentzian_squared.__doc__ else ""
#     fwhm_factor = 2.0*np.sqrt(np.sqrt(2)-1)
#     def __init__(self, *args, **kwargs):
#         super(LorentzianSquaredModel, self).__init__(lorentzian_squared, *args, **kwargs)
#         self.set_param_hint('sigma', min=0)
#         self.set_param_hint('fwhm', expr=fwhm_expr(self))
#
#     def guess(self, data, x=None, negative=False, **kwargs):
#         pars = guess_from_peak(self, data, x, negative, ampscale=0.5, amp_area=False)
#         return update_param_vals(pars, self.prefix, **kwargs)
#
#
# class PlaneModel(Model):
#     __doc__ = plane.__doc__ + COMMON_DOC if plane.__doc__ else ""
#     def __init__(self, *args, **kwargs):
#         super(PlaneModel, self).__init__(plane, *args, **kwargs)
#
#     def guess(self, data, x=None, **kwargs):
#         sxval, syval, oval = 0., 0., 0.
#         if x is not None:
#             not_nan_inds = ~np.isnan(data)
#             sxval, oval = np.polyfit(x[0][not_nan_inds], data[not_nan_inds], 1)
#             syval, oval = np.polyfit(x[1][not_nan_inds], data[not_nan_inds], 1)
#         pars = self.make_params(intercept=oval, slope_x=sxval, slope_y=syval)
#         return update_param_vals(pars, self.prefix, **kwargs)
#
#
# class LorentzianSquared2DModel(Model):
#     __doc__ = lor2_2D.__doc__ + COMMON_DOC if lor2_2D.__doc__ else ""
#     fwhm_factor = 2.0*np.sqrt(np.sqrt(2)-1)
#     def __init__(self, *args, **kwargs):
#         super(LorentzianSquared2DModel, self).__init__(lor2_2D, *args, **kwargs)
#         self.set_param_hint('sigma_x', min=0)
#         self.set_param_hint('sigma_y', min=0)
#
#         self.set_param_hint('fwhm_x', expr=_fwhm_expr_2D(self, parameter='sigma_x'))
#         self.set_param_hint('fwhm_y', expr=_fwhm_expr_2D(self, parameter='sigma_y'))
#
#     def guess(self, data, x=None, negative=False, **kwargs):
#         pars = guess_from_peak_2D(self, data, x, negative, ampscale=1.25, amp_area=False)
#         return update_param_vals(pars, self.prefix, **kwargs)
#
#
# class Gaussian2DModel(Model):
#     __doc__ = gauss_2D.__doc__ + COMMON_DOC if gauss_2D.__doc__ else ""
#     fwhm_factor = 2.354820
#     def __init__(self, *args, **kwargs):
#         super(Gaussian2DModel, self).__init__(gauss_2D, *args, **kwargs)
#         self.set_param_hint('sigma_x', min=0)
#         self.set_param_hint('sigma_y', min=0)
#         self.set_param_hint('fwhm_x', expr=_fwhm_expr_2D(self, parameter='sigma_x'))
#         self.set_param_hint('fwhm_y', expr=_fwhm_expr_2D(self, parameter='sigma_y'))
#
#     def guess(self, data, x=None, negative=False, **kwargs):
#         pars = guess_from_peak_2D(self, data, x, negative, ampscale=1., amp_area=False)
#         return update_param_vals(pars, self.prefix, **kwargs)
