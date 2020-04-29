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
geopotential = iris.load('geopotential.nc')[0]

# Find the wind speed
wind_speed_squared = eastward_wind ** 2 + northward_wind ** 2
wind_speed_squared.standard_name = "wind_speed"
wind_speed_squared.long_name = "Wind Speed Squared"
wind_speed_squared.var_name = "V"

# Find the altitude from geopotential
altitude = geopotential / 9.80665
altitude.standard_name = "altitude"
altitude.long_name = "Altitude"
altitude.var_name = "h"
altitude.units = Unit("meters")

# Clear memory
# del eastward_wind
# del northward_wind
# del geopotential
# del Unit

# Debug: Plot
# qplt.contourf(wind_speed[0,0,:,:])
# qplt.show()

# Display info
print("\nOriginal Data:")
print(wind_speed_squared.summary())
print(altitude.summary())



wind_speed_at_alt = wind_speed_squared[:, 8, :, :] ** 0.5
mean_wind_speed_at_alt = wind_speed_at_alt.collapsed('time', ia.MEAN)

plt.figure()
plt.ion()
X, Y = np.meshgrid(
    mean_wind_speed_at_alt.dim_coords[1].points,
    mean_wind_speed_at_alt.dim_coords[0].points,
)
Z = np.array(mean_wind_speed_at_alt.data)
fig = plt.contourf(
    X,
    Y,
    Z,
    cmap="viridis"
)
plt.xlabel("Longitude [deg]")
plt.ylabel("Latitude [deg]")
plt.title("Mean Wind Speeds at 5 kPa PL (~20908 m, ~68596 ft.), CONUS July-Aug, 1972-present")
plt.tight_layout()
# plt.savefig("aloft_wind_speeds.svg")
plt.colorbar(label="Wind Speed [m/s]")
plt.show()

# fig = plt.contourf(mean_wind_speed_at_alt, cmap="viridis")
