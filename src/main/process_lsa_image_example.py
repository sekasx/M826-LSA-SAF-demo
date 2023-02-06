# Required package to load data
import h5py
import numpy as np
import os
import datetime as dt
import xarray as xr


# Required packages for ploting
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature.nightshade import Nightshade
import warnings

from src.main.helper.get_msg_col_lin import lat_lon2col_lin


def lsa_example():
    # open the hdf5 file with h5py
    # Assuming the WebDAV was maped into drive "Z:\" / or replace with local drive if file was downloaded
    # use os.path.join to avoid windows/linux problems
    # slot = dt.datetime(2022, 9, 21, 0, 0)
    slot=dt.datetime(2021,8,2,15,15)

    # example for MSG
    # file_path = os.path.join('Z:', 'PRODUCTS', 'MSG', 'MDSSFTD', 'HDF5',
    #                          slot.strftime("%Y"), slot.strftime("%m"), slot.strftime("%d"),
    #                          'HDF5_LSASAF_MSG_MDSSFTD_MSG-DISK_' + slot.strftime("%Y%m%d%H%M"))
    # # example for MSG-IODC
    # file_path = os.path.join('Z:', 'PRODUCTS', 'MSG-IODC', 'MDSSFTD', 'HDF5',
    #                          slot.strftime("%Y"), slot.strftime("%m"), slot.strftime("%d"),
    #                          'HDF5_LSASAF_MSG-IODC_MDSSFTD_IODC-Disk_' + slot.strftime("%Y%m%d%H%M"))


    # example for MSG-IODC
    file_path = os.path.join('C:\\', 'Users', 'sekas', 'Downloads',
                             'HDF5_LSASAF_MSG_MDSSFTD_MSG-Disk_' + slot.strftime("%Y%m%d%H%M"))
                             # 'HDF5_LSASAF_MSG_DLST-MAX10D_MSG-Disk_' + slot.strftime("%Y%m%d%H%M"))

    # open file
    h5 = h5py.File(file_path, 'r')

    ds = xr.open_dataset(file_path)
    print(ds)

    # print datasets in file

    print("====Datasets in file====")
    for k in h5.keys():
        print(k, h5[k])

    # print global attributes
    print("====Global Attributes====")
    for k in h5.attrs.keys():
        print(k, h5.attrs[k])

    vname = 'DSSF_TOT'
    # vname = 'LST_MAX'
    # print variable attributes
    for k in h5[vname].attrs.keys():
        print(k, h5[vname].attrs[k])

    # Load variable
    zvar = h5[vname][:, :]
    miss_val = h5[vname].attrs['MISSING_VALUE']
    scalling = h5[vname].attrs['SCALING_FACTOR']
    offset = h5[vname].attrs['CAL_OFFSET']
    zvar = offset + np.ma.masked_equal(zvar, miss_val) / scalling
    central_longitude = h5.attrs['NOMINAL_LONG']  #
    COFF = h5.attrs['COFF']
    CFAC = h5.attrs['CFAC']
    LOFF = h5.attrs['LOFF']
    LFAC = h5.attrs['LFAC']
    h5.close()  # close file here

    print(slot)

    # Create a simple plot of the variable

    # to avoid showing warnings of cartopy
    warnings.filterwarnings('ignore')

    # Define the coordinate reference system (CRS) for the data
    data_crs = ccrs.Geostationary(central_longitude=central_longitude, satellite_height=42171 * 1000.)

    lat = 37.98
    lon = 23.72
    col,lin = lat_lon2col_lin(lat, lon, 0, COFF,LOFF,LFAC,CFAC)

    print("line: ", lin, " col: ", col)

    # Create a Matplotlib axis object with a Geostationary CRS and a white background
    ax = plt.axes(projection=data_crs, facecolor='white')
    # Get the extent of the image in the Geostationary CRS
    map_extend_geos = ax.get_extent(crs=data_crs)
    # Apply a correction to the extent to correctly display the image
    map_extend_geos = [1.025 * x for x in map_extend_geos]  # needs this correction because image gets shifted
    # ax.coastlines()
    ax.add_feature(cfeature.OCEAN, facecolor='lightgray')
    ax.gridlines(color='black', alpha=0.5, linestyle='--', linewidth=0.75, draw_labels=False)
    im1 = ax.imshow(zvar, interpolation='nearest', origin='upper', extent=map_extend_geos, )
    cb = plt.colorbar(im1, shrink=0.7)
    ax.add_feature(Nightshade(slot, alpha=0.2))

    plt.gcf().set_dpi(1000)
    # plt.gcf().set_dpi(1000)
    plt.show()


    print('END')