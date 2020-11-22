import pandas as pd
import glob
import os
import itertools

from preprocess import isolate_vpn
from preprocess import unpack
from preprocess import packet_data


def etl(source_dir, out_dir):
    
    if not os.path.exists(source_dir):
        #need to figure out why python os.symlink didn't work but ln -s worked
        symlink_dir = "/teams/DSC180A_FA20_A00/b05vpnxray/GoodData"

        os.symlink(symlink_dir, source_dir)    
        #do a os command to run ln -s   
        datafiles = glob.glob('data/raw/GoodData/*')
        file_lst = [l for l in datafiles if 'novpn' not in l]

    else:
        #test data
        file_lst = glob.glob(source_dir + '*')

    #remove files
    for f in glob.glob(os.path.join(out_dir, '*')):
        os.remove(f)

    for filename in file_lst:
        print(filename)
        df = pd.read_csv(filename)
        df = isolate_vpn(df)
        df = df.apply(packet_data, axis=1)
        df = pd.DataFrame(df.sum(), columns = ['time','size','dir'])
        df = df.apply(pd.to_numeric)

        filename = os.path.basename(filename)
        df.to_csv(os.path.join(out_dir, 'preprocessed-'+filename))