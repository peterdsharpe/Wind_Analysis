import numpy as np
from scipy import interpolate
try:
    from .process_data import data
except ImportError:
    from process_data import data

percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]

import matplotlib.pyplot as plt
from matplotlib import style, ticker
import seaborn as sns
from labellines import labelLines
sns.set(font_scale=1)
style.use("default")

fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=200)
colors = plt.cm.rainbow(np.linspace(0, 1, len(percentiles)))

altitude_mean = data["altitude"].mean(
    dim=["latitude", "longitude", "time"],
).data

for i, percentile in enumerate(percentiles):
    windspeed_pct = data["windspeed"].quantile(
        dim=["latitude", "longitude", "time"],
        q=percentile/100
    ).data

    altitude_plt = np.linspace(
        np.min(altitude_mean),
        30000,
        500
    )
    windspeed_plt = interpolate.interp1d(
        x=altitude_mean,
        y=windspeed_pct,
        kind="cubic"
    )(altitude_plt)
    plt.plot(
        windspeed_plt,
        altitude_plt,
        "-",
        label="%i%%" % percentile,
        color=colors[i],
    )
plt.title("Summertime Wind Speed Percentiles the CONUS")
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2000))
plt.xlabel(r"Wind Speed [m/s]")
plt.ylabel(r"Altitude [m]")
plt.tight_layout()
plt.grid(True)
label_x = (0, 30)
labelLines(ax.get_lines(), xvals=label_x, zorder=2.5)
plt.savefig("analysis_wind_speed_percentiles_at_altitude/analysis_wind_speed_percentiles.png")
plt.show()
