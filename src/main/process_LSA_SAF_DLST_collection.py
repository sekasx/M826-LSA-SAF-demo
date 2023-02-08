import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from src.main.helper.get_msg_col_lin import lat_lon2col_lin
from src.main.helper.get_msg_lat_lon import col_lin2lat_lon


def execute(properties):
    base_dir = properties['base-dir']
    data_dir = properties['input-data-dir']
    input_dir = os.path.join(base_dir, data_dir)

    mean_temps = []
    std_temps = []
    mean_times = []
    count = 0
    concat_ds = xr.Dataset()

    filenames = sorted([os.path.join(input_dir, filename) for filename in os.listdir(input_dir)])
    # filenames = filenames[1:10]
    for filename in filenames:
        count += 1
        print(f"{100 * count // len(filenames)}% {count} of {len(filenames)}, File Name: {filename}")

        product = read_product(filename)

        processed_product = crop_product(product)

        # Objective #1 create timeseries
        mean_temp, std_temp, mean_datetime = reduce_product(processed_product)
        mean_temps.append(mean_temp)
        std_temps.append(std_temp)
        mean_times.append(mean_datetime)

        # Objective #2 create composite image
        concat_ds = xr.concat([concat_ds, processed_product], dim='time')

        # Close the dataset
        product.close()
        processed_product.close()

    new_dataset = create_composite_with_mean_and_std(concat_ds)

    write_product(os.path.join(base_dir, "HDF5_COMPOSITE_2019_2022"), new_dataset)

    plot_timeseries_temperature(mean_temps, mean_times, std_temps)

    plot_product_image(new_dataset["LST_MEAN"], 'Mean Temperature')
    plot_product_image(new_dataset["LST_STD"], 'STD Temperature')


def read_product(file_name):
    # Read the HDF5 file
    xds = xr.open_dataset(file_name)
    # print(xds)
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


def crop_product(product):
    # Crop the data to the area of Greece
    min_lat = 34
    max_lat = 44
    min_lon = 19
    max_lon = 29

    COFF = product.COFF
    CFAC = product.CFAC
    LOFF = product.LOFF
    LFAC = product.LFAC

    # col,lin = lat_lon2col_lin(lat, lon, 0, COFF,LOFF,LFAC,CFAC)
    min_x, min_y = lat_lon2col_lin(max_lat, min_lon, 0, COFF, LOFF, LFAC, CFAC)
    max_x, max_y = lat_lon2col_lin(min_lat, max_lon, 0, COFF, LOFF, LFAC, CFAC)

    cropped_ds = product.sel(phony_dim_1=slice(min_x, max_x), phony_dim_0=slice(min_y, max_y))

    return cropped_ds


def reduce_product(cropped_ds):
    mean_temp = cropped_ds['LST_MED'].where(cropped_ds['LST_MED'] > -8000).mean()
    std_temp = cropped_ds['LST_MED'].where(cropped_ds['LST_MED'] > -8000).std()
    normalized_mean_temp = normalize_lst_value(mean_temp, cropped_ds['LST_MED'])
    normalized_std_temp = normalize_lst_value(std_temp, cropped_ds['LST_MED'])
    date_format = '%Y%m%d%H%M%S'
    mean_datetime = datetime.strptime(cropped_ds.IMAGE_ACQUISITION_TIME, date_format)
    print(f"Mean temp {normalized_mean_temp}")
    return normalized_mean_temp, normalized_std_temp, mean_datetime


def write_product(new_file_name, processed_product):
    # Write the cropped and processed data back to a .bz2 file
    processed_product.to_netcdf(new_file_name, format="NETCDF4", engine="h5netcdf")


def normalize_lst_value(value, band):
    return (value - band.OFFSET) / band.SCALING_FACTOR


def create_composite_with_mean_and_std(concat_ds):
    # Calculate the standard deviation for each pixel across all time steps
    new_dataset = concat_ds.LST_MED.mean(dim='time')
    new_dataset["LST_STD"] = concat_ds.LST_MED.copy().std(dim='time')
    # Set invalid values to -8000
    new_dataset["LST_STD"] = new_dataset["LST_STD"].where(new_dataset["LST_STD"] > 0, -8000)
    # concat_ds.LST_STD["name"] = 'LST_STD'
    new_dataset["LST_MEAN"] = concat_ds.LST_MED.copy().mean(dim='time')
    new_dataset["LST_MEAN"] = new_dataset["LST_MEAN"].where(new_dataset["LST_MEAN"] > 0, -8000)
    return new_dataset


def plot_timeseries_temperature(mean_temps, mean_times, std_temps):
    plt.plot(mean_times, mean_temps, label='Mean Temperature')
    plt.plot(mean_times, std_temps, label='STD Temperature')
    # plt.plot(mean_times, mean_temps, 'ro', label='Result 1')
    plt.legend()
    plt.xlabel('Date and time')
    plt.ylabel('Temperature C')
    plt.xticks(rotation=45)
    plt.gcf().set_dpi(300)
    plt.show()


def plot_product_image(dataset_array, title):
    flipped_std = np.flipud(dataset_array) / 100  # offset
    # Plot the flipped DataArray using imshow
    im = plt.imshow(flipped_std, origin='lower', cmap='viridis', vmin=-10, vmax=50)
    plt.colorbar(im)
    plt.title(title)
    plt.gcf().set_dpi(300)
    plt.show()
