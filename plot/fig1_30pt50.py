import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import uproot
import warnings
from functions import *

warnings.filterwarnings('ignore')

def getEff(pythiaFile, pythiaCuts):
    df = applyCut(addNewBranches(getData(observables, pythiaFile, treeName)),pythiaCuts)
    match_miss, _ = np.histogram(df[ob], range=(range_low,range_high), bins=bins, weights=df['w'])
    match, _ = np.histogram(df[(df.ms>1) & (df.pts>15)][ob], range=(range_low,range_high), bins=bins, weights=df[(df.ms>1) & (df.pts>15)]['w'])
    return match/(1e-50+match_miss)

def getFull(effFile, pythiaCuts, ofCsvPath, ofCuts, it, nom=False, filelist=None):
    if filelist is None:
        filelist = np.arange(0,6)
    df2s = []
    for i in filelist:
        df_temp = pd.read_csv(ofCsvPath+'jet_noweight.csv', low_memory=False)
        df_temp.eval('a=(m*m-mg*mg)/(pt*pt)',inplace=True)
        df_temp[df_temp.a<0.000001]['a'] = 0
        df_temp[['loga']] = np.log10(df_temp[['a']].replace(0, np.nan))
        df_temp.mask(df_temp.isna(),-4.1,inplace=True)
        df_temp['weight'] = pd.read_csv(ofCsvPath+'it'+str(it)+'_seed'+str(i)+'.csv', low_memory=False)
        df2s.append(applyCut(df_temp, ofCuts))
    y2s = []
    for i in range(0, len(filelist)):
        y2s.append(np.histogram(df2s[i][ob], range=(range_low,range_high), bins=bins, weights=df2s[i]['weight'], density=True)[0])
    y2 = np.average(y2s, axis=0)
    y2_err = np.std(y2s, axis=0)
    eff = getEff(effFile, pythiaCuts)
    y = y2/(1e-50+eff)
    y_err = y2_err/(1e-50+eff)
    norm = sum(y)
    y = y/norm
    y_err = y_err/norm
    if (nom==False):
        err_seed=0
    else:
        err_seed = y_err/(np.sqrt(len(filelist))) # use standard error
    return y, err_seed

def getFullStat(effFile, pythiaCuts, ofCsvPath, ofCuts, it, filelist=None):
    if filelist is None:
        filelist = np.arange(0,10)
    df2s = []
    for i in filelist:
        df_temp = pd.read_csv(ofCsvPath+'jet_noweight.csv', low_memory=False)
        df_temp.eval('a=(m*m-mg*mg)/(pt*pt)',inplace=True)
        df_temp[df_temp.a<0.000001]['a'] = 0
        df_temp[['loga']] = np.log10(df_temp[['a']].replace(0, np.nan))
        df_temp.mask(df_temp.isna(),-4.1,inplace=True)
        df_temp['weight'] = pd.read_csv(ofCsvPath+'it'+str(it)+'_statistic'+str(i)+'.csv', low_memory=False)
        df2s.append(applyCut(df_temp, ofCuts))
    y2s = []
    for i in range(0, len(filelist)):
        y2s.append(np.histogram(df2s[i][ob], range=(range_low,range_high), bins=bins, weights=df2s[i]['weight'], density=True)[0])
    y2 = np.average(y2s, axis=0)
    y2_err = np.std(y2s, axis=0)
    eff = getEff(effFile, pythiaCuts)
    y = y2/(1e-50+eff)
    y_err = y2_err/(1e-50+eff)
    norm = sum(y)
    err_stat = y_err/norm
    return err_stat

# set up PYTHIA6 embedding dataframe
observables = ['pt','m','q','rg','zg','mg','w','reject','pts','ms','qs','rgs','zgs','mgs','ws','rejects']
file = '/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root'
treeName = "MatchedTree"
df_py6 = applyCut(getData(observables, file, treeName), 'rg>0 and reject<=0 and rejects<=0 and w<5e-10')
df_py6 = addNewBranches(df_py6)

# set up HERWIG7 truth dataframe
observables_hw = ['q', 'qs', 'xsec','matching','pt','m','n','parton','mg','rg','zg','pts','ms','ns','partons','mgs','rgs','zgs', 'index','delta_r_1','delta_r_2','event_scale']
dataframes = []
files = ['/gpfs01/star/pwg/youqi/run12/mc/text/herwig_50pthat_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_45pthat50_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_40pthat45_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_35pthat40_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_30pthat35_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_25pthat30_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_20pthat25_1208.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/herwig_15pthat20_1208.txt']
for file in files:
    df = pd.read_csv(file, names=observables_hw, low_memory=False)
    df['w'] = np.ones(df.shape[0]) * (float)(df.iloc[df.shape[0]-1]['xsec'])/200000
    dataframes.append(df)
df = pd.concat([df for df in dataframes])
df = applyCut(df, 'rg>0')
df_hw = df[['pt','m','rg','zg','mg','w']]
df_hw = addNewBranches(df_hw)

# set up PYTHIA8 truth dataframe
observables_py8 = ['q05','q','q05s', 'qs', 'xsec','matching','pt','m','n','parton','mg','rg','zg','ng','pts','ms','ns','partons','mgs','rgs','zgs','ngs','index','delta_r_1','delta_r_2','event_scale']
dataframes = []
files = ['/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_50pthat.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_45pthat50.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_40pthat45.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_35pthat40.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_30pthat35.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_25pthat30.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_20pthat25.txt', \
         '/gpfs01/star/pwg/youqi/run12/mc/text/pythia1208_15pthat20.txt']
for file in files:
    df = pd.read_csv(file, names=observables_py8, low_memory=False)
    df['w'] = np.ones(df.shape[0]) * (float)(df.iloc[df.shape[0]-1]['xsec'])/200000
    dataframes.append(df)
df = pd.concat([df for df in dataframes])
df = applyCut(df, 'rg>0')
df_py8 = df[['pt','m','rg','zg','mg','w']]
df_py8 = addNewBranches(df_py8)

# set parameters for plotting
cut = '30<pt<50 and a>0.0000001'
ob = 'loga'
range_low = -4.
range_high = -0.
bins = 16
binwidth = (range_high - range_low)/bins
bins_mc = 32
binwidth_mc = (range_high - range_low)/bins_mc
it_mean = 5

# set midpoints for x-axis
x = np.arange(range_low+(range_high-range_low)/(2*bins),range_high+(range_high-range_low)/(2*bins), (range_high-range_low)/bins)
x_mc = np.arange(range_low+(range_high-range_low)/(2*bins_mc),range_high+(range_high-range_low)/(2*bins_mc), (range_high-range_low)/bins_mc)

# calculate y-values for MC curves
df_py6 = applyCut(df_py6, cut)
y_nom_truth, err_nom_truth = calc_hist(df_py6[ob], bins=np.arange(range_low, range_high+binwidth_mc, binwidth_mc), weights=df_py6['w'], density=True)[:2]
df_hw = applyCut(df_hw, cut)
y_hw_truth, err_hw_truth = calc_hist(df_hw[ob], bins=np.arange(range_low, range_high+binwidth_mc, binwidth_mc), weights=df_hw['w'], density=True)[:2]
df_py8 = applyCut(df_py8, cut)
y_py8_truth, err_py8_truth = calc_hist(df_py8[ob], bins=np.arange(range_low, range_high+binwidth_mc, binwidth_mc), weights=df_py8['w'], density=True)[:2]

# set paths to read MultiFold output from
nom_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/nominal/'
hadcorr_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/hadcorr05/'
tow_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/tow104/'
eff_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/eff096/'
hw_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/herwig/'
py8_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/pythia8/'
stat_path = '/gpfs01/star/pwg/youqi/run12/final/results/multifold_output/statistic/'

# calculate y-values for nominal and systematic uncertainty variations
y_nom, err_seed = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    nom_path, cut, it_mean, nom=True)
y_hadcorr = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched_hadcorr05.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    hadcorr_path, cut, it_mean)[0]
y_tow = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched_tow104.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    tow_path, cut, it_mean)[0]
y_eff = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched_eff096.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    eff_path, cut, it_mean)[0]
y_hw = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    hw_path, cut, it_mean)[0]
y_p8 = getFull('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    py8_path, cut, it_mean)[0]
err_stat = getFullStat('/gpfs01/star/pwg/youqi/run12/final/results/matched/matched.root',
    'rg!=-1 and reject<=0 and rejects<=0 and '+cut,
    stat_path, cut, it_mean)

# calculate systematic uncertainties
err1 = abs(np.array(y_nom/sum(y_nom))-np.array(y_hadcorr/sum(y_hadcorr)))
err2 = abs(np.array(y_nom/sum(y_nom))-np.array(y_tow/sum(y_tow)))
err3 = abs(np.array(y_nom/sum(y_nom))-np.array(y_eff/sum(y_eff)))
err4 = abs(np.array(y_nom/sum(y_nom))-np.array(y_hw/sum(y_hw)))
err5 = abs(np.array(y_nom/sum(y_nom))-np.array(y_p8/sum(y_p8)))
err6 = err_seed/sum(y_nom)
err_unf = []
for i in range(0,len(err4)):
    err_unf.append( np.sqrt( (max(abs(err4[i]),abs(err5[i])))**2 + (err6[i])**2 ) )
err_unf = np.array(err_unf)
err_sys = np.sqrt( err1**2 + err2**2 + err3**2 + err_unf**2 )

# make fig 1
fig, ax = plt.subplots()
plt.text(-2, 1.15, '$p+p$ $\sqrt{s}=200$ GeV\nanti-$k_T$ jets $R=0.4, |\eta|<0.6$', fontsize=12)
plt.text(-1.75, 1,'$30<p_T<50$ GeV/c', fontsize=15)
plt.errorbar(x, 4*y_nom/sum(y_nom), yerr=4*err_stat, capsize=3, color='darkred', markersize=11, ls='none')
line1, = plt.plot(x, 4*y_nom/sum(y_nom), label='STAR data', color='r', marker='*', markersize=11, ls='none')
line2 = plt.fill_between(x, 4*(y_nom/sum(y_nom)-err_sys), 4*(y_nom/sum(y_nom)+err_sys), color='r', alpha=0.15, label='Sys. Unc.')
l1 = ax.legend(handles=[line1,line2], frameon=False, loc='upper left', fontsize=12)
line3 = plt.errorbar(x_mc, 8*y_hw_truth/sum(y_hw_truth), yerr=8*err_hw_truth/sum(y_hw_truth), label='HERWIG7 7.2 Default', color='g', linestyle='--')
line4 = plt.errorbar(x_mc, 8*y_nom_truth/sum(y_nom_truth), yerr=8*err_nom_truth/sum(y_nom_truth), label='PYTHIA6 STAR tune', color='b', linestyle='--')
line5 = plt.errorbar(x_mc, 8*y_py8_truth/sum(y_py8_truth), yerr=8*err_py8_truth/sum(y_py8_truth), label='PYTHIA8 Detroit tune', color='k', linestyle='--')
l2 = ax.legend(handles=[line3, line4, line5], frameon=False, loc='upper right', fontsize=12)
ax.add_artist(l2)
plt.xlabel('$\log_{10}(a) = \log_{10}((M^2-M_g^2)/p_T^2)$', fontsize=15)
plt.ylabel(r'$1/N_{\mathrm{jet}}$ $d\log_{10}(N_{\mathrm{jet}})/d\log_{10}(a)$', fontsize=15)
plt.xlim(-3.5,-0.5)
plt.ylim(0,1.7)
plt.savefig('fig1_30pt50.png', bbox_inches='tight')