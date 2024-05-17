import math
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from functions import *

warnings.filterwarnings('ignore')

def weighted_avg_and_std(values, weights):
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)
    return (average, math.sqrt(variance))

def func(x, te):
    return 1/2 * (1-np.sqrt(1- 2/(te * (1-np.cos(x)))))

# set binning
rgedges=np.arange(0.,0.45,0.05)
zgedges=np.arange(0.1,0.55,0.05)

# set parameters
path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/'
cut = '20<pt<30 and rg!=-1'
it = 5

# create an array of DataFrames for unfolded matched jets
df2s = []
for i in [0]:
#for i in range(1,21):
    df_temp = pd.read_csv(path+'jet_noweight.csv', low_memory=False)
    df_temp.eval('a=(m*m-mg*mg)/(pt*pt)',inplace=True)
    df_temp['weight'] = pd.read_csv(path+'it'+str(it)+'_seed'+str(i)+'.csv', low_memory=False)
    df2s.append(applyCut(df_temp, cut))

# find the average weight for each jet for the array of DataFrames (for unfolded matched jets)
w = []
for i in range(0, len(df2s)):
    w.append(np.asarray(df2s[i]['weight']))
w_avg=np.average(w,axis=0)
w_std=np.std(w,axis=0)

# create a DataFrame df2 which is the average of the array of DataFrames (for unfolded matched jets)
df2 = df2s[0]
df2['w_avg'] = w_avg
df2 = addNewBranches(df2)

# calculate z-values for each bin with df2
z2 = np.zeros((len(rgedges)-1, len(zgedges)-1))
for i in range(0, len(rgedges)-1):
    for j in range(0, len(zgedges)-1):
        df_temp = df2[(df2.rg>rgedges[i]) & (df2.rg<=rgedges[i+1]) & (df2.zg>zgedges[j]) & (df2.zg<=zgedges[j+1])]
        avg, err = weighted_avg_and_std(df_temp['a'], weights=df_temp['w_avg'])
        z2[i][j] = avg

# create a DataFrame df1 for missed jets
observables = ['pt','m','q','rg','zg','mg','w','reject','pts','ms','qs','rgs','zgs','mgs','ws','rejects']
file = '/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root'
treeName = "MatchedTree"
df1 = applyCut(getData(observables, file, treeName), cut+' and reject<=0 and rejects<=0 and w<5e-10 and (pts<15 or ms<1)')
df1 = addNewBranches(df1)

# calculate z-values for each bin with df1
z1 = np.zeros((len(rgedges)-1, len(zgedges)-1))
for i in range(0, len(rgedges)-1):
    for j in range(0, len(zgedges)-1):
        df_temp = df1[(df1.rg>rgedges[i]) & (df1.rg<=rgedges[i+1]) & (df1.zg>zgedges[j]) & (df1.zg<=zgedges[j+1])]
        avg, err = weighted_avg_and_std(df_temp['a'], weights=df_temp['w'])
        z1[i][j] = avg

# calculate efficiency for each bin
df_truth = applyCut(getData(observables, file, treeName), cut+' and reject<=0 and rejects<=0 and w<5e-10')
match_miss = np.histogram2d(df_truth['rg'],df_truth['zg'], bins=[rgedges,zgedges], weights=df_truth['w'])[0]
match = np.histogram2d(df_truth[(df_truth.ms>1) & (df_truth.pts>15)]['rg'], df_truth[(df_truth.ms>1) & (df_truth.pts>15)]['zg'], bins=[rgedges,zgedges], weights=df_truth[(df_truth.ms>1) & (df_truth.pts>15)]['w'])[0]
eff = match/match_miss

# calculate values of constant formation time
x0 = np.arange(0.,0.401,0.001)
y0 = func(x0,50)
x1 = np.arange(0.,0.401,0.001)
y1 = func(x1,200)
x2 = np.arange(0.,0.401,0.001)
y2 = func(x2,800)

# make fig 2
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = '15'
fig = plt.figure(figsize=(6,5))
ax = plt.gca()
plt.pcolormesh(rgedges, zgedges, np.transpose(eff*z2+(1-eff)*z1), cmap='seismic')
ax.tick_params(top=True, right=True, bottom=True, left=True, direction='in', which='both', labelcolor='k')
plt.ylabel(r'$z_g$')
plt.xlabel(r'$R_g$')
plt.clim(0,0.02)
plt.ylim(0.,0.5)
plt.plot(x0,y0, color='white')
plt.plot(x1,y1, color='k')
plt.plot(x2,y2, color='k')
cbar = plt.colorbar()
for l in cbar.ax.yaxis.get_ticklabels():
    l.set_family("serif")
cbar.set_label(r'$(M^2-M_g^2)/p_T^2$',font='arial',fontsize=20)
plt.savefig('fig2.png', bbox_inches='tight')