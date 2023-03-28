#%%
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

sns.set(font_scale=1, rc={'text.usetex' : True,
                          'text.latex.preamble': r'\usepackage[charter]{mathdesign}',
                          'font.family':['serif'],
                          'font.size': 10,
                          'figure.dpi': 300},
                          color_codes=True)
sns.set_style('white')

#%%
def slopes_test(b1,b2,sb1,sb2,n1,n2) -> str:
    t = abs((b1-b2)/(((sb1**2)+(sb2**2))**(1/2)))
    gl = n1+n2-4
    p = (1-stats.t(gl).cdf(t))*2
    return f'Valor t: {t}, graus de liberdade: {gl}, probabilidade: {p}'

#%%
df = pd.read_csv('SYNEDATA.csv', sep=';')
df = df.loc[df['id'] != 'L']
df['day'] = [int(x.replace('h','')) for x in df['day']]
df['total'] = [x+y for x,y in zip(df['aml'], df['uml'])]

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
            palette=('Dark2')).set(title='Controle\nA')

X = CA['hora'].loc[CA['classe'] == 'agregado']
y = CA['unid./mL'].loc[CA['classe'] == 'agregado']
slope_agg_CA, intercept, r_value, p_value, std_err_agg_CA = stats.linregress(X,y)
plt.text(51, 82000, f'y = {str(round(slope_agg_CA,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_CA,2))}')


print(r_value**2)

X = CA['hora'].loc[CA['classe'] == 'não agregado']
y = CA['unid./mL'].loc[CA['classe'] == 'não agregado']
slope_uni_CA, intercept, r_value, p_value, std_err_uni_CA = stats.linregress(X,y)
plt.text(51, 295000, f'y = {str(round(slope_uni_CA,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_CA,2))}')

print(r_value**2)

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%
CB = table.loc[(df['id'] == 'CB')]

g = sns.lmplot(x='hora', y='unid./mL', hue='classe', data=CB,
            x_estimator=np.mean, 
            hue_order=['não agregado','agregado'],
            palette=('Dark2')).set(title='Controle\nB')

X = CB['hora'].loc[CB['classe'] == 'agregado']
y = CB['unid./mL'].loc[CB['classe'] == 'agregado']
slope_agg_CB, intercept, r_value, p_value, std_err_agg_CB = stats.linregress(X,y)
plt.text(51, 44000, f'y = {str(round(slope_agg_CB,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_CB,2))}')

print(r_value**2)

X = CB['hora'].loc[CB['classe'] == 'não agregado']
y = CB['unid./mL'].loc[CB['classe'] == 'não agregado']
slope_uni_CB, intercept, r_value, p_value, std_err_uni_CB = stats.linregress(X,y)
plt.text(51, 237000, f'y = {str(round(slope_uni_CB,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_CB,2))}')

print(r_value**2)

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%
Q = table.loc[(df['id'] == 'Q')]

g = sns.lmplot(x='hora', y='unid./mL', hue='classe', data=Q,
            x_estimator=np.mean,
            hue_order=['não agregado','agregado'],
            palette=('Dark2')).set(title='Químico')

X = Q['hora'].loc[Q['classe'] == 'agregado']
y = Q['unid./mL'].loc[Q['classe'] == 'agregado']
slope_agg_Q, intercept, r_value, p_value, std_err_agg_Q = stats.linregress(X,y)
plt.text(51, 44000, f'y = {str(round(slope_agg_Q,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_agg_Q,2))}')

print(r_value**2)

X = Q['hora'].loc[Q['classe'] == 'não agregado']
y = Q['unid./mL'].loc[Q['classe'] == 'não agregado']
slope_uni_Q, intercept, r_value, p_value, std_err_uni_Q = stats.linregress(X,y)
plt.text(51, 210000, f'y = {str(round(slope_uni_Q,2))}x + {str(round(intercept,2))}\
        \nerro padrão: {str(round(std_err_uni_Q,2))}')

print(r_value**2)

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%agg comparison
agg = table.loc[(table['classe'] == 'agregado')]

g = sns.lmplot(x='hora', y='unid./mL', hue='id', data=agg,
            x_estimator=np.mean,
            hue_order=['CA','Q','CB'],
            palette='plasma',
            markers=['x', '*', 'o']).set(title='Agregados')

g.set_ylabels(rotation=0)
sns.despine()
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 1.01)

#%%uni comparison
uni = table.loc[(table['classe'] == 'não agregado')]

g = sns.lmplot(x='hora', y='unid./mL', hue='id', data=uni,
            x_estimator=np.mean,
            hue_order=['CA','Q','CB'],
            palette='Greens_r',
            markers=['x', '*', 'o']).set(title='Não-agregados')

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

sns.lineplot(x='id',y='ratio', data=hour_0,
             estimator='mean', marker='o',
             err_style='bars', linestyle='',
             color='gray')\
                .set(xlabel='tratamento', 
                     ylabel='razão', title='Hora 0')

diffs = ['a','a','b']
loop_x = [.435, .4135, .4655]
y = .03
for label, x in zip(diffs, loop_x):
    plt.annotate(label, (y, x))
    y += 1

#%% 24h
hour_24 = ratio_table.loc[ratio_table['day'] == 24]
CA = hour_24.loc[hour_24['id'] == 'CA']['ratio']
CB = hour_24.loc[hour_24['id'] == 'CB']['ratio']
Q = hour_24.loc[hour_24['id'] == 'Q']['ratio']

print(stats.shapiro(CA), stats.shapiro(CB), stats.shapiro(Q))
print(stats.f_oneway(CA, CB, Q))
print(stats.tukey_hsd(CA, CB, Q))

sns.lineplot(x='id',y='ratio', data=hour_24,
             estimator='mean', marker='o',
             err_style='bars', linestyle='',
             color='gray')\
                .set(xlabel='tratamento', 
                     ylabel='razão', title='Hora 24')

diffs = ['a','b','b']
loop_x = [.365, .276, .297]
y = .03
for label, x in zip(diffs, loop_x):
    plt.annotate(label, (y, x))
    y += 1

#%% 48h
hour_48 = ratio_table.loc[ratio_table['day'] == 48]
CA = hour_48.loc[hour_48['id'] == 'CA']['ratio']
CB = hour_48.loc[hour_48['id'] == 'CB']['ratio']
Q = hour_48.loc[hour_48['id'] == 'Q']['ratio']

print(stats.shapiro(CA), stats.shapiro(CB), stats.shapiro(Q))
print(stats.f_oneway(CA, CB, Q))
print(stats.tukey_hsd(CA, CB, Q))

sns.lineplot(x='id',y='ratio', data=hour_48,
             estimator='mean', marker='o',
             err_style='bars', linestyle='',
             color='gray')\
                .set(xlabel='tratamento', 
                     ylabel='razão', title='Hora 48')

diffs = ['a','b','ab']
loop_x = [.303, .213, .231]
y = .025
for label, x in zip(diffs, loop_x):
    plt.annotate(label, (y, x))
    y += 1

print(np.mean(Q))

#%%
total = df[['id', 'day', 'total']]
total['day'] = [f'{x}h' for x in total['day']]
total

g = sns.catplot(
    data=total, kind='bar',
    x='id', y='total', hue='day',
    errorbar='se', palette='gray_r', alpha=.6, height=6
).set(title='Total')

g.despine(left=True)
g.set_axis_labels('tratamento', 'unidades/mL')
g.legend.set_title('')

# plt.ylim(0,450000)
g.set_ylabels(rotation=0)
axes = g.axes.flatten()
axes[0].yaxis.set_label_coords(-.1, 0.93)


CA = total.loc[total['id'] == 'CA']
CA_0 = CA.loc[CA['day'] == '0h']['total']
CA_24 = CA.loc[CA['day'] == '24h']['total']
CA_48 = CA.loc[CA['day'] == '48h']['total']

print(stats.shapiro(CA_0), stats.shapiro(CA_24), stats.shapiro(CA_48))
_, p_CA = stats.f_oneway(CA_0, CA_24, CA_48)
# print(stats.tukey_hsd(CA_0, CA_24, CA_48))

CB = total.loc[total['id'] == 'CB']
CB_0 = CB.loc[CB['day'] == '0h']['total']
CB_24 = CB.loc[CB['day'] == '24h']['total']
CB_48 = CB.loc[CB['day'] == '48h']['total']

print(stats.shapiro(CB_0), stats.shapiro(CB_24), stats.shapiro(CB_48))
_, p_CB = stats.f_oneway(CB_0, CB_24, CB_48)
# print(stats.tukey_hsd(CB_0, CB_24, CB_48))

Q = total.loc[total['id'] == 'Q']
Q_0 = Q.loc[Q['day'] == '0h']['total']
Q_24 = Q.loc[Q['day'] == '24h']['total']
Q_48 = Q.loc[Q['day'] == '48h']['total']

print(stats.shapiro(Q_0), stats.shapiro(Q_24), stats.shapiro(Q_48))
_, p_Q = stats.f_oneway(Q_0, Q_24, Q_48)

print(f'Valores p: CA = {p_CA}, CB = {p_CB}, Q = {p_Q}')