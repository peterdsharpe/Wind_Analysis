sampledata = 'http://dapds00.nci.org.au/thredds/dodsC/rr3/CMIP5/output1/CSIRO-BOM/ACCESS1-0/amip/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_ACCESS1-0_amip_r1i1p1_197901-200812.nc'

import xarray

# Open a file
data = xarray.open_dataset(sampledata)

# Variables can be accessed either as properties or as a dict
surface_temperature = data.tas
surface_temperature = data['tas']

print("Variable:\n", surface_temperature)

# Same for attributes
units = surface_temperature.units
units = surface_temperature.attrs['units']

print()
print("Attribute:\n", units)

# Variables can be indexed numpy-style or pandas-style
d = surface_temperature[0, 0:10, 0:10]
d = surface_temperature.isel(time=0, lat=slice(0,10), lon=slice(0,10))
d = surface_temperature.sel(time='19790116T1200', lat=slice(-90,-80), lon=slice(0,20))

# Data can be saved to a new file easily
data.to_netcdf('data.nc')