import iris.coord_categorisation
from cf_units import Unit
import iris.quickplot as qplt
import iris.plot as iplt
import iris.analysis as ia
import numpy as np
from scipy import interpolate
import parse_data

data = parse_data.get_data()
data = {k: data[k] for k in ["altitude", "windspeed"]}

percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]

import matplotlib.pyplot as plt
from matplotlib import style, ticker
import seaborn as sns
from labellines import labelLines
sns.set(font_scale=1)
style.use("default")

fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi=200)
colors = plt.cm.rainbow(np.linspace(0, 1, len(percentiles)))

altitude_mean = np.array(data["altitude"].collapsed(
    ["latitude", "longitude", "time"],
    ia.MEAN
).data)
np.save("analysis_wind_speed_percentiles_at_altitude/altitude.npy", altitude_mean)

for i, percentile in enumerate(percentiles):
    windspeed_pct = np.array(data["windspeed"].collapsed(
        ["latitude", "longitude", "time"],
        ia.PERCENTILE,
        percent=percentile
    ).data)
    np.save("analysis_wind_speed_percentiles_at_altitude/wind_speed_%i_percentile.npy" % percentile, windspeed_pct)
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
plt.xlabel(r"Wind Speed [m/s]")
plt.ylabel(r"Altitude [m]")
plt.title("Summertime Wind Speed Percentiles over Spaceport America")
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2000))
plt.tight_layout()
plt.grid(True)
labelLines(plt.gca().get_lines(), zorder=2.5)
plt.savefig("analysis_wind_speed_percentiles_at_altitude/analysis_wind_speed_percentiles.png")
plt.show()
