import numpy as np
from scipy import interpolate

try:
    from .process_data import data
except ImportError:
    from process_data import data

altitude_ft = 55000
altitude = altitude_ft * 0.3048

altitudes = data.altitude.mean(
    dim=["latitude", "longitude", "time"],
).data

level_index = interpolate.interp1d(
    altitudes,
    np.arange(len(altitudes))
)(altitude)

level_index_base = int(level_index)
level_index_rem = level_index % 1

data_level = (
        (1 - level_index_rem) * data.isel(level=level_index_base) +
        (level_index_rem) * data.isel(level=level_index_base + 1)
)
cc_overhead_level = data_level.cc_overhead.data.flatten()

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from aerosandbox.tools.miscellaneous import eng_string
# sns.set(palette=sns.color_palette("husl"))

fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
sns.distplot(
    cc_overhead_level,
    hist=True,
    kde=False,
    axlabel="Cloud Coverage Fraction",
    bins = np.linspace(0, 1, 100),
    norm_hist=True
    # fit = stats.beta
    # kde_kws=dict(
    #     bw=0.03, shade=True, cut=10
    # )
)

plt.annotate(
    s="Source: ECMWF ERA5 Reanalysis",
    xy=(0.02, 0.02),
    xycoords="axes fraction",
    ha="left",
    fontsize=9
)
plt.xlim(0, 1)
plt.ylim(1e-4, 1e2)
plt.yscale('log')
plt.ylabel("Probability Distribution Function")
plt.title(f"Distribution of Cloud Coverage at {eng_string(altitude_ft)} ft.")

plt.show()

