#%%
import sys
sys.path.append('D:\\pyutils')
import os
from netCDF4 import Dataset
from glob import glob
import pygrib
import numpy as np
import tarfile
import shutil
from read_nc import save_nc
from datetime import datetime
from datetime import timedelta
#%%
gfs_dir = 'E:\\gfs'
gfs_dir = 'D:\\Doutorado\\GFS'
tar_files = glob(f'{gfs_dir}\\*.tar')
ref_date = datetime(2000, 1, 1)
data_year = '2010'
#%%
for tar_file in tar_files:

#%%
    print(tar_file)
    # unpacking tar files
    with tarfile.open(tar_file) as my_tar:
        my_tar.extractall(f'{gfs_dir}\\unpacked')

    grib_files = glob(f'{gfs_dir}\\unpacked\\*.grb2')
#%%
    pr = []

    for grib_file in grib_files:
        print('\t --', grib_file)
        grbs = pygrib.open(grib_file)                     # open grib file
        grb = grbs.select(name='Precipitable water')[0]     # reading grib with precitation
        data, lats, lons = grb.data()                     # reading data, latitude and longitude
        pr.append(data)
        grbs.close()
    
    shutil.rmtree(f'{gfs_dir}\\unpacked')
    pr = np.array(pr)
#%%
    start_date  = grib_file.split('_')[2]
    start_date = datetime.strptime(start_date, '%Y%m%d')
    diff_dates = (start_date - ref_date).total_seconds() / 3600
    hours_since_ref = [diff_dates + i for i in range(0, len(pr)*3, 3)]
    filename = '_'.join(grib_file.split('_')[1:4])
    filename = f"{gfs_dir}\\netcdfs\\{data_year}\\gfs_pr_{filename}.nc"
    time_units = 'hours since 2000-01-01'
    var_name = 'pr'
    var_units = 'mm/day'
    var_long_name = 'milemeters per day'
    lons = lons[0]
    lats = lats[:,0]
    save_nc(pr, lats, lons, hours_since_ref, filename, time_units, var_name, 
            var_units, var_long_name)
#%%
