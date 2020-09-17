import numpy as np
from scipy import interpolate
import xarray as xr

try:
    from .process_data import data
except ImportError:
    from process_data import data

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

w_m_s = data.w_m_s  # type: xr.DataArray

### Figure: Histogram of all vertical speeds
fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
plt.hist(
    w_m_s.data.flatten(),
    bins=100,
    density=True,
)
plt.annotate(
    s="Source: ECMWF ERA5 Dataset",
    xy=(0.02, 0.98),
    xycoords="axes fraction",
    ha="left",
    va="top",
    fontsize=9
)
plt.yscale('log')
plt.xlabel(r"Vertical Wind Speed [m/s]")
plt.ylabel(r"Probability Distribution Function")
plt.title("Relative Frequencies of Different Vertical Wind Speeds\n(CONUS, Summers, 1970-2020, all altitudes)")
plt.tight_layout()
plt.legend()
# plt.savefig("C:/Users/User/Downloads/temp.svg")
plt.show()


### Figure: Vertical speed KDE plot at different altitudes
fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
colors = plt.cm.rainbow(np.linspace(0, 1, len(data.coords["level"])))
for i, level in enumerate(data.coords["level"].data[::-1]):
    sns.kdeplot(
        w_m_s.sel(level=level).data.flatten(),
        color=colors[i],
        bw=0.01,
        label=f"{data.altitude.sel(level=level).mean().data:.0f} m",
        linewidth=1,
    )
plt.annotate(
    s="Source: ECMWF ERA5 Dataset",
    xy=(0.02, 0.98),
    xycoords="axes fraction",
    ha="left",
    va="top",
    fontsize=9
)
# plt.yscale('log')
# plt.ylim(1e-5, 1e2)
plt.xlim(-0.25, 0.25)
plt.xlabel(r"Vertical Wind Speed [m/s]")
plt.ylabel(r"Probability Distribution Function")
plt.title(f"Vertical Wind Speeds Distributions at Various Altitudes\n(averaged over CONUS, Summers, 1970-2020)")
plt.tight_layout()
plt.legend(ncol=2, fontsize=8)
plt.show()

### Figure: RMS Vertical Speed at different altitudes
fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
w_m_s_var = data.w_m_s.var(dim=["latitude", "longitude", "time"])
plt_x = np.sqrt(w_m_s_var.data)
plt_y = data.altitude.mean(["latitude", "longitude", "time"]).data
plt_y_i = np.linspace(np.min(plt_y), np.max(plt_y), 500)
plt_x_i = interpolate.PchipInterpolator(plt_y[::-1], plt_x[::-1])(plt_y_i)
plt.plot(plt_x_i, plt_y_i)
plt.plot(plt_x, plt_y, "k.")
plt.annotate(
    s="Source: ECMWF ERA5 Dataset",
    xy=(0.02, 0.98),
    xycoords="axes fraction",
    ha="left",
    va="top",
    fontsize=9
)
plt.xlabel(r"Standard Deviation of Vertical Wind Speed [m/s]")
plt.ylabel(r"Altitude [m]")
plt.title("Typical Vertical Wind Speeds\n(averaged over CONUS, Summers, 1970-2020)")
plt.tight_layout()
plt.legend()
# plt.savefig("C:/Users/User/Downloads/temp.svg")
plt.show()
