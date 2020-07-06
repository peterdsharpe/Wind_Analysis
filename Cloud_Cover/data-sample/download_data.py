import cdsapi

c = cdsapi.Client()

# Get data from: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview

# Live monitor: https://cds.climate.copernicus.eu/live/queue

# Results mirror: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests

request = {
    'product_type'  : 'reanalysis',
    'format'        : 'netcdf',
    'variable'      : [
        'geopotential',
        'u_component_of_wind',
        'v_component_of_wind',
        'fraction_of_cloud_cover'
    ],
    'pressure_level': [
        '50', '125',
        # '1', '2', '3',
        # '5', '7', '10',
        # '20', '30', '50',
        # '70', '100', '125',
        # '150', '175', '200',
        # '225', '250', '300',
        # '350', '400', '450',
        # '500', '550', '600',
        # '650', '700', '750',
        # '775', '800', '825',
        # '850', '875', '900',
        # '925', '950', '975',
        # '1000',
    ],
    'area'          : [33.5, -107.5, 32.5, -106.5],  # north, west, south, east
    'grid'          : [1.0, 1.0],  # latitude/longitude grid resolution
    'year'          : [
        '1996', '2019'
        # '1979', '1980', '1981',
        # '1982', '1983', '1984',
        # '1985', '1986', '1987',
        # '1988', '1989', '1990',
        # '1991', '1992', '1993',
        # '1994', '1995', '1996',
        # '1997', '1998', '1999',
        # '2000', '2001', '2002',
        # '2003', '2004', '2005',
        # '2006', '2007', '2008',
        # '2009', '2010', '2011',
        # '2012', '2013', '2014',
        # '2015', '2016', '2017',
        # '2018', '2019', '2020',
    ],
    'month'         : [
        '07', '08'
        # '01', '02', '03',
        # '04', '05', '06',
        # '07', '08', '09',
        # '10', '11', '12',
    ],
    'day'           : [
        '15',
        # '01', '02', '03',
        # '04', '05', '06',
        # '07', '08', '09',
        # '10', '11', '12',
        # '13', '14', '15',
        # '16', '17', '18',
        # '19', '20', '21',
        # '22', '23', '24',
        # '25', '26', '27',
        # '28', '29', '30',
        # '31',
    ],
    'time'          : [
        '00:00', '12:00'
        # '00:00', '01:00', '02:00',
        # '03:00', '04:00', '05:00',
        # '06:00', '07:00', '08:00',
        # '09:00', '10:00', '11:00',
        # '12:00', '13:00', '14:00',
        # '15:00', '16:00', '17:00',
        # '18:00', '19:00', '20:00',
        # '21:00', '22:00', '23:00',
    ],
}
### One file
print("\nDownloading as one file.")
c.retrieve(
    'reanalysis-era5-pressure-levels',
    request,
    f'data.nc'
)

### Separate files
# print("\nDownloading as separate files.")
# vars_to_download = request['variable']
# for variable in vars_to_download:
#     print("\nSending API request for %s" % variable)
#     request['variable'] = variable
#     c.retrieve(
#         'reanalysis-era5-pressure-levels',
#         request,
#         f'{variable}.nc'
#     )
