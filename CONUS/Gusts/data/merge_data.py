import os, sys
import xarray as xr

data_files = [
    file
    for file in os.listdir()
    if (".nc" in file) and ("data" not in file)
]

datasets = [
    xr.load_dataarray(file)
    for file in data_files
]

data = xr.merge(datasets)

data.to_netcdf("data.nc")