import numpy as np
import matplotlib.pyplot as plt
from utils import get_data

EMB_FILE = '/gpfs01/star/pwg/youqi/run12/final_0628/results_20235003/matched/all050124_rc_notrueptcons.root'
COLUMNS  = ['pt', 'b', 'w', 'y1', 'y2', 'phi1', 'phi2',
               'pts', 'bs', 'ws', 'y1s', 'y2s', 'phi1s', 'phi2s', 'nefs']
PT_EDGES = [15, 20, 25, 30, 40, 60]
PT_CENTERS = [17.5, 22.5, 27.5, 35, 50]

plt.rcParams['font.size'] = 12


def delta_phi(a, b):
    diff = np.abs(a - b)
    return np.minimum(diff, 2 * np.pi - diff)

def get_eff(df, cut):
    true  = np.histogram(df['pt'], bins=PT_EDGES, weights=df['w'])[0]
    match = np.histogram(df[cut]['pt'], bins=PT_EDGES, weights=df[cut]['w'])[0]
    return match / true


df = get_data(COLUMNS, EMB_FILE, 'MatchedTree').query('pt>15 and b!=-9').copy()

df['distance1'] = np.sqrt(delta_phi(df['phi1'].values, df['phi1s'].values)**2
                          + (df['y1'].values - df['y1s'].values)**2)
df['distance2'] = np.sqrt(delta_phi(df['phi2'].values, df['phi2s'].values)**2
                          + (df['y2'].values - df['y2s'].values)**2)

df_os = df.query('b==-1')
df_ss = df.query('b==1')

cut1_os = df_os.pts > 15
cut2_os = (df_os.pts > 15) & (df_os.bs != -9)
cut3_os = (df_os.pts > 15) & (df_os.bs != -9) & (df_os.distance1 < 0.02) & (df_os.distance2 < 0.02)
cut1_ss = df_ss.pts > 15
cut2_ss = (df_ss.pts > 15) & (df_ss.bs != -9)
cut3_ss = (df_ss.pts > 15) & (df_ss.bs != -9) & (df_ss.distance1 < 0.02) & (df_ss.distance2 < 0.02)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(PT_CENTERS, get_eff(df_ss, cut1_ss), 'o',   color='k',        ls='none', label='same sign')
ax.plot(PT_CENTERS, get_eff(df_os, cut1_os), 'x',   color='k',        ls='none', label='opposite signs')
ax.plot(PT_CENTERS, get_eff(df_os, cut1_os), 'x--', color='k',        label=r'cut1 = $p_{\mathrm{T}}^{\mathrm{det}}>15$ GeV$/c$, $\Delta R_{\mathrm{jet}}<0.4$')
ax.plot(PT_CENTERS, get_eff(df_os, cut2_os), 'x--', color='tab:blue', label=r'cut2 = cut1 + reco $N_{ch} \geq$ 2')
ax.plot(PT_CENTERS, get_eff(df_os, cut3_os), 'x--', color='r',        label=r'cut3 = cut2 + $\Delta R_{\mathrm{track}}$ < 0.02')
ax.plot(PT_CENTERS, get_eff(df_ss, cut1_ss), 'o--', color='k')
ax.plot(PT_CENTERS, get_eff(df_ss, cut2_ss), 'o--', color='tab:blue')
ax.plot(PT_CENTERS, get_eff(df_ss, cut3_ss), 'o--', color='r')
ax.set_xlabel(r'truth-level $p_{\mathrm{T}}$ [GeV$/c$]')
ax.set_ylabel('efficiency')
ax.text(43, 0.63, 'STAR Simulation\n$p$+$p$ $\\sqrt{s}=200$ GeV\nanti-$k_{\\mathrm{T}}$ jets, $R=0.4$')
ax.legend()
ax.set_xlim(15, 60)
ax.set_ylim(0., 1)
plt.savefig('fig6.pdf', bbox_inches='tight')
plt.show()

print("Opposite sign jets efficiency:", get_eff(df_os, cut3_os))
print("Same sign jets efficiency:", get_eff(df_ss, cut3_ss))
