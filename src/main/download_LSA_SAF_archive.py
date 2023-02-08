import glob
import shutil

webdav_dir = "Z:\\PRODUCTS\\MSG\\DLST\\HDF5"
dest_dir = "C:\\Users\\sekas\\projects\\M826-LSA-SAF-demo\\data\\DLST-HDF5"
hdf5_files = []

# Pattern matching all DLST-MED files, at 12:00 UTC
pattern = f"{webdav_dir}\\**\\HDF5_LSASAF_MSG_DLST-MED10D_MSG-Disk_*1200"
# Create a list with all the file names muching the pattern
hdf5_files.extend(glob.glob(pattern, recursive=True))

count = 0
# Download files by Coping them to the Destination Folder in the local drive
for file in hdf5_files:
    count += 1
    print(f"{100 * count // len(hdf5_files)}% -> coping file: {file}")
    shutil.copy(file, dest_dir)
