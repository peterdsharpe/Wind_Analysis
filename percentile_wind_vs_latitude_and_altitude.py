import iris.coord_categorisation
import matplotlib.style as style
from cf_units import Unit
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import iris.analysis as ia
import numpy as np

percentiles = [50, 75, 90, 95, 99]

for percentile in percentiles:

    style.use("seaborn")

    # percentile = 95

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

    wind_speed_squared = wind_speed_squared.collapsed(["time","longitude"], ia.PERCENTILE, percent=percentile)

    wind_speed = wind_speed_squared ** 0.5

    # Display info
    print("\nOriginal Data:")
    print(wind_speed.summary())

    latitudes = wind_speed.dim_coords[1].points
    speeds = np.array(wind_speed.data)

    np.save("wind_%.0f_vs_latitudes_altitudes" % percentile, speeds)

    # Supersample
    from scipy import ndimage
    ss_factor = 5
    latitudes = ndimage.zoom(latitudes, ss_factor)
    altitudes = ndimage.zoom(altitudes, ss_factor)
    speeds = ndimage.zoom(speeds, ss_factor)


    plt.figure()
    plt.ion()
    X, Y = np.meshgrid(
        latitudes,
        altitudes,
    )
    Z = speeds
    fig = plt.contourf(
        X,
        Y,
        Z,
        cmap="viridis"
    )
    plt.xlabel("Latitude [deg]")
    plt.ylabel("Altitude [m]")
    plt.title("%.0f%% Wind Speeds, CONUS July-Aug, 1972-present" % percentile)
    plt.colorbar(label="Wind Speed [m/s]")
    plt.tight_layout()
    plt.savefig("wind_speeds_%.0f.svg" % percentile)
    plt.show()

