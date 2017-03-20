import numpy as np
from process_data import load_data
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014']

# define constants
z = 10
pii = 2 * np.pi


def function(x_normalized, a, b):
    """"Defines the functions that will fit the spectral data"""
    return a/(1+(b*x_normalized))**(5/3)


def def_vars(dat_bin, uinds):
    """Defines the variables"""
    ustar = (dat_bin.upwp_ ** 2 + dat_bin.vpwp_ ** 2) ** .5
    u_star = ustar[uinds].mean()
    Uhor = (dat_bin.u ** 2 + dat_bin.v ** 2) ** .5
    U_hor = Uhor[uinds].mean()
    return u_star, U_hor


def def_x_y(dat_bin, z, u_star, U_hor, uinds, freq_range):
    """Defines x and y and normalizes them"""
    # ifreq = np.zeros(dat_bin.freq.shape, dtype='bool')
    ifreq = ((freq_range[0] < dat_bin.freq) & (dat_bin.freq < freq_range[1]))
    x = dat_bin.freq[ifreq]
    y = dat_bin.Spec[0, uinds].mean(0) * pii
    y = y[ifreq]
    x_norm = (x * z) / U_hor
    y_norm = (y * U_hor) / (z * u_star)
    return x_norm, y_norm, x, y


for filename in FILENAMES:

    dat_bin = load_data(filename + '_binned')
    UINDS = [abs(dat_bin.u) < 0.5,
            (0.5 < abs(dat_bin.u)) & (abs(dat_bin.u) < 1.0),
            (1.0 < abs(dat_bin.u)) & (abs(dat_bin.u) < 1.5),
            (1.5 < abs(dat_bin.u)) & (abs(dat_bin.u) < 2.0),
            abs(dat_bin.u) > 2.0]
    UINDS_words = [' u less than 0.5 ',
                   ' u between 0.5 and 1.0 ',
                   ' u between 1.0 and 1.5 ',
                   ' u between 1.5 and 2.0 ',
                   ' u greater than 2.0 ']
    for indices, words in zip(UINDS, UINDS_words):
        uinds = indices
        freq_range = [0, 3]
        u_star, U_hor = def_vars(dat_bin, uinds)
        x_norm, y_norm, x, y = def_x_y(dat_bin, z, u_star, U_hor, uinds, freq_range)
        popt, pcov = scipy.optimize.curve_fit(function, x_norm, y_norm)
        print ("For" + words + " in the file " + filename + " the optimal values are " + str(popt))
        print popt

        fig = plt.figure(1, figsize=[8, 4])
        fig.clf()
        ax = fig.add_axes([.14, .14, .8, .74])

        # plot our data
        ax.loglog(x_norm, y_norm, 'b-')
        ax.set_autoscale_on(False)  # Otherwise, infinite loop

        y_theory = function(x_norm, popt[0], popt[1])
        ax.loglog(x_norm, y_theory, 'r-')
        ax.set_title(words + " for " + filename)

        fig.savefig('./figures/spectral_fits/u/' + filename + '_fit_' + words + '.png')
