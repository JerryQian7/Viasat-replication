import pandas as pd
import glob
import os
import itertools
import numpy as np
import scipy
from scipy.signal import peak_prominences
import warnings
warnings.filterwarnings("ignore")

from feature_creation import split
from feature_creation import roll
from feature_creation import longest_dir_streak


def create_features(source_dir, out_dir, out_file, chunk_size, rolling_window_1, rolling_window_2, resample_rate, frequency):

    #remove files
    for f in glob.glob(os.path.join(out_dir, '*')):
        os.remove(f)

    #splitting dataframe into chunk_size'd chunks
    #chunk size is in milliseconds
    preprocessed_dfs = glob.glob(os.path.join(source_dir, 'preprocessed*'))
    split_df_groups = [split(f, chunk_size) for f in preprocessed_dfs]
    
    #flattening list
    merged = list(itertools.chain.from_iterable(split_df_groups))
    
    #0s and 1s indicating whether or not streaming is occurring
    merged_keys = [m[0] for m in merged]
    
    #the actual dataframes
    merged_dfs = [m[1] for m in merged]
    cols = ['b_ratio', 'p_ratio', 'delays_10', 'delays_60', 'psize_10', 'psize_60', 'sent_l_ratio', 'sent_s_ratio',
       'rec_l_ratio', 'rec_s_ratio', 'longest_sent', 'longest_rec', 'max_prom', 'streaming']

    features_df = pd.DataFrame(columns=cols, index=range(len(merged)))

    for i, df in enumerate(merged_dfs):
        df['dt_time'] = pd.to_timedelta(df['dt_time'])
        df = df.set_index('dt_time')
        df = df.drop(columns=['binned'])
        df = df.sort_values('time')

        #1 if streaming is ocurring, 0 if not
        streaming = merged_keys[i]

        #drop rows with any nan
        df = df.dropna(how='any')

        #flow level statistics
        sent_bytes = df[df['dir'] == 1]['size'].sum()
        received_bytes = df[df['dir'] == 2]['size'].sum()
        sent_packets = len(df[df['dir'] == 1])
        received_packets = len(df[df['dir'] == 2])

        #if there are no received bytes or packets, skip this chunk
        if received_bytes == 0 or received_packets == 0:
            continue

        #ratio of sent bytes over received bytes
        bytes_ratio = sent_bytes / received_bytes

        #ratio of sent packets over received packets
        packet_ratio = sent_packets / received_packets

        #ratios
        #large packet is defined as any packet size over 1200 byes
        #small packet is defined as any packet under 200 bytes
        sent_large = df[(df['dir']==1) & (df['size'] > 1200)]
        sent_small = df[(df['dir']==1) & (df['size'] < 200)]
        received_large = df[(df['dir']==2) & (df['size'] > 1200)]
        received_small = df[(df['dir']==2) & (df['size'] < 200)]
        
        #ratio of large, uploaded packets over all uploaded packets 
        sent_large_ratio = len(sent_large) / len(df[(df['dir']==1)])
        #ratio of small, uploaded packets over all uploaded packets
        sent_small_ratio = len(sent_small) / len(df[(df['dir']==1)])
        #ratio of large, downloaded packets over all downloaded packets
        received_large_ratio = len(received_large) / len(df[(df['dir']==2)])
        #ratio of small, downloaded packets over all downloaded packets
        received_small_ratio = len(received_small) / len(df[(df['dir']==2)])
        
        
        #interpacket delay
        df['ip_delay'] = df.index.to_series().diff().dt.total_seconds() * 1000
        df = df.dropna(how='any')

        #signal peak prominence using welch's method
        df_rs = df.resample(resample_rate).sum()
        f, Pxx_den = scipy.signal.welch(df_rs['size'], fs = frequency)
        peaks, _ = scipy.signal.find_peaks(np.sqrt(Pxx_den))
        prominences = peak_prominences(np.sqrt(Pxx_den), peaks)[0]
        try:
            df_max_prom = prominences.max()
        except:
            df_max_prom = 0
        print(df_max_prom)
        #interpacket delay means over rolling windows of 10 seconds and 60 seconds
        rolling_delays_10 = roll(df, 'ip_delay', rolling_window_1)['mean'].mean()
        rolling_delays_60 = roll(df, 'ip_delay', rolling_window_2)['mean'].mean()
        
        #print(roll(df, 'ip_delay', rolling_window_1))
        #packet size means over rolling windows of 10 seconds and 60 seconds
        packet_size_means_10 = roll(df, 'size', rolling_window_1)['mean'].mean()
        packet_size_means_60 = roll(df, 'size', rolling_window_2)['mean'].mean()
        
        #longest streaks
        longest_sent = longest_dir_streak(df['dir'], 1)
        longest_received = longest_dir_streak(df['dir'], 2)
        
        #downtime, longest time of no byte above 1200 bytes
        #downtime_sent_time = pd.Series(sent_large.index).dropna(how='any').diff().max().total_seconds()
        #downtime_received_time = pd.Series(received_large.index).dropna(how='any').diff().max().total_seconds()
            
        features = [bytes_ratio, 
                    packet_ratio, 
                    rolling_delays_10, 
                    rolling_delays_60, 
                    packet_size_means_10,
                    packet_size_means_60, 
                    sent_large_ratio, 
                    sent_small_ratio, 
                    received_large_ratio, 
                    received_small_ratio,
                    longest_sent, 
                    longest_received,
                    df_max_prom, 
                    #downtime_sent_time, downtime_received_time
                    streaming
                ]
        features_df.iloc[i] = features

    features_df.dropna().to_csv(os.path.join(out_dir, out_file))
    print('Features created: ', list(features_df.columns))

    

    

