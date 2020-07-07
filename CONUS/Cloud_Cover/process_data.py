import xarray as xr
import numpy as np

data_directory = 'data-medium'

# reanalyze = True
reanalyze = False

try:
    if not reanalyze:
        data = xr.open_dataset(f'{data_directory}/data_processed.nc')
        print("Loaded data from cache.")
except FileNotFoundError:
    reanalyze = True

if reanalyze:
    print("Analyzing...")
    # Pull in data from file
    data = xr.open_dataset(f'{data_directory}/data.nc')

    # Add the wind speed and altitude
    data = data.assign(
        windspeed=lambda x: (x.u ** 2 + x.v ** 2) ** 0.5,
        altitude=lambda x: (x.z / 9.80665)
    )

    # Get the effective cloud coverage above a point
    cc_overhead = np.zeros_like(data.cc)
    cc = data.cc.data
    for i in range(cc.shape[2]):  # latitude
        for j in range(cc.shape[3]):  # longitude
            for k in range(cc.shape[0]):  # time
                column = cc[k, :, i, j]  # extract a "column" at air at a fixed point in space & time

                column_cc_overhead = 0

                for l, cc_at_level in enumerate(column):  # pressure level
                    column_cc_overhead = max(column_cc_overhead, cc_at_level)

                    cc_overhead[k, l, i, j] = column_cc_overhead

    data = data.assign(
        cc_overhead=(data.cc.dims, cc_overhead)
    )

    data.to_netcdf(f"{data_directory}/data_processed.nc")
    print("Saved data to cache.")
