import xarray as xr
import os
import numpy as np

from src.main.helper.get_msg_col_lin import lat_lon2col_lin
from src.main.helper.get_msg_lat_lon import col_lin2lat_lon


def read_product(file_name):

    # Open the .bz2 HDF5 file in the DIMAP format

    xds = xr.open_dataset(file_name, engine="h5netcdf")

    print(xds)
    return xds


# It has a bug
def add_coordinates(product):

    COFF = product.COFF
    CFAC = product.CFAC
    LOFF = product.LOFF
    LFAC = product.LFAC
    sub_lon = 0

    # Get the values of the pixel count dimensions
    phony_dim_0 = product['phony_dim_0'].values
    phony_dim_1 = product['phony_dim_1'].values

    # Create arrays for latitude and longitude
    latitude = np.zeros_like(phony_dim_0)
    longitude = np.zeros_like(phony_dim_1)

    # Loop through the pixel count values and calculate the latitude and longitude
    for i, (col, lin) in enumerate(zip(phony_dim_0, phony_dim_1)):
        coords = col_lin2lat_lon(col, lin, sub_lon, COFF, LOFF, LFAC, CFAC)
        if coords is None:
            latitude[i] = 100000
            longitude[i] = 100000
        else:
            lat, lon = coords
            latitude[i] = lat
            longitude[i] = lon

    # Create a new dimension for latitude and longitude
    product['latitude'] = xr.DataArray(latitude, dims='phony_dim_0')
    product['longitude'] = xr.DataArray(longitude, dims='phony_dim_1')

# -----------------------------------------------------------------------------------------------

    return product


def process(product):

    # Crop the data to the Attica, Greece area
    min_lat = 34
    max_lat = 44
    min_lon = 19
    max_lon = 29
    min_x = 2350
    max_x = 2600
    min_y = 530
    max_y = 730

    COFF = product.COFF
    CFAC = product.CFAC
    LOFF = product.LOFF
    LFAC = product.LFAC

    # col,lin = lat_lon2col_lin(lat, lon, 0, COFF,LOFF,LFAC,CFAC)
    min_x, min_y = lat_lon2col_lin(max_lat, min_lon, 0, COFF,LOFF,LFAC,CFAC)
    max_x, max_y = lat_lon2col_lin(min_lat, max_lon, 0, COFF,LOFF,LFAC,CFAC)

    # product = add_coordinates(product)
    # ds_cropped = product.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
    cropped_ds = product.sel(phony_dim_1=slice(min_x, max_x), phony_dim_0=slice(min_y, max_y))
    mean_temp = cropped_ds['LST_MAX'].where(cropped_ds['LST_MAX'] > -8000).mean()
    print(normalize_lst_value(mean_temp, product['LST_MAX']))

    # # Subtract the mean temperature from each pixel
    # mean_temp = product['LST_MAX'].where(product['LST_MAX'] > -8000).mean()
    # print(normalize_lst_value(mean_temp, product['LST_MAX']))
    # # value = product.sel(lat=min_lat, lon=min_lon, method='nearest')['LST_MAX'].values[0]
    # value = product.sel(phony_dim_0=slice(10, 2000), phony_dim_1=slice(10, 2000))['LST_MAX']
    # print( value)
    # product['LST_MAX'] = product['LST_MAX'] - mean_temp

    return cropped_ds


def write_product(new_file_name, processed_product):
    # Write the cropped and processed data back to a .bz2 file
    processed_product.to_netcdf(new_file_name, format="NETCDF4", engine="h5netcdf")

def normalize_lst_value(value, band):
    return (value - band.OFFSET)/band.SCALING_FACTOR

def execute(properties):
    file_name = "HDF5_LSASAF_MSG_DLST-MAX10D_MSG-Disk_201710110015"
    product = read_product(file_name)

    processed_product = process(product)

    write_product(file_name+"_processed", processed_product)

    # Close the dataset
    product.close()
    print("Hello World!")