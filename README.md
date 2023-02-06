# M826-LSA-SAF-demo
Project repo for M826 Space Data Demo Processing for Space Exploration

## Install conda dependencies ##


````
conda install -n M826-LSA-SAF-processing -c conda-forge h5py matplotlib cartopy xarray, netCDF4, h5netcdf
````

When using conda there is no easy way to store the dependencies in a file upon installation. This is why the conda env needs to be:
- exported
- committed to the repo
- import it to the new environment 

### Conda Export environment
````
conda env export -n M826-LSA-SAF-processing -f environment.conda.yaml
````

### Conda Import environment
````
conda env create -n M826-LSA-SAF-processing -f environment.conda.yaml
````


## Download LSA-SAF data
````
wget -c --no-check-certificate -r -np -nH \
     --user=XXX --password=XXX \
     -R "*15, *30, *45, *.html" \
     https://datalsasaf.lsasvcs.ipma.pt/PRODUCTS/MSG/DLST/HDF5/

````
