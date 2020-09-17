import numpy as np
from scipy import interpolate

try:
    from .process_data import data
except ImportError:
    from process_data import data

import matplotlib.pyplot as plt
from matplotlib import style, ticker
import seaborn as sns
from labellines import labelLines
from scipy import stats

sns.set()
# style.use("seaborn")

fig, ax_m = plt.subplots(1, 1, figsize=(8, 6), dpi=200)
ax_ft = ax_m.twinx()


def convert_ax_m_to_ft(ax_m):
    y1, y2 = ax_m.get_ylim()
    meters2feet = lambda x: x / 0.3048
    ax_ft.set_ylim(meters2feet(y1), meters2feet(y2))
    ax_ft.figure.canvas.draw()


ax_m.callbacks.connect("ylim_changed", convert_ax_m_to_ft)
# colors = plt.cm.rainbow(np.linspace(0, 1, len(percentiles)))

altitude = data.altitude.mean(
    dim=["latitude", "longitude", "time"],
).data

coverage_thresholds = [1e-3, 1e-2, 1e-1]
# colors = plt.cm.rainbow(np.linspace(0, 1, len(coverage_thresholds))[::-1])
colors = sns.husl_palette(len(coverage_thresholds))[::-1]

for i, coverage_threshold in enumerate(coverage_thresholds):

    fraction_covered = []
    for j in range(len(data.level)):
        cc_overhead_level = data.cc_overhead.isel(level=j).data.flatten()

        # Build up a statistical model
        # fit = stats.

        fraction_covered.append(
            (
                    np.sum(cc_overhead_level >= coverage_threshold) + 1
            ) / (len(cc_overhead_level) + 2)
        )
    fraction_covered = np.array(fraction_covered)

    altitude_plt = np.linspace(
        0,
        30000,
        500
    )
    # fraction_covered_plt = 10**interpolate.interp1d(
    #     altitude,
    #     np.log10(fraction_covered),
    #     kind="slinear",
    #     fill_value="extrapolate",
    # )(altitude_plt)
    fraction_covered_plt = 10**interpolate.PchipInterpolator(
        altitude[::-1],
        np.log10(fraction_covered[::-1]),
        extrapolate=True
    )(altitude_plt)

    ax_m.plot(
        fraction_covered_plt,
        altitude_plt,
        label=f"Cloud Coverage > {coverage_threshold:.0e}",
        color=colors[i]
    )

ax_m.annotate(
    s="1/1000 chance of >10%\ncloud coverage at 55.3 kft",
    xy=(1e-3, 16850),
    xytext=(2e-4, 10000),
    xycoords="data",
    ha="right",
    arrowprops={
        "color"     : "k",
        "width"     : 0.25,
        "headwidth" : 4,
        "headlength": 6,
    }
)
ax_m.annotate(
    s="Nonzero asymptote due\nto Bayesian prior\n(beta dist.)",
    xy=(3.53e-6, 29000),
    xytext=(2e-5, 27000),
    xycoords="data",
    ha="left",
    arrowprops={
        "color"     : "k",
        "width"     : 0.25,
        "headwidth" : 4,
        "headlength": 6,
    }
)
plt.annotate(
    s="60% chance of clouds\non a given CONUS day",
    xy=(0.60, 1000),
    xytext=(7e-2, 3000),
    xycoords="data",
    ha="right",
    arrowprops={
        "color"     : "k",
        "width"     : 0.25,
        "headwidth" : 4,
        "headlength": 6,
    }
)


ax_m.axhline(y=65000 * 0.3048, ls='--', color="gray")
ax_m.text(
    x=0.8*ax_m.get_xlim()[1]+(1-0.8)*ax_m.get_xlim()[0],
    y=65000 * 0.3048 ,
    s="65,000 ft",
    color="gray",
    horizontalalignment='center',
    verticalalignment='bottom'
)
ax_m.axhline(y=55000 * 0.3048, ls='--', color="gray")
ax_m.text(
    x=0.8*ax_m.get_xlim()[1]+(1-0.8)*ax_m.get_xlim()[0],
    y=55000 * 0.3048 ,
    s="55,000 ft",
    color="gray",
    horizontalalignment='center',
    verticalalignment='bottom'
)
plt.annotate(
    s="Source: ECMWF ERA5 Reanalysis",
    xy=(0.02, 0.02),
    xycoords="axes fraction",
    ha="left",
    fontsize=9
)



ax_m.set_xlabel(r"Fraction of Time with Cloud Coverage above Threshold")
ax_m.set_ylabel(r"Altitude [m]")
ax_ft.set_ylabel(r"Altitude [ft]")
plt.title("Cloud Coverage by Altitude over CONUS")
# ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2000))
plt.xscale('log')
ax_m.set_xlim((1e-6, 1))
plt.tight_layout()
ax_m.grid(True)
ax_ft.grid(False)
ax_m.legend()
# labelLines(plt.gca().get_lines(), zorder=2.5)
plt.savefig("analysis_cloud_coverage_at_altitude/analysis_cloud_coverage_at_altitude.png")
plt.show()
