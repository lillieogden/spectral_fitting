from __future__ import division
import numpy as np
from process_data import load_data
from scipy import optimize
import matplotlib.pyplot as plt
import pandas as pd
from os.path import isfile
plt.ion()
import pdb

z = 10
pii = 2 * np.pi

FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014']



def function(x_normalized, a, b):
    """"Defines the functions that will fit the spectral data"""
    return a / (1 + (b * x_normalized)) ** (5 / 3)


def def_vars(dat_bin, inds_t):
    """Defines the variables"""
    ustar = (dat_bin.upwp_ ** 2 + dat_bin.vpwp_ ** 2) ** .5
    u_star = ustar[inds_t]
    u_star = u_star[:,None]
    Uhor = (dat_bin.u ** 2 + dat_bin.v ** 2) ** .5
    U_hor = Uhor[inds_t]
    U_hor = U_hor[:, None]
    return u_star, U_hor


def def_x_y(dat_bin, z, u_star, U_hor, inds_t, inds_f):
    """Defines x and y and normalizes them"""
    f = dat_bin.freq[inds_f][None,:]
    y = dat_bin.Spec[0, inds_t][..., inds_f] * pii
    f_norm = (f * z) / U_hor
    Su_norm = (y * U_hor) / (z * u_star)
    return f_norm, Su_norm, f, y


def spectra_fit_plot(f_final, Su_final,  title, popt):
    """Plots the spectral fit over the data"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # plot our data
    ax.loglog(f_final, Su_final, 'b.', alpha=0.3)
    ax.set_autoscale_on(False)  # Otherwise, infinite loop

    Su_theory = function(f_final, popt[0], popt[1])
    ax.loglog(f_final, Su_theory, 'r-')
    ax.set_title(title)
    fig.savefig('./figures/spectral_fits/' + title + '.png')


def map_hist(x, y, h, bins):
    xi = np.digitize(x, bins[0]) - 1
    yi = np.digitize(y, bins[1]) - 1
    inds = np.ravel_multi_index((xi, yi),
                                (len(bins[0]) - 1, len(bins[1]) - 1),
                                mode='clip')
    vals = h.flatten()[inds]
    bads = ((x < bins[0][0]) | (x > bins[0][-1]) |
            (y < bins[1][0]) | (y > bins[1][-1]))
    vals[bads] = np.NaN
    return vals


def scat_hist2d(f_final, Su_final, f_fit, a, b,
                s=20, marker=u'o',
                mode='mountain',
                bins=10, range=None,
                normed=False, weights=None,  # np.histogram2d args
                edgecolors='none',
                ax=None, dens_func=None):
    """
    Make a scattered-histogram plot.

    Parameters
    ----------
    x, y: array_like, shape (n, )
        Input values

    mode: [None | 'mountain' | 'valley' | 'clip']
       Possible values are:

       - None : The points are plotted as one scatter object, in the
         order in-which they are specified at input.

       - 'mountain' : The points are sorted/plotted in the order of
         the number of points in their 'bin'. This means that points
         in the highest density will be plotted on-top of others. This
         cleans-up the edges a bit, the points near the edges will
         overlap.

       - 'valley' : The reverse order of 'mountain'. The low density
         bins are plotted on top of the high ones.

       - 'clip' : This returns a ?LINE COLLECTION? where points are
         clipped at the edges of their boxes. Thus, there is no
         overlap, but individual (outlier) points will also be
         clipped.


    """
    if ax is None:
        ax = plt.gca()

    h, fe, Sue = np.histogram2d(f_final, Su_final, bins=bins,
                               range=range, normed=normed, weights=weights)
    # bins = (xe, ye)
    dens = map_hist(f_final, Su_final, h, bins=(fe, Sue))
    if dens_func is not None:
        dens = dens_func(dens)
    iorder = slice(None)  # No ordering by default
    if mode == 'mountain':
        iorder = np.argsort(dens)
    elif mode == 'valley':
        iorder = np.argsort(dens)[::-1]
    f_final = f_final[iorder]
    Su_final = Su_final[iorder]
    dens = dens[iorder]

    ax.set_ylim([1e-4, 1e3])
    ax.scatter(f_final, Su_final,
                    s=s, c=dens,
                    edgecolors=edgecolors,
                    marker=marker)
    Su_theory = function(f_fit, popt[0], popt[1])
    ax.loglog(f_fit, Su_theory, 'r-')

    Su_walter = function(f_fit, a, b)
    ax.loglog(f_fit, Su_walter, 'orange')
    plt.savefig('./figures/spectral_fits/single_fit_all_data.png')

fs = []
Sus = []
f_norms = []
Su_norms = []
for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    inds_t = (1.0> abs((dat_bin.u**2 + dat_bin.v**2) ** .5)) & (abs((dat_bin.u**2 + dat_bin.v**2) ** .5) < 1.5)
    inds_f = (dat_bin.freq < 1)
    # inds_f = (dat_bin.freq < 1) & (dat_bin.freq > 0.4)|(dat_bin.freq < .08)
    u_star, U_hor = def_vars(dat_bin, inds_t)
    f_norm, Su_norm, f, Su = def_x_y(dat_bin, z, u_star, U_hor, inds_t, inds_f)
    for item in f:
        fs.append(item)
    for item in Su:
        Sus.append(item)
    for item in f_norm:
        f_norms.append(item)
    for item in Su_norm:
        Su_norms.append(item)

f_final = np.hstack(f_norms)
Su_final = np.hstack(Su_norms)
f_fit = np.sort(f_final)

popt, pcov = optimize.curve_fit(function, f_final, Su_final)
scat_hist2d(f_final, Su_final, f_fit, a = 105, b = 33,
                s=20, marker=u'o',
                mode='mountain',
                bins=(np.logspace(-4, 2, 60), np.logspace(-6, 2, 50)), range=None,
                normed=False, weights=None,  # np.histogram2d args
                edgecolors='none',
                ax=None, dens_func=None)
# spectra_fit_plot(f_final, Su_final, 'Single Fit_1', popt)
