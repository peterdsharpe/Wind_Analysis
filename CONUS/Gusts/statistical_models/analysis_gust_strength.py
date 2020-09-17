from data import sigma, altitude, probability_of_exceedance, von_karman_gust_intensity
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(palette=sns.color_palette("husl"))
plt.scatter(
    sigma,
    altitude,
    c=np.log10(probability_of_exceedance),
    cmap="PuBu"
)
plt.xlabel(r"Turbulence Intensity $\sigma$ [m/s]")
plt.ylabel(r"Altitude [m]")
plt.title(r"Von Karman Gusts: Turbulence Intensity")
plt.tight_layout()
cb = plt.colorbar()
cb.set_label(r"$log_{10}($Probability of Exceedance$)$")
plt.legend()
# plt.savefig("C:/Users/User/Downloads/temp.svg")
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
plt.xscale('log')
poes = np.logspace(-1, -6, 300)
alts = np.linspace(0, np.max(altitude), 300)
Poes, Alts = np.meshgrid(
    poes,
    alts,
    indexing="ij"
)
Sigmas = np.zeros_like(Poes)
for i, alt in enumerate(alts):
    Sigmas[:, i] = von_karman_gust_intensity(alt, poes).flatten()
Poes_per_hour = Poes / 4
levels = np.linspace(0, 10, 21)
plt.contourf(
    Poes_per_hour,
    Alts,
    Sigmas,
    levels=levels,
    alpha=0.7,
    # antialiased=False,
    linewidths=0,
    cmap=plt.cm.Spectral.reversed()
)
CS = ax.contour(
    Poes_per_hour,
    Alts,
    Sigmas,
    levels=levels,
    colors="k",
    linewidths=1,
    alpha=0.9
)
plt.annotate(
    s="Data: \"Flying Qualities of Piloted Aircraft\"\n"
      "MIL-STD-1797A (1990), U.S. DoD\n"
      "*Approximate, assumes 4-hour flights\n"
      "for DoD data-collection missions",
    xy=(0.98, 0.98),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=8,
    color=(0, 0, 0, 1)
)

ax.clabel(CS, levels[0::2],  # label every second level
          inline=1, fmt='%.0f m/s', fontsize=10)
cb = plt.colorbar()
from matplotlib import ticker

cb.locator = ticker.MultipleLocator(base=1)
cb.update_ticks()
cb.set_label("Turbulence Intensity (RMS Gusts) [m/s]")
plt.xlabel("Probability of Gust Limit Exceedance Per Flight-Hour*")
plt.ylabel(r"Altitude [m]")
plt.title(r"RMS Gust Strengths at Various Altitudes")
plt.tight_layout()
# plt.legend()
# plt.savefig("C:/Users/User/Downloads/temp.svg")
plt.show()
