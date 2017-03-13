from process_data import load_data


FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014']


def vel_spectra_plot(filename):
    """Plot the turbulence spectra"""
    dat_bin = load_data(filename, binned=True)

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
    fig.savefig('./figure/' + filename + '_spectra.png')

