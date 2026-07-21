import numpy as np
import matplotlib.pyplot as plt
from utils import get_data, calc_hist

EMB_FILE = '/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.root'
COLUMNS  = ['pt', 'b', 'w', 'y1', 'y2', 'phi1', 'phi2',
            'pts', 'bs', 'ws', 'y1s', 'y2s', 'phi1s', 'phi2s', 'nefs']
plt.rcParams['font.size'] = 15

df = get_data(COLUMNS, EMB_FILE, 'MatchedTree').query('w < 1 and pts > 15 and bs != -9 and nefs < 0.9').copy()

def delta_phi(a, b):
    diff = np.abs(a - b)
    return np.minimum(diff, 2 * np.pi - diff)

df['distance1'] = np.sqrt(delta_phi(df['phi1'].values, df['phi1s'].values)**2
                          + (df['y1'].values - df['y1s'].values)**2)
df['distance2'] = np.sqrt(delta_phi(df['phi2'].values, df['phi2s'].values)**2
                          + (df['y2'].values - df['y2s'].values)**2)

DR_BINS = np.arange(0, 0.055, 0.005)
kw = dict(bins=DR_BINS, weights=df['ws'], density=True)
y1, yerr1 = calc_hist(df['distance1'], **kw)[:2]
y2, yerr2 = calc_hist(df['distance2'], **kw)[:2]

bin_centers = 0.5 * (DR_BINS[:-1] + DR_BINS[1:])

fig, ax = plt.subplots()
ax.errorbar(bin_centers, y1, xerr=0., yerr=yerr1, label='leading track')
ax.errorbar(bin_centers, y2, xerr=0., yerr=yerr2, label='subleading track')
ax.set_xticks(np.arange(0, 0.06, 0.01))
ax.set_xlabel(r'$\Delta R_{\mathrm{track}}$(truth, det.)')
ax.set_yscale('log')
ax.set_ylabel('arb. unit')
ax.legend()
ax.text(0.015, 3,
        'STAR Simulation\n$p$+$p$ $\\sqrt{s}=200$ GeV\nPYTHIA6+GEANT3\n'
        r'anti-$k_{\mathrm{T}}$ jets, $R=0.4$, $|\eta|<0.6$' '\n'
        r'$p_{\mathrm{T,jet}}^{\mathrm{tru}}>5$ GeV$/c$,'
        r' $p_{\mathrm{T,jet}}^{\mathrm{det}}>15$ GeV$/c$',
        fontsize=15)
plt.savefig('fig1.png', bbox_inches='tight')
plt.show()