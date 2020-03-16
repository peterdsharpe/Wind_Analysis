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

# Take a small sampling just to test # TODO remove for full analysis
dims = wind_speed_squared.shape
times_to_use = np.arange(0, 1968, 24) #np.round(np.linspace(0, dims[0]-1, 82)).astype(int)
pressure_levels_to_use = 8#np.round(np.linspace(0, dims[1]-1, 5)).astype(int)
lats_to_use = 46 #np.round(np.linspace(0, dims[2]-1, 100)).astype(int)
lons_to_use = np.round(np.linspace(0, dims[2]-1, 100)).astype(int)

wind_speed_squared = wind_speed_squared[
    times_to_use,
    pressure_levels_to_use,
    lats_to_use,
    lons_to_use
]
altitude = altitude[
    times_to_use,
    pressure_levels_to_use,
    lats_to_use,
    lons_to_use
]

# Add time categorization

iris.coord_categorisation.add_hour(wind_speed_squared, 'time', name='hour_of_day')
iris.coord_categorisation.add_hour(altitude, 'time', name='hour_of_day')

# Display info
print("\nData to use:")
print(wind_speed_squared.summary())
print(altitude.summary())

# endregion

##### region Analyze

# plt.scatter(wind_speed.data.reshape(-1), altitude.data.reshape(-1))
# plt.show()

# Regression


# data = wind_speed.data
print("Reshaping data...")
data = wind_speed_squared.data.reshape(-1)
print("Data reshaped!")

import time

start = time.time()

### Method 3
params = stats.ncx2.fit(
    data,
    2, # Degrees of freedom
    0.25, # Noncentrality parameter
    fix_df=2, # 2 DoF
    floc=0, # centered at zero
    scale=40 # scale
    # fscale=1 # scale
)

print("Fit Parameters:\n", params)
print("Fit Runtime:\n", time.time() - start)

# Visualize distribution
style.use('fivethirtyeight')
x = np.linspace(0, np.max(data),400)
plt.figure()
plt.plot(x, stats.ncx2.pdf(x, *params), label="Model")
plt.hist(data, bins=120, density=True, label="Data")
plt.xlabel("Wind Speed Squared [(m/s)^2]")
plt.ylabel("Probability Distribution Function")
plt.title("Wind Speed over CONUS, Summer\n5 kPa PL (~20908 m, ~68596 ft.)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("fit.png", dpi=600)
plt.savefig("fit.svg")
plt.show()

# Print percentiles
print("Data Wind Speed 99th percentile: ", np.sqrt(np.percentile(data, 99)))
print("Fit  Wind Speed 99th percentile: ", np.sqrt(stats.ncx2.ppf(0.99, *params)))
# endregion
