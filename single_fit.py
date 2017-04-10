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


def def_vars(dat_bin, uinds):
    """Defines the variables"""
    ustar = (dat_bin.upwp_ ** 2 + dat_bin.vpwp_ ** 2) ** .5
    u_star = ustar[uinds].mean()
    Uhor = (dat_bin.u ** 2 + dat_bin.v ** 2) ** .5
    U_hor = Uhor[uinds].mean()
    return u_star, U_hor


def def_x_y(dat_bin, z, u_star, U_hor, uinds, freqinds):
    """Defines x and y and normalizes them"""
    x = dat_bin.freq
    x = x[freqinds][uinds]
    y = dat_bin.Spec[0, uinds] * pii
    x_norm = (x * z) / U_hor
    y_norm = (y * U_hor) / (z * u_star)
    return x_norm, y_norm, x, y


def spectra_fit_plot(x_norm, x, y, title, popt, u_star, U_hor):
    """Plots the spectral fit over the data"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # plot our data
    ax.loglog(x, y, 'b-')
    ax.set_autoscale_on(False)  # Otherwise, infinite loop

    y_theory_norm = function(x_norm, popt[0], popt[1])
    y_theory = y_theory_norm * u_star * z / U_hor
    ax.loglog(x_norm * U_hor / z, y_theory, 'r-')
    ax.set_title(title)
    fig.savefig('./figures/spectral_fits/u/' + title + '.png')

xs = []
ys = []
x_norms = []
y_norms = []
for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    uinds = abs(dat_bin.u) > 0.5
    freqinds = dat_bin.freq > 1
    u_star, U_hor = def_vars(dat_bin, uinds)
    x_norm, y_norm, x, y = def_x_y(dat_bin, z, u_star, U_hor, uinds, freqinds)
    for item in x:
        xs.append(item)
    for item in y:
        ys.append(item)
    for item in x_norm:
        x_norms.append(item)
    for item in y_norm:
        y_norms.append(item)

popt, pcov = optimize.curve_fit(function, x_norms, y_norms)
