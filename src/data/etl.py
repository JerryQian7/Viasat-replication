import pandas as pd
import glob
import os


def etl(source_dir, out_dir):
    
    if not os.path.exists(source_dir):
        #need to figure out why python os.symlink didn't work but ln -s worked
        symlink_dir = "/teams/DSC180A_FA20_A00/b05vpnxray/GoodData"

        os.symlink(symlink_dir, source_dir)
    
    
    datafiles = glob.glob('data/raw/GoodData/*')
    print((datafiles))