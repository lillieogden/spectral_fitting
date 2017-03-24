import pandas as pd
from process_data import load_data
import matplotlib.pyplot as plt


def scatter(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, name):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(x1, y1, s=10, c='b', marker="s", label='TTM_NREL03_May2015')
    ax.scatter(x2, y2, s=10, c='r', marker="o", label='TTM_NRELvector_Jun2012')
    ax.scatter(x3, y3, s=10, c='g', marker="D", label='TTM01b_ADVbottom_NREL01_June2014')
    ax.scatter(x4, y4, s=10, c='y', marker="p", label='TTM01_ADVtop_NREL02_June2014')
    ax.scatter(x5, y5, s=10, c='m', marker="^", label='TTM01_ADVbottom_NREL01_June2014')

    ax.set_title( 'Popt vs Mean_vel for ' + name)
    plt.xlabel('Mean Velocity')
    plt.ylabel('Optimized Fit Parameter')
    plt.legend(loc='upper left')
    plt.show()

    fig.savefig('./figures/analysis/' + name + '.png')

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

scatter(mean_u1, a_u1, mean_u2, a_u2, mean_u3, a_u3, mean_u4, a_u4, mean_u5, a_u5, 'u_a')
scatter(mean_u1, b_u1, mean_u2, b_u2, mean_u3, b_u3, mean_u4, b_u4, mean_u5, b_u5, 'u_b')

scatter(mean_v1, a_v1, mean_v2, a_v2, mean_v3, a_v3, mean_v4, a_v4, mean_v5, a_v5, 'v_a')
scatter(mean_v1, b_v1, mean_v2, b_v2, mean_v3, b_v3, mean_v4, b_v4, mean_v5, b_v5, 'v_b')

scatter(mean_w1, a_w1, mean_w2, a_w2, mean_w3, a_w3, mean_w4, a_w4, mean_w5, a_w5, 'w_a')
scatter(mean_w1, b_w1, mean_w2, b_w2, mean_w3, b_w3, mean_w4, b_w4, mean_w5, b_w5, 'w_b')

