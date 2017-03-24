import pandas as pd
from process_data import load_data
import numpy as np
import dolfyn.adv.api as avm
import matplotlib.pyplot as plt
from os.path import isfile
import urllib2
import pyts.api as pyturb
import pyts.plot.api as pt

FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014']


def param_Vs_mean(x, a, b, filename, width):
    fig = plt.figure(1, figsize=[8, 4])
    fig.clf()
    ax = fig.add_axes([.14, .14, .8, .74])
    a = ax.bar(x + width, a, width)
    b = ax.bar(x, b, width)
    ax.legend([a, b], ["a", "b"])

    ax.set_ylabel('a_opt')
    ax.set_xlabel('mean_vel')
    ax.set_title('p_opts versus mean_vel')

    fig.savefig('./figures/analysis/' + filename + '.png')

for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    fname = './csv_files/' + filename + '_results.csv'
    df = pd.DataFrame.from_csv(fname)
    a_u = df['u_a']
    b_u = df['u_b']
    mean_u = df['mean_u']
    N_u = df['N_u']
    a_v = df['v_a']
    b_v = df['v_b']
    mean_v = df['mean_v']
    N_v = df['N_v']
    a_w = df['w_a']
    b_w = df['w_b']
    mean_w = df['mean_w']
    N_w = df['N_w']

    param_Vs_mean(mean_u, a_u, b_u,  filename + '_params_Vs_mean_u', .1)
    param_Vs_mean(mean_v, a_v, b_v,  filename + '_params_Vs_mean_v', .009)
    param_Vs_mean(mean_w, a_w, b_w, filename + '_params_Vs_mean_w', .01)





