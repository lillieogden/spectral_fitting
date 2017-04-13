from __future__ import division
import numpy as np
from process_data import load_data
from scipy import optimize
import matplotlib.pyplot as plt
import pandas as pd
from os.path import isfile
plt.ion()

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
    u_star = u_star[None,:]
    Uhor = (dat_bin.u ** 2 + dat_bin.v ** 2) ** .5
    U_hor = Uhor[inds_t]
    U_hor = U_hor[:, None]
    return u_star, U_hor


def def_x_y(dat_bin, z, u_star, U_hor, inds_t, inds_f):
    """Defines x and y and normalizes them"""
    f = dat_bin.freq
    f = f[inds_f][inds_t]
    f = f[None,:]
    y = dat_bin.Spec[0, inds_t] * pii
    y_list = []
    for i in range(len(y)):
        y_list.append(y[i][inds_t])
    Su = np.asarray(y_list)

    f_norm = (f * z) / U_hor
    Su_norm = (Su * U_hor) / (z * u_star)
    return f_norm, Su_norm, f, y


def spectra_fit_plot(f_norm, f, Su, title, popt, u_star, U_hor):
    """Plots the spectral fit over the data"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # plot our data
    ax.loglog(f, Su, 'b-')
    ax.set_autoscale_on(False)  # Otherwise, infinite loop

    Su_theory_norm = function(f_norm, popt[0], popt[1])
    Su_theory = Su_theory_norm * u_star * z / U_hor
    ax.loglog(f_norm * U_hor / z, Su_theory, 'r-')
    ax.set_title(title)
    fig.savefig('./figures/spectral_fits/u/' + title + '.png')

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

f_flat = []
Su_flat = []
for i in range(len(f_norms)):
    for item in f_norms[i]:
        f_flat.append(item)
for i in range(len(Su_norms)):
    for item in Su_norms[i]:
        Su_flat.append(item)

# when joining large arrays, it takes a lot memory so use numpy.hstack/vstack to turn into array
# flatten the data before giving it to the fit function
popt, pcov = optimize.curve_fit(function, f_flat, Su_flat)
