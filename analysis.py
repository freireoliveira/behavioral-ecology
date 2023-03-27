#%%
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt

sns.set(font_scale=1, rc={'text.usetex' : True,
                          'text.latex.preamble': r'\usepackage[charter]{mathdesign}',
                          'font.family':['serif'],
                          'font.size': 10,
                          'figure.dpi': 300})
sns.set_style('white')

#%%
def slopes_test(b1,b2,sb1,sb2,n1,n2) -> str:
    t = abs((b1-b2)/(math.sqrt((sb1**2)+(sb2**2))))
    gl = n1+n2-4
    p = (1-stats.t(gl).cdf(t))*2
    return f'Valor t: {t}, graus de liberdade: {gl}, probabilidade: {p}'

#%%
df = pd.read_csv('SYNEDATA.csv', sep=';')
df = df.loc[df['id'] != 'L']

day_dict = {
    '0h': 0,
    '24h': 24,
    '48h': 48
}

for key in day_dict.keys():
    df['day'] = df['day'].replace(key, day_dict[key])

df

#%%
df1 = df[['id', 'day', 'aml']]
df1['classe'] = ['agregado' for x in range(len(df1))]
df1.columns = ['id', 'hora', 'unid./mL', 'classe']
df2 = df[['id', 'day', 'uml']]
df2['classe'] = ['não agregado' for x in range(len(df1))]
df2.columns = ['id', 'hora', 'unid./mL', 'classe']
table = pd.concat([df1, df2])
table

#%%
CA = table.loc[(df['id'] == 'CA')]

g = sns.lmplot(x='hora', y='unid./mL', hue='classe', data=CA,
            x_estimator=np.mean,
            hue_order=['não agregado','agregado'],
            palette=('cubehelix')).set(title='Controle\nA')

X = CA['hora'].loc[CA['classe'] == 'agregado']
y = CA['unid./mL'].loc[CA['classe'] == 'agregado']
slope_agg_CA, intercept, r_value, p_value, std_err_agg_CA = stats.linregress(X,y)
plt.text(51, 82000, f'y = {str(round(slope_agg_CA,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_CA,2))}')

X = CA['hora'].loc[CA['classe'] == 'não agregado']
y = CA['unid./mL'].loc[CA['classe'] == 'não agregado']
slope_uni_CA, intercept, r_value, p_value, std_err_uni_CA = stats.linregress(X,y)
plt.text(51, 295000, f'y = {str(round(slope_uni_CA,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_CA,2))}')

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%
CB = table.loc[(df['id'] == 'CB')]

g = sns.lmplot(x='hora', y='unid./mL', hue='classe', data=CB,
            x_estimator=np.mean, palette=("flare")).set(title='Controle\nB')

X = CB['hora'].loc[CB['classe'] == 'agregado']
y = CB['unid./mL'].loc[CB['classe'] == 'agregado']
slope_agg_CB, intercept, r_value, p_value, std_err_agg_CB = stats.linregress(X,y)
plt.text(51, 44000, f'y = {str(round(slope_agg_CB,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_CB,2))}')

X = CB['hora'].loc[CB['classe'] == 'não agregado']
y = CB['unid./mL'].loc[CB['classe'] == 'não agregado']
slope_uni_CB, intercept, r_value, p_value, std_err_uni_CB = stats.linregress(X,y)
plt.text(51, 237000, f'y = {str(round(slope_uni_CB,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_CB,2))}')

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%
Q = table.loc[(df['id'] == 'Q')]

g = sns.lmplot(x='hora', y='unid./mL', hue='classe', data=Q,
            x_estimator=np.mean, palette=('rocket')).set(title='Químico')

X = Q['hora'].loc[Q['classe'] == 'agregado']
y = Q['unid./mL'].loc[Q['classe'] == 'agregado']
slope_agg_Q, intercept, r_value, p_value, std_err_agg_Q = stats.linregress(X,y)
plt.text(51, 44000, f'y = {str(round(slope_agg_Q,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_Q,2))}')

X = Q['hora'].loc[Q['classe'] == 'não agregado']
y = Q['unid./mL'].loc[Q['classe'] == 'não agregado']
slope_uni_Q, intercept, r_value, p_value, std_err_uni_Q = stats.linregress(X,y)
plt.text(51, 210000, f'y = {str(round(slope_uni_Q,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_Q,2))}')

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%% Q/CA agg
slopes_test(b1=slope_agg_Q, b2=slope_agg_CA, sb1=std_err_agg_Q,sb2=std_err_agg_CA,n1=3,n2=3)

#%% Q/CB agg
slopes_test(b1=slope_agg_Q, b2=slope_agg_CB, sb1=std_err_agg_Q,sb2=std_err_agg_CB,n1=3,n2=3)

#%% CA/CB agg
slopes_test(b1=slope_agg_CA, b2=slope_agg_CB, sb1=std_err_agg_CA,sb2=std_err_agg_CB,n1=3,n2=3)

#%% Q/CA nao agg
slopes_test(b1=slope_uni_Q, b2=slope_uni_CA, sb1=std_err_uni_Q,sb2=std_err_uni_CA,n1=3,n2=3)

#%% Q/CB nao agg
slopes_test(b1=slope_uni_Q, b2=slope_uni_CB, sb1=std_err_uni_Q,sb2=std_err_uni_CB,n1=3,n2=3)

#%% CA/CB nao agg
slopes_test(b1=slope_uni_CA, b2=slope_uni_CB, sb1=std_err_uni_CA,sb2=std_err_uni_CB,n1=3,n2=3)

#%%
ratio_table = df[['id', 'day', 'ratio']]
ratio_table

#%% 0h
hour_0 = ratio_table.loc[ratio_table['day'] == 0]
CA = hour_0.loc[hour_0['id'] == 'CA']['ratio']
CB = hour_0.loc[hour_0['id'] == 'CB']['ratio']
Q = hour_0.loc[hour_0['id'] == 'Q']['ratio']

print(stats.shapiro(CA), stats.shapiro(CB), stats.shapiro(Q))
print(stats.f_oneway(CA, CB, Q))
print(stats.tukey_hsd(CA, CB, Q))

# fig, ax = plt.subplots(1, 1)
# ax.boxplot([CA, CB, Q])
# ax.set_xticklabels(["group0", "group1", "group2"]) 
# ax.set_ylabel("mean") 
# plt.show()

#%% 24h
hour_24 = ratio_table.loc[ratio_table['day'] == 24]
CA = hour_24.loc[hour_24['id'] == 'CA']['ratio']
CB = hour_24.loc[hour_24['id'] == 'CB']['ratio']
Q = hour_24.loc[hour_24['id'] == 'Q']['ratio']

print(stats.shapiro(CA), stats.shapiro(CB), stats.shapiro(Q))
print(stats.f_oneway(CA, CB, Q))
print(stats.tukey_hsd(CA, CB, Q))

#%% 48h
hour_48 = ratio_table.loc[ratio_table['day'] == 48]
CA = hour_48.loc[hour_48['id'] == 'CA']['ratio']
CB = hour_48.loc[hour_48['id'] == 'CB']['ratio']
Q = hour_48.loc[hour_48['id'] == 'Q']['ratio']

print(stats.shapiro(CA), stats.shapiro(CB), stats.shapiro(Q))
print(stats.f_oneway(CA, CB, Q))
print(stats.tukey_hsd(CA, CB, Q))

