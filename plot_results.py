from process_data import load_data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dt

FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014']

pii = 2 * np.pi


def processed_plot(dat_raw, dat_screen, filename):
    """Plots processed/screened data over raw/unscreened data"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # Plot the raw (unscreened) data:
    ax.plot(dat_raw.mpltime, dat_raw.u, 'o-')
    ax.set_autoscale_on(False)  # Otherwise, infinite loop

    # Plot the screened data:
    ax.plot(dat_screen.mpltime, dat_screen.u, 'o-', rasterized=True)

    bads = np.abs(dat_screen.u - dat_raw.u[dat_raw.props['time_range']])
    ax.text(0.55, 0.95, (np.float(sum(bads > 0)) / len(bads) * 100),
            transform=ax.transAxes,
            va='top',
            ha='left',
            )

    ax.axvspan(dat_raw.mpltime[0], t_range[0], zorder=-10, facecolor='0.9', edgecolor='none')
    ax.text(0.13, 1.0, 'Mooring falling\ntoward seafloor', ha='center', va='top', transform=ax.transAxes, size='small')
    ax.text(0.3, 0.6, 'Mooring on seafloor', ha='center', va='top', transform=ax.transAxes, size='small')
    ax.annotate('', (0.25, 0.4), (0.4, 0.4), arrowprops=dict(facecolor='black'))
    ax.set_ylabel('$u\,\mathrm{[m/s]}$', size='large')
    ax.set_xlabel('Time')
    ax.set_title('Data cropping and cleaning')

    fig.savefig('./figures/' + filename + 'processed_plot.png')


def spectrum_plot(dat_bin, filename):
    """Plot the turbulence spectra"""
    fig = plt.figure(2, figsize=[6, 6])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])
    inds = dat_bin.u > 1.0
    ax.loglog(dat_bin.freq,
              dat_bin.Spec[0, inds].mean(0) * pii,
              'b-',
              label='motion corrected')
    ax.loglog(dat_bin.freq,
              dat_bin.Spec_velraw[0, inds].mean(0) * pii,
              'r-',
              label='no motion correction')
    ax.set_xlim([1e-3, 20])
    ax.set_ylim([1e-4, 1])
    ax.set_xlabel('frequency [hz]')
    ax.set_ylabel('$\mathrm{[m^2s^{-2}/hz]}$', size='large')
    f_tmp = np.logspace(-3, 1)
    ax.plot(f_tmp, 4e-5 * f_tmp ** (-5. / 3), 'k--')
    ax.set_title('Velocity Spectra')
    ax.legend()
    fig.savefig('./figures/' + filename + '_velocity_spectrum.png')


def tke_plot(dat_bin, filename):
    """Plots the Turbulent Kinetic Energy"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # first, convert the num_time to date_time, and plot this versus dat_raw.u
    date_time = dt.num2date(dat_bin.mpltime)

    # plot the data
    ax.plot(date_time, dat_bin.upup_, 'r-', rasterized=True)
    ax.plot(date_time, dat_bin.vpvp_, 'g-', rasterized=True)
    ax.plot(date_time, dat_bin.wpwp_, 'b-', rasterized=True)

    # label axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Turbulent Energy $\mathrm{[m^2/s^2]}$', size='large')

    fig.savefig('./figures/' + filename + '_tke_plot.png')


def reynolds_stress(dat_bin, filename):
    """Plots the Reynold's Stress"""
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])

    # first, convert the num_time to date_time, and plot this versus dat_raw.u
    date_time = dt.num2date(dat_bin.mpltime)

    # plot the data
    ax.plot(date_time, dat_bin.upvp_, 'r-', rasterized=True)
    ax.plot(date_time, dat_bin.upwp_, 'g-', rasterized=True)
    ax.plot(date_time, dat_bin.vpwp_, 'b-', rasterized=True)

    # label axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Reynolds Stresses $\mathrm{[m^2/s^2]}$', size='large')

    fig.savefig('./figures/' + filename + '_reynolds_plot.png')


for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    dat_screen = load_data(filename + '_processed')
    dat_raw = load_data(filename + '_raw')
    processed_plot(dat_raw, dat_screen, filename)
    spectrum_plot(dat_bin, filename)
    tke_plot(dat_bin, filename)
    reynolds_stress(dat_bin, filename)
