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

df1 = pd.DataFrame.from_csv('./csv_files/TTM_NREL03_May2015_results.csv')
a_u1 = df1['u_a']
b_u1 = df1['u_b']
a_v1 = df1['v_a']
b_v1 = df1['v_b']
a_w1 = df1['w_a']
b_w1 = df1['w_b']
mean_u1 = df1['mean_u']
mean_v1 = df1['mean_v']
mean_w1 = df1['mean_w']

df2 = pd.DataFrame.from_csv('./csv_files/TTM_NRELvector_Jun2012_results.csv')
a_u2 = df2['u_a']
b_u2 = df2['u_b']
a_v2 = df2['v_a']
b_v2 = df2['v_b']
a_w2 = df2['w_a']
b_w2 = df2['w_b']
mean_u2 = df2['mean_u']
mean_v2 = df2['mean_v']
mean_w2 = df2['mean_w']

df3 = pd.DataFrame.from_csv('./csv_files/TTM01b_ADVbottom_NREL01_June2014_results.csv')
a_u3 = df3['u_a']
b_u3 = df3['u_b']
a_v3 = df3['v_a']
b_v3 = df3['v_b']
a_w3 = df3['w_a']
b_w3 = df3['w_b']
mean_u3 = df3['mean_u']
mean_v3 = df3['mean_v']
mean_w3 = df3['mean_w']

df4 = pd.DataFrame.from_csv('./csv_files/TTM01_ADVtop_NREL02_June2014_results.csv')
a_u4 = df4['u_a']
b_u4 = df4['u_b']
a_v4 = df4['v_a']
b_v4 = df4['v_b']
a_w4 = df4['w_a']
b_w4 = df4['w_b']
mean_u4 = df4['mean_u']
mean_v4 = df4['mean_v']
mean_w4 = df4['mean_w']

df5 = pd.DataFrame.from_csv('./csv_files/TTM01_ADVbottom_NREL01_June2014_results.csv')
a_u5 = df5['u_a']
b_u5 = df5['u_b']
a_v5 = df5['v_a']
b_v5 = df5['v_b']
a_w5 = df5['w_a']
b_w5 = df5['w_b']
mean_u5 = df5['mean_u']
mean_v5 = df5['mean_v']
mean_w5 = df5['mean_w']

frames = [df1, df2, df3, df4, df5]
all = pd.concat(frames)


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

df = pd.DataFrame()
x_norms = []
y_norms = []
xs = []
ys = []
for filename in FILENAMES:
    dat_bin = load_data(filename + '_binned')
    uinds = abs(dat_bin.u) > 0.5
    freqinds = dat_bin.freq > 1
    u_star, U_hor = def_vars(dat_bin, uinds)
    x_norm, y_norm, x, y = def_x_y(dat_bin, z, u_star, U_hor, uinds, freqinds)
    x_norms.append(x_norm)
    y_norms.append(y_norm)
    xs.append(x)
    ys.append(y)

df['x_norm'] = x_norms
df['y_norm'] = y_norms
df['x'] = xs
df['y'] = ys