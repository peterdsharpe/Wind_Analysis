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
eastward_wind = iris.load('u_component_of_wind.nc')[0]
northward_wind = iris.load('v_component_of_wind.nc')[0]

# Find the wind speed
wind_speed_squared = eastward_wind ** 2 + northward_wind ** 2
wind_speed_squared.standard_name = "wind_speed"
wind_speed_squared.long_name = "Wind Speed Squared"
wind_speed_squared.var_name = "V"

# Find the altitude from geopotential
altitudes = np.load("altitudes.npy")

wind_speed_squared = wind_speed_squared.collapsed(["time","longitude"], ia.MEAN)

wind_speed = wind_speed_squared ** 0.5

# Display info
print("\nOriginal Data:")
print(wind_speed.summary())


plt.figure()
plt.ion()
X, Y = np.meshgrid(
    wind_speed.dim_coords[1].points,
    altitudes,
)
Z = np.array(wind_speed.data)
fig = plt.contourf(
    X,
    Y,
    Z,
    cmap="viridis"
)
plt.xlabel("Latitude [deg]")
plt.ylabel("Altitude [m]")
plt.title("Mean Wind Speeds, CONUS July-Aug, 1972-present")
plt.tight_layout()
# plt.savefig("aloft_wind_speeds.svg")
plt.colorbar(label="Wind Speed [m/s]")
plt.show()