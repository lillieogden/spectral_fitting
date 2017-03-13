import numpy as np
import dolfyn.adv.api as avm
# import dolfyn.adv.turbulence as turb
import matplotlib.pyplot as plt
# import matplotlib.dates as dt
# import matplotlib.ticker as mtick
import os.path
import urllib2

import pyts.api as pyturb
# import pyts.specModels
import pyts.plot.api as pt
# from pyts.specModels.hydro import specModelBase, np, specObj, ts_float

pii = 2 * np.pi


def load_vec(filename, url):
    """Load ``filename``. If it doesn't exist, the file is
    downloaded from ``url``.
    """
    # download the raw ADV file specified by the above path
    # ff the file exists...
    # ....as an '.h5' file, read it
    filename = './data_cache/' + filename.rstrip('.VEC')
    if os.path.isfile(filename + '.h5'):
        dat_raw = avm.load(filename + '.h5')
    # ....as a '.VEC' file, save it as an '.h5' and then read it using dolfyn library
    elif os.path.isfile(filename + '.VEC'):
        dat_raw = avm.read_nortek(filename + '.VEC')
        dat_raw.save(filename + '.h5')
    # if the file does not exist as either a '.VEC' or '.h5', download it from the internet,
    #  save it as a '.h5' file and read it
    else:
        response = urllib2.urlopen(url)
        with open(filename + '.VEC', 'wb') as f:
            f.write(response.read())
        dat_raw = avm.read_nortek(filename + '.VEC')
        dat_raw.save(filename + '.h5')
    return dat_raw


def clean_correct(dat, accel_filter):
    """Cleans the raw data file and performs motion correction"""
    # clean the data using the Goring+Nikora method:
    avm.clean.GN2002(dat)
    # then perform motion correction
    avm.motion.correct_motion(dat, accel_filter)
    avm.rotate.earth2principal(dat)
    return


def vel_spectra_plot(dat):
    """Plot the turbulence spectra"""
    # average the data and compute turbulence statistics
    binner = avm.TurbBinner(n_bin=19200, fs=dat.fs, n_fft=19200)
    dat_bin = binner(dat)
    dat_bin.add_data('Spec_velraw', binner.psd(dat['velraw']), 'spec')
    fig = plt.figure(2, figsize=[6, 6])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])
    inds = dat_bin.u > 1.0
    ax.loglog(dat_bin.freq, dat_bin.Spec[0, inds].mean(0) * pii, 'b-',
              label='motion corrected')
    ax.loglog(dat_bin.freq, dat_bin.Spec_velraw[0, inds].mean(0) * pii, 'r-',
              label='no motion correction')
    ax.set_xlim([1e-3, 20])
    ax.set_ylim([1e-4, 1])
    ax.set_xlabel('frequency [hz]')
    ax.set_ylabel('$\mathrm{[m^2s^{-2}/hz]}$', size='large')
    f_tmp = np.logspace(-3, 1)
    ax.plot(f_tmp, 4e-5 * f_tmp ** (-5. / 3), 'k--')
    ax.set_title('Velocity Spectra')
    ax.legend()
    return dat_bin


def main():
    """Runs the main program"""
    filename = 'TTM_NREL03_May2015.VEC'
    url = 'https://mhkdr.openei.org/files/51/TTM_NREL03_May2015.VEC'
    accel_filter = 0.03

    dat_raw = load_vec(filename, url)

    # set the t_range inds based on the props attribute
    t_range_inds = ((dat_raw.props['inds_range'][0] < dat_raw.mpltime) &
                    (dat_raw.mpltime < dat_raw.props['inds_range'][1]))
    dat = dat_raw.subset(t_range_inds)

    # clean the data and perform motion corretcion
    clean_correct(dat, accel_filter)

    # plot the velocity spectra
    dat_bin = vel_spectra_plot(dat)

    # begin work with PyTurbSim
    # define some variables
    refht = 10.
    ustar = 0.03
    Uref = 3
    # initialize a run object
    tsr = pyturb.tsrun()
    # define the grid
    tsr.grid = pyturb.tsGrid(center=refht, ny=5, nz=5, height=5, width=9, time_sec=1000, dt=0.5)
    # define a mean profile and assign it to the run object
    prof_model = pyturb.profModels.h2l(Uref, refht, ustar)
    tsr.profModel = prof_model
    # define and assign a 'spectral model', 'coherence model', and 'stress model' to the run object:
    tsr.specModel = pyturb.specModels.tidal(ustar, refht)
    tsr.cohere = pyturb.cohereModels.nwtc()
    tsr.stress = pyturb.stressModels.tidal(ustar, refht)
    # call the run object to produce the pyturbsim output
    turbsim_output = tsr()
    # create a pyturbsim summary plotting figure
    fig = pt.summfig()
    # plot pyturbsim output
    fig.plot(turbsim_output, color='k')
    fig.plot(tsr, color='r', linestyle='--')
    fig.finalize()
    return dat, dat_bin

# run the program
dat, dat_bin = main()
