import glob
import os
import shutil

from src.main.helper.properties import load_properties


def main():
    properties = load_properties()

    webdav_dir = properties['webdav-dir']
    base_dir = properties['base-dir']
    data_dir = properties['data-dir']
    input_dir = os.path.join(base_dir, data_dir)

    dest_dir = input_dir
    hdf5_files = []

    print("Please wait. Loading remote files...")
    # Pattern matching all DLST-MED files, at 12:00 UTC
    pattern = f"{webdav_dir}\\**\\HDF5_LSASAF_MSG_DLST-MED10D_MSG-Disk_202208*1200"
    # Create a list with all the file names muching the pattern
    hdf5_files.extend(glob.glob(pattern, recursive=True))

    count = 0
    # Download files by Coping them to the Destination Folder in the local drive
    for file in hdf5_files:
        count += 1
        print(f"{100 * count // len(hdf5_files)}% -> coping file: {file}")
        shutil.copy(file, dest_dir)


if __name__ == "__main__":
    main()
