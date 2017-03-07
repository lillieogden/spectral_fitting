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


def download_file(file_path, filename, url):
    """ Downloads the raw ADV file """
    # download the raw ADV file specified by the above path
    # ff the file exists...
    # ....as an '.h5' file, read it
    if os.path.isfile(file_path + '.h5'):
        dat_raw = avm.load(file_path + '.h5')
    # ....as a '.VEC' file, save it as an '.h5' and then read it using dolfyn library
    elif os.path.isfile(file_path + ',VEC'):
        dat_raw = avm.read_nortek(file_path + '.VEC')
        dat_raw.save(file_path + '.h5')
    # if the file does not exist as either a '.VEC' or '.h5', download it from the internet,
    #  save it as a '.h5' file and read it
    else:
        response = urllib2.urlopen(url)
        with open(filename, 'wb') as f:
            f.write(response.read())
        dat_raw = avm.read_nortek(f)
        dat_raw.save(file_path + '.h5')
    return dat_raw


def clean_correct(dat, dat_crop, accel_filter):
    """Cleans the raw data file and performs motion correction"""
    # then clean the file using the Goring+Nikora method:
    avm.clean.GN2002(dat)
    dat_cln = dat.copy()
    # then perform motion correction
    avm.motion.correct_motion(dat_crop, accel_filter)
    # rotate the uncorrected data into the earth frame, for comparison to motion correction:
    avm.rotate.inst2earth(dat_cln)
    # then rotate it into a 'principal axes frame':
    avm.rotate.earth2principal(dat_crop)
    avm.rotate.earth2principal(dat_cln)
    return dat_cln, dat_crop


def vel_spectra_plot(dat, dat_cln):
    """Plot the turbulence spectra"""
    # average the data and compute turbulence statistics
    dat_bin = avm.calc_turbulence(dat, n_bin=19200, n_fft=4096)
    dat_cln_bin = avm.calc_turbulence(dat_cln, n_bin=19200, n_fft=4096)
    fig = plt.figure(2, figsize=[6, 6])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])
    ax.loglog(dat_bin.freq, dat_bin.Suu_hz.mean(0), 'b-', label='motion corrected')
    ax.loglog(dat_cln_bin.freq, dat_cln_bin.Suu_hz.mean(0), 'r-', label='no motion correction')
    ax.set_xlim([1e-3, 20])
    ax.set_ylim([1e-4, 1])
    ax.set_xlabel('frequency [hz]')
    ax.set_ylabel('$\mathrm{[m^2s^{-2}/hz]}$', size='large')
    f_tmp = np.logspace(-3, 1)
    ax.plot(f_tmp, 4e-5 * f_tmp ** (-5. / 3), 'k--')
    ax.set_title('Velocity Spectra')
    ax.legend()
    plt.show()
    return plt


def main():
    """Runs the main program"""
    # user specifications for the raw ADV file
    file_path = '/Users/lillie/turbulence_data/raw_data/TTM_NREL03_May2015'
    # body2head_vec = np.array([9.75, 2, -5.75]) * 0.0254
    # body2head_rotmat = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])
    # x_start = .00835 + 7.3572944e5
    # x_end = .304 + 7.35731e5
    # t_range = [x_start, x_end]
    filename = 'TTM_NREL03_May2015.VEC'
    url = 'https://mhkdr.openei.org/files/51/TTM_NREL03_May2015.VEC'
    accel_filter = 0.1
    load_vec = True

    dat_raw = download_file(file_path, filename, url)

    # set the t_range inds based on the props attribute
    t_range_inds = (dat_raw.props.inds_range[0] < dat_raw.mpltime) & (dat_raw.mpltime < dat_raw.props.inds_range[1])
    dat_crop = dat_raw.subset(t_range_inds)
    dat = dat_raw.subset(t_range_inds)

    # clean the data and perform motion corretcion
    dat_cln, dat_crop = clean_correct(dat, dat_crop, accel_filter)

    # plot the velocity spectra
    vel_spectra = vel_spectra_plot(dat, dat_cln)

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

# run the program
main()
