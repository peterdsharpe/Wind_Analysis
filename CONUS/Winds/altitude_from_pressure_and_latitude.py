import iris.coord_categorisation
import matplotlib.style as style
from cf_units import Unit
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import iris.analysis as ia
import numpy as np

style.use("seaborn")

##### region Parse

# Pull in data from file
geopotential = iris.load('geopotential.nc')[0]


# Find the altitude from geopotential
altitude = geopotential / 9.80665
altitude.standard_name = "altitude"
altitude.long_name = "Altitude"
altitude.var_name = "h"
altitude.units = Unit("meters")

altitude = altitude.collapsed(['time', 'longitude'], ia.MEAN)

plt.figure()
plt.ion()
X, Y = np.meshgrid(
    altitude.dim_coords[1].points,
    np.log10(altitude.dim_coords[0].points*100),
)
Z = np.array(altitude.data)
fig = plt.contourf(
    X,
    Y,
    Z,
    cmap="viridis"
)
plt.xlabel("Latitude [deg]")
plt.ylabel("log10(Pressure [Pa])")
plt.title("Altitude vs. Pressure, CONUS July-Aug, 1972-present")
plt.tight_layout()
# plt.savefig("aloft_wind_speeds.svg")
plt.colorbar(label="Altitude")
plt.show()

# fig = plt.contourf(altitude, cmap="viridis")
