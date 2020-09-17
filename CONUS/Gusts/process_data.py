import xarray as xr
import numpy as np

data_directory = 'data'

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
    cc = data.cc
    data = data.assign(
        cc_overhead=lambda x: 0 * x.cc
    )

    sheet = data.cc_overhead.isel(level=0) # A "sheet" of air at a particular pressure level, across space and time

    for i, level in enumerate(cc.coords["level"].data[1:]):
        sheet = xr.ufuncs.maximum(
            sheet, # the atmosphere sheet above us
            data.cc.isel(level=i), # the cloud cover at our current pressure level
        )
        data.cc_overhead.loc[dict(level=level)] = sheet

    # Compute the vertical velocity in m/s, not Pa/s
    import aerosandbox.library.atmosphere as atmo

    altitudes = data.altitude.mean(
        dim=["latitude", "longitude", "time"]
    ).data
    densities = xr.DataArray(
        np.array(atmo.get_density_at_altitude(altitudes)).flatten(),
        coords={
            "level": data.coords["level"]
        },
        dims=[
            "level"
        ]
    )
    dPdh = -densities * 9.80665
    w_m_s = data.w / dPdh

    data = data.assign(
        w_m_s=(data.w.dims, w_m_s)
    )

    data.to_netcdf(f"{data_directory}/data_processed.nc")
    print("Saved data to cache.")
