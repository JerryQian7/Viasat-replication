import pandas as pd
import glob
import os
import pathlib
import itertools

from preprocess import isolate_vpn
from preprocess import unpack
from preprocess import packet_data


DATA_DIRECTORY = "/teams/DSC180A_FA20_A00/b05vpnxray/GoodData"

def etl(source_dir, out_dir):

    source_path = pathlib.Path(source_dir)
    out_path = pathlib.Path(out_dir)
    
    # Ensure source exists. If not then we'll create it with symlinking.
    if not source_path.exists():

        # Create the parents. It's important we don't make the final directory
        # otherwise the symlink will fail since it already exists!
        source_path.parent.mkdir(parents=True, exist_ok=True)

        # Symlink data to make our source directory
        print(f"Symlinking {source_path} to raw data from {DATA_DIRECTORY}")
        source_path.symlink_to(
            pathlib.Path(DATA_DIRECTORY), target_is_directory=True
        )

    # Ensure out directory exists.
    out_path.mkdir(parents=True, exist_ok=True)
        
    # Clean out existing preprocessed files.
    for fp in out_path.iterdir():
        fp.unlink()
    
    # We're only working with data which used a VPN, so we can ignore the rest.
    file_lst = [
        fp
        for fp in source_path.iterdir()
        if 'novpn' not in fp.name
    ]

    for filepath in file_lst:
        #reading in each dataframe
        df = pd.read_csv(filepath)
        
        #filtering any non vpn connection rows
        df = isolate_vpn(df)

        #splitting data into packet level data
        df = df.apply(packet_data, axis=1)
        df = pd.DataFrame(df.sum(), columns = ['time','size','dir']).astype(int)
        df = df.sort_values('time')

        #setting index as timedelta in milliseconds
        df['dt_time'] = pd.to_timedelta(df.time - df.time[0], 'ms')
        df = df.set_index('dt_time')

        df.to_csv(os.path.join(out_dir, 'preprocessed-'+filepath.name))