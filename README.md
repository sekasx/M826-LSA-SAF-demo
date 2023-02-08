# M826-LSA-SAF-demo
Project repo for M826 Space Data Demo Processing for Space Exploration

## Install conda dependencies ##


````
conda install -n M826-LSA-SAF-processing -c conda-forge h5py matplotlib cartopy xarray, netCDF4, h5netcdf, pyyaml
````
Sometimes, the dependencies might need to be installed one-by-one. In that case, version mismatch may occur. 
In this case, by updating all dependencies fix the issue. This can be done with the following command:
````
conda update -n ENVIRONMENT --all
````


When using conda there is no easy way to store the dependencies in a file upon installation (like pipenv). 
This is why the conda env needs to be:
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
#### Linux

````
wget -c --no-check-certificate -r -np -nH \
     --user=XXX --password=XXX \
     -R "*15, *30, *45, *.html" \
     https://datalsasaf.lsasvcs.ipma.pt/PRODUCTS/MSG/DLST/HDF5/

````

#### Windows

While wget.exe can be downloaded, the execution is not always a 1-to-1 match with the Linux version.

The execution of the `download_LSA_SAF_archive.py` is an easy way to download the desired files,
that also gives greater flexibility that the wget command.

### Pre-steps

To execute the scripts, the LSA-SAF DLST product need to be accessible by the scripts, and the configuration file has to
be updated.

#### WebDav

The recommended option is to set up [WebDav](https://gitlab.com/helpdesk.landsaf/lsasaf_data_access/-/wikis/data/webdav)
to "map a network drive" pointing to this url: https://datalsasafwd.lsasvcs.ipma.pt/.
With this network drive you can copy&past, drag-and-drop as any other folder in your system. Files can be also accessed
directly from scripts (e.g. python script) running in the machine, pointing to the network path.

Ones the WebDav connection has been established, it is advised for better performance, to download the files in the
local hard drive

#### Configuration

To execute the script, the properties file need to be configured. The file is located in the directory `./src/resource`.

The format of the file is `properties-{env}.yml`

Where **{env}** is the environment variable that is given to the script upon execution.
The properties need to be configured are:

- base-dir - the local base directory with the different LSA-SAF collections
- input-data-dir - the directory with the collection that is going to be processed

### Execution

To execute the processing the command need to run

````
python main.py --env local-windows 
````



