import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import (get_data, calc_hist, get_rc_and_err, get_rc_and_err_new)

EMB_FILE   = '/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.root'
EMB_CSV    = '/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.csv'
COLUMNS    = ['pt', 'b', 'w', 'y1', 'y2', 'phi1', 'phi2', 'mcevi',
              'pts', 'bs', 'ws', 'y1s', 'y2s', 'phi1s', 'phi2s', 'nefs']
PT_EDGES   = [15, 20, 25, 30, 40, 60]
PT_CENTERS = [17.5, 22.5, 27.5, 35, 50]
PT_XERR    = [2.5, 2.5, 2.5, 5, 10]
B_BINS     = np.array([-1.2, 0.0, 1.2])

plt.rcParams['font.size']          = 15
plt.rcParams['font.family']        = 'arial'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi']        = 120


def bin_df_in_pts(df, col='pts'):
    return [df[(df[col] > PT_EDGES[i]) & (df[col] < PT_EDGES[i+1])] for i in range(5)]

def delta_phi(a, b):
    diff = np.abs(a - b)
    return np.minimum(diff, 2 * np.pi - diff)

def get_rc_and_err_arr(df_arr, ob):
    rc_arr, err_arr = [], []
    for df in df_arr:
        rc, err = get_rc_and_err(df, ob)
        rc_arr.append(rc)
        err_arr.append(err)
    return rc_arr, err_arr

def get_rc_and_err_new_arr(df_arr, ob):
    rc_arr, err_arr = [], []
    for df in df_arr:
        rc, err = get_rc_and_err_new(df, ob)
        rc_arr.append(rc)
        err_arr.append(err)
    return rc_arr, err_arr

# 3-return variant
def _get_rc_p(df, ob):
    if ob == 'b':
        nos, nss = sum(df[df.b == -1]['w']),  sum(df[df.b == +1]['w'])
    elif ob == 'b_ch':
        nos, nss = sum(df[df.b_ch == -1]['w']), sum(df[df.b_ch == +1]['w'])
    elif ob == 'bs':
        nos, nss = sum(df[df.bs == -1]['ws']), sum(df[df.bs == +1]['ws'])
    else:
        raise ValueError(f"Unknown observable '{ob}'")
    rc = (nss - nos) / (nss + nos)
    p_final = nss / (nss + nos)
    w_array = np.unique(df['w'])
    err2_array = []
    for w_i in w_array:
        mask = df.w == w_i
        if ob == 'b':
            p = sum(df[mask & (df.b == +1)]['w'])  / sum(df[mask]['w'])
        elif ob == 'b_ch':
            p = sum(df[mask & (df.b_ch == +1)]['w']) / sum(df[mask]['w'])
        elif ob == 'bs':
            p = sum(df[mask & (df.bs == +1)]['w'])  / sum(df[mask]['ws'])
        variance = p * (1 - p) / df[mask].shape[0]
        w = sum(df[mask]['w']) / sum(df['w'])
        err2_array.append(w**2 * variance)
    rc_err = 2 * np.sqrt(sum(err2_array))
    return rc, rc_err, p_final


# One-time: load from ROOT, compute distances, save to CSV
# df_all = get_data(COLUMNS, EMB_FILE, 'MatchedTree').copy()
# dphi1 = delta_phi(df_all['phi1'].values, df_all['phi1s'].values)
# dphi2 = delta_phi(df_all['phi2'].values, df_all['phi2s'].values)
# df_all['distance1'] = np.sqrt(dphi1**2 + (df_all['y1'].values - df_all['y1s'].values)**2)
# df_all['distance2'] = np.sqrt(dphi2**2 + (df_all['y2'].values - df_all['y2s'].values)**2)
# df_all.to_csv(EMB_CSV, index=False)

# Normal path: load from CSV
df_all = pd.read_csv(EMB_CSV, low_memory=False)
print("read pre-saved csv")

df1_all = df_all[df_all['mcevi'] % 2 == 1]
df2_all = df_all[df_all['mcevi'] % 2 == 0]
print("number of jets in samples 1 and 2 (unweighted):", df1_all.shape[0], df2_all.shape[0])

df1_allreco  = df1_all.query('pts>15 and bs!=-9 and w<1')
df2_allreco  = df2_all.query('pts>15 and bs!=-9 and w<1')
df1_alltruth = df1_all.query('pt>5 and b!=-9 and w<1')
df2_alltruth = df2_all.query('pt>5 and b!=-9 and w<1')

df1_match   = df1_allreco.query('pt!=-9 and b!=-9 and distance1<0.02 and distance2<0.02')
df1_allfake = df1_allreco.query('pt==-9 or b==-9 or distance1>0.02 or distance2>0.02')
df2_match   = df2_allreco.query('pt!=-9 and b!=-9 and distance1<0.02 and distance2<0.02')
df2_allfake = df2_allreco.query('pt==-9 or b==-9 or distance1>0.02 or distance2>0.02')

# Process sample 1
df1_allreco_pts = bin_df_in_pts(df1_allreco)
df1_match_pts   = bin_df_in_pts(df1_match)
df1_allfake_pts = bin_df_in_pts(df1_allfake)

rc1_allreco, err1_allreco = get_rc_and_err_arr(df1_allreco_pts, 'bs')
rc1_match,   err1_match   = get_rc_and_err_arr(df1_match_pts,   'bs')
rc1_allfake, err1_allfake = get_rc_and_err_arr(df1_allfake_pts, 'bs')

fig, ax = plt.subplots(figsize=(5, 5))
ax.errorbar(PT_CENTERS, rc1_allfake, xerr=PT_XERR, yerr=err1_allfake, capsize=3, color='b', ls='none', label='mistagged')
ax.errorbar(PT_CENTERS, rc1_allreco, xerr=PT_XERR, yerr=err1_allreco, capsize=3, color='k', ls='none', label='matched + mistagged')
ax.errorbar(PT_CENTERS, rc1_match,   xerr=PT_XERR, yerr=err1_match,   capsize=3, color='r', ls='none', label='matched')
ax.set_xlabel(r'full jet reco $p_{\mathrm{T}}$ [GeV]')
ax.set_title('sample 1')
ax.axhline(0.0, color='grey', linestyle='--')
ax.set_ylabel(r'reco charged jet $r_c$')
ax.set_ylim(-0.6, 0.1)
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()

b1_fake_array, b1_err_fake_array = [], []
for df_f in df1_allfake_pts:
    y, yerr, _ = calc_hist(df_f['bs'], bins=B_BINS, weights=df_f['ws'], density=True)
    b1_fake_array.append(y / sum(y))
    b1_err_fake_array.append(yerr / sum(y))

b1_match_array, b1_err_match_array = [], []
for df_m in df1_match_pts:
    y, yerr, _ = calc_hist(df_m['bs'], bins=B_BINS, weights=df_m['ws'], density=True)
    b1_match_array.append(y / sum(y))
    b1_err_match_array.append(yerr / sum(y))

matched_mask = ((df1_allreco.pt != -9) & (df1_allreco.b != -9) &
                (df1_allreco.distance1 < 0.02) & (df1_allreco.distance2 < 0.02))
match_fake, _ = np.histogram(df1_allreco['pts'],               bins=PT_EDGES, weights=df1_allreco['ws'])
match, _      = np.histogram(df1_allreco[matched_mask]['pts'], bins=PT_EDGES, weights=df1_allreco[matched_mask]['ws'])
fake_rate_array = 1 - match / match_fake
print("fake rate:", fake_rate_array)

# Process sample 2

df2_allreco_pts = bin_df_in_pts(df2_allreco)
df2_match_pts   = bin_df_in_pts(df2_match)
df2_allfake_pts = bin_df_in_pts(df2_allfake)

rc2_allreco, err2_allreco = get_rc_and_err_arr(df2_allreco_pts, 'bs')
rc2_match,   err2_match   = get_rc_and_err_arr(df2_match_pts,   'bs')
rc2_allfake, err2_allfake = get_rc_and_err_arr(df2_allfake_pts, 'bs')

b2_allreco_array, sqrt_n_over_n_array_2 = [], []
for df_r in df2_allreco_pts:
    y, yerr, _ = calc_hist(df_r['bs'], bins=B_BINS, weights=df_r['ws'], density=True)
    b2_allreco_array.append(y / sum(y))
    y, yerr, _ = calc_hist(df_r['bs'], bins=[B_BINS[0], B_BINS[-1]], weights=df_r['ws'], density=True)
    sqrt_n_over_n_array_2.append(yerr[0] / y[0])

fig, ax = plt.subplots(figsize=(5, 5))
ax.errorbar(PT_CENTERS, rc2_allfake, xerr=PT_XERR, yerr=err2_allfake, capsize=3, color='b', ls='none', label='mistagged')
ax.errorbar(PT_CENTERS, rc2_allreco, xerr=PT_XERR, yerr=err2_allreco, capsize=3, color='k', ls='none', label='matched + mistagged')
ax.errorbar(PT_CENTERS, rc2_match,   xerr=PT_XERR, yerr=err2_match,   capsize=3, color='r', ls='none', label='matched')
ax.set_xlabel(r'full jet reco $p_{\mathrm{T}}$ [GeV]')
ax.set_title('sample 2')
ax.axhline(0.0, color='grey', linestyle='--')
ax.set_ylabel(r'reco charged jet $r_c$')
ax.set_ylim(-0.6, 0.1)
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()

# 1. Mistagged subtraction
b2_fakesubtracted_array, b2_err_fakesubtracted_array = [], []
rc_fakesubtracted_array, rc_err_fakesubtracted_array = [], []

for i in range(5):
    b2_sub     = (b2_allreco_array[i] - fake_rate_array[i] * b1_fake_array[i]) / (1 - fake_rate_array[i])
    b2_sub_err = np.array([np.sqrt(b2_sub[0] * b2_sub[1]) * sqrt_n_over_n_array_2[i] / np.sqrt(1 - fake_rate_array[i])] * 2)
    rc_fakesubtracted_array.append(b2_sub[1] - b2_sub[0])
    rc_err_fakesubtracted_array.append(2 * b2_sub_err[0])
    b2_fakesubtracted_array.append(b2_sub)
    b2_err_fakesubtracted_array.append(b2_sub_err)

# 2. pT correction

reweight_array, reweight_err_array = [], []
for i in range(5):
    num     = b2_fakesubtracted_array[i]     / sum(b2_fakesubtracted_array[i])
    denom   = b1_match_array[i]              / sum(b1_match_array[i])
    num_err = b2_err_fakesubtracted_array[i] / sum(b2_fakesubtracted_array[i])
    den_err = b1_err_match_array[i]          / sum(b1_match_array[i])
    rw      = num / denom
    reweight_array.append(rw)
    reweight_err_array.append(rw * np.sqrt((num_err / num)**2 + (den_err / denom)**2))
print("reweighting factors:", reweight_array)

# Reweight sample 1
rw = np.array(reweight_array)   # shape (5, 2): rw[i,0]=os weight, rw[i,1]=ss weight
pts_vals = df1_match['pts'].values
bs_vals  = df1_match['bs'].values
bin_idx  = np.clip(np.digitize(pts_vals, PT_EDGES) - 1, 0, 4)
df1_match = df1_match.copy()
df1_match['r'] = np.where(bs_vals == -1, rw[bin_idx, 0], rw[bin_idx, 1])

df1_match_pt = bin_df_in_pts(df1_match, col='pt')
rc_match_corrected, err_match_corrected = get_rc_and_err_new_arr(df1_match_pt, 'bs')


# Statistical uncertainty from reweight_err_array
rwerr_match_corrected = []

for i in range(5):
    df_cut_pt = df1_match[(df1_match['pt'] > PT_EDGES[i]) & (df1_match['pt'] < PT_EDGES[i+1])]
    df_cut_pt_pts = bin_df_in_pts(df_cut_pt)
    df_cut_pt_ss  = df_cut_pt.query('bs==1')
    p_array, prob_ss_array = [], []
    for j in range(5):
        _, _, p = _get_rc_p(df_cut_pt_pts[j], 'bs')
        prob_ss = (sum(df_cut_pt_ss[(df_cut_pt_ss.pts > PT_EDGES[j]) & (df_cut_pt_ss.pts < PT_EDGES[j+1]) &
                                    (df_cut_pt_ss.pt  > PT_EDGES[i]) & (df_cut_pt_ss.pt  < PT_EDGES[i+1])]['w']) /
                   sum(df_cut_pt_ss[(df_cut_pt_ss.pt > PT_EDGES[i]) & (df_cut_pt_ss.pt  < PT_EDGES[i+1])]['w']))
        p_array.append(p)
        prob_ss_array.append(prob_ss)
    p_err = np.sqrt(sum((reweight_err_array[j][1] * p_array[j] * prob_ss_array[j])**2 for j in range(5)))
    rwerr_match_corrected.append(2 * p_err)

rc_rwerr   = np.asarray(rwerr_match_corrected)
rc_err     = np.asarray(err_match_corrected)
rc_err_tot = np.sqrt(rc_rwerr**2 + rc_err**2)
print('central rc values:               ', rc_match_corrected)
print('uncertainties from reweighting:  ', rc_rwerr)
print('uncertainties from PYTHIA jets:  ', rc_err)
print('total statistical uncertainties: ', rc_err_tot)

# Obtain truth from sample 2
df2_alltruth_pt = bin_df_in_pts(df2_alltruth, col='pt')
rc2_truth, err2_truth = get_rc_and_err_arr(df2_alltruth_pt, 'b')

# Closure plot
x_shift = [-1, -0.5, 0, 0.5]

fig, ax = plt.subplots(figsize=(5, 5))
ax.errorbar([c + x_shift[0] for c in PT_CENTERS], rc2_allreco,
            yerr=err2_allreco, capsize=3, color='k', ls='none', marker='x', label='Raw')
ax.errorbar([c + x_shift[1] for c in PT_CENTERS], rc_fakesubtracted_array,
            yerr=rc_err_fakesubtracted_array, capsize=3, color='r', ls='none', marker='s',
            label='Partially corrected (after 1 step)')
ax.errorbar([c + x_shift[2] for c in PT_CENTERS], rc_match_corrected,
            yerr=rc_err_tot, capsize=3, color='olive', ls='none', marker='o',
            label='Fully corrected (after 2 steps)')
eb = ax.errorbar([c + x_shift[3] for c in PT_CENTERS], rc2_truth,
                 xerr=PT_XERR, yerr=err2_truth, capsize=3, color='g', ls='none', label='Truth')
eb[-1][0].set_linestyle('--')
eb[-1][1].set_linestyle('--')
ax.set_xlabel(r'full jet $p_{\mathrm{T}}$ [GeV/$c$]')
ax.axhline(0.0, color='grey', linestyle='--')
ax.set_ylabel(r'charged $r_c$')
ax.set_ylim(-0.6, -0.1)
ax.legend(loc='lower left', frameon=False)
ax.text(20, -0.28, 'STAR Simulation\n$p$+$p$ $\\sqrt{s}=200$ GeV\nPYTHIA6+GEANT3\n'
        r'anti-$k_{\mathrm{T}}$ jets, $R=0.4$, $|\eta|<0.6$')
ax.tick_params(top=True, right=True, bottom=True, left=True, direction='in', which='both')
ax.yaxis.set_minor_locator(MultipleLocator(0.05))
plt.savefig('fig7a.png', bbox_inches='tight')
plt.show()

# Relative difference: (corrected - truth) / truth
rc_corr  = np.asarray(rc_match_corrected)
rc_truth = np.asarray(rc2_truth)

fig, ax = plt.subplots(figsize=(5, 5))
ax.errorbar(PT_CENTERS, (rc_corr - rc_truth) / rc_truth,
            yerr=rc_err_tot / np.abs(rc_truth),
            capsize=3, color='olive', ls='none', marker='o', label='stat. unc. on corrected')
eb = ax.errorbar(PT_CENTERS, np.zeros(5),
                 yerr=np.asarray(err2_truth) / np.abs(rc_truth),
                 capsize=3, color='g', ls='none', label='stat. unc. on truth')
eb[-1][0].set_linestyle('--')
ax.axhline(0.0, color='grey', linestyle='--')
ax.set_xlabel(r'full jet $p_{\mathrm{T}}$ [GeV/$c$]')
ax.set_ylabel(r'$(r_c^{\mathrm{corrected}}-r_c^{\mathrm{truth}})/r_c^{\mathrm{truth}}$')
ax.set_ylim(-0.1, 0.1)
ax.set_xlim(15, 60)
ax.legend(loc='lower left', frameon=False)
ax.tick_params(top=True, right=True, bottom=True, left=True, direction='in', which='both')
ax.yaxis.set_minor_locator(MultipleLocator(0.05))
plt.savefig('fig7b.png', bbox_inches='tight')
plt.show()

print('relative difference:               ', (rc_corr - rc_truth) / rc_truth)
print('stat. unc. on corrected / |truth|: ', rc_err_tot / np.abs(rc_truth))
print('stat. unc. on truth     / |truth|: ', np.asarray(err2_truth) / np.abs(rc_truth))