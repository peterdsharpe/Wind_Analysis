import iris.coord_categorisation
import numpy as np
from cf_units import Unit

def get_data():
    # Pull in data from file
    eastward_wind = iris.load('data/u_component_of_wind.nc')[0]
    northward_wind = iris.load('data/v_component_of_wind.nc')[0]
    geopotential = iris.load('data/geopotential.nc')[0]

    # Add time categorization
    iris.coord_categorisation.add_hour(eastward_wind, 'time', name='hour_of_day')
    iris.coord_categorisation.add_hour(northward_wind, 'time', name='hour_of_day')
    iris.coord_categorisation.add_hour(geopotential, 'time', name='hour_of_day')

    # Find the wind speed
    windspeed = (eastward_wind ** 2 + northward_wind ** 2) ** 0.5
    windspeed.rename('windspeed')

    # Find the altitude from geopotential
    altitude = geopotential / 9.80665
    altitude.standard_name = "altitude"
    altitude.long_name = "Altitude"
    altitude.var_name = "h"
    altitude.units = Unit("meters")

    # Assemble data
    data = {
        "eastward_wind": eastward_wind,
        "northward_wind": northward_wind,
        "windspeed": windspeed,
        "altitude": altitude
    }

    # Display info
    print("\nData to use:")
    for k, v in data.items():
        print(v.summary())

    return data

if __name__ == '__main__':
    data = get_data()