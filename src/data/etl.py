import pandas as pd
import glob
import os


def etl(source_dir, out_dir):
    
    if not os.path.exists(source_dir):
        symlink_dir = "/teams/DSC180A_FA20_A00/b05vpnxray/GoodData/"

        os.symlink(symlink_dir, source_dir)
    
    
    datafiles = glob.glob(os.path.join(source_dir, "*"))
    print((datafiles))