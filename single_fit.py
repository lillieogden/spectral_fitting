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

fs = []
Sus = []
f_norms = []
Su_norms = []
for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    inds_t = abs(dat_bin.u**2 +dat_bin.v**2) > 0.5
    inds_f = dat_bin.freq > 1
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

popt, pcov = optimize.curve_fit(function, f_final, Su_final)
spectra_fit_plot(f_final, Su_final, 'Single Fit', popt)
