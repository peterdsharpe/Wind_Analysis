import iris.coord_categorisation
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import scipy.stats as stats
from cf_units import Unit
style.use("seaborn")

##### region Parse

# Pull in data from file
eastward_wind = iris.load('u_component_of_wind.nc')[0]
northward_wind = iris.load('v_component_of_wind.nc')[0]
geopotential = iris.load('geopotential.nc')[0]

# Find the wind speed
wind_speed = (eastward_wind ** 2 + northward_wind ** 2) ** 0.5
wind_speed.standard_name = "wind_speed"
wind_speed.long_name = "Wind Speed"
wind_speed.var_name = "V"

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
print(wind_speed.summary())
print(altitude.summary())

# # Take a small sampling just to test # TODO remove for full analysis
# dims = wind_speed.shape
# times_to_use = np.round(np.linspace(0, dims[0]-1, dims[0])).astype(int)
# pressure_levels_to_use = 8#np.round(np.linspace(0, dims[1]-1, 5)).astype(int)
# lats_to_use = np.round(np.linspace(0, dims[2]-1, 25)).astype(int)
# lons_to_use = np.round(np.linspace(0, dims[2]-1, 25)).astype(int)
#
# wind_speed = wind_speed[
#     times_to_use,
#     pressure_levels_to_use,
#     lats_to_use,
#     lons_to_use
# ]
# altitude = altitude[
#     times_to_use,
#     pressure_levels_to_use,
#     lats_to_use,
#     lons_to_use
# ]

import iris.quickplot as qplt
import iris.analysis as an

fig = qplt.contourf(wind_speed[0,-1,:,:], cmap="viridis")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Winds at Ground, 6/15/1972 0:00 GMT")
plt.tight_layout()
plt.savefig("ground_winds_demo.svg")
plt.show()

fig = qplt.contourf(wind_speed[0,8,:,:], cmap="viridis")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Winds at 5 kPa PL (~20908 m, ~68596 ft.), 6/15/1972 0:00 GMT")
plt.tight_layout()
plt.savefig("aloft_winds_demo.svg")
plt.show()