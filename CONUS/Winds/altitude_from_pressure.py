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

altitude = altitude.collapsed(['time', 'longitude', 'latitude'], ia.MEAN)

# Extract
pressures_Pa = np.array(altitude.dim_coords[0].points) * 100
altitudes = np.array(altitude.data)

if __name__ == "__main__":
    plt.figure()
    plt.semilogy(altitudes, pressures_Pa,'.-')
    plt.xlabel("Altitude [m]")
    plt.ylabel("Pressure [Pa]")
    plt.title("Altitude vs. Pressure, CONUS July-Aug, 1972-present")
    plt.tight_layout()
    plt.show()
