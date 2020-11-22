import pandas as pd
import glob
import os
import itertools

from feature_creation import split
from feature_creation import roll
from feature_creation import longest_dir_streak


def create_features(source_dir, out_dir, out_file, chunk_size):

    preprocessed_dfs = glob.glob(os.path.join(source_dir, 'preprocessed*'))
            
    split_df_groups = [split(f, chunk_size) for f in preprocessed_dfs]
    #flattening list
    merged = list(itertools.chain.from_iterable(split_df_groups))
    merged_keys = [m[0] for m in merged]
    merged_dfs = [m[1] for m in merged]
    cols = ['b_ratio', 'p_ratio', 'delays_10', 'delays_60', 'psize_10', 'psize_60', 'sent_l_ratio', 'sent_s_ratio',
       'rec_l_ratio', 'rec_s_ratio', 'longest_sent', 'longest_rec', 'streaming']

    features_df = pd.DataFrame(columns=cols, index=range(len(merged)))
    print(len(merged_keys))
    print(len(merged_dfs))
    for i, df in enumerate(merged_dfs):
        streaming = merged_keys[i]
        df = df.dropna(how='any')
        #flow level statistics
        sent_bytes = df[df['dir'] == 1]['size'].sum()
        received_bytes = df[df['dir'] == 2]['size'].sum()
        sent_packets = len(df[df['dir'] == 1])
        received_packets = len(df[df['dir'] == 2])
        if received_bytes == 0 or received_packets == 0:
            continue
        bytes_ratio = sent_bytes / received_bytes
        packet_ratio = sent_packets / received_packets
        
        #packet level statistics 

        #interpacket delay
        df = df.sort_values('time')
        df['ip_delay'] = df['time'].diff()
        df = df.dropna(how='any')
        
        #interpacket delay means over rolling windows of 10 and 60
        rolling_delays_10 = roll(df, 'ip_delay', 10)['mean'].mean()
        rolling_delays_60 = roll(df, 'ip_delay', 60)['mean'].mean()
        
        #packet size means over rolling windows of 10 and 60
        packet_size_means_10 = roll(df, 'size', 10)['mean'].mean()
        packet_size_means_60 = roll(df, 'size', 60)['mean'].mean()
        
        #ratios
        sent_large = df[(df['dir']==1) & (df['size'] > 1200)]
        sent_small = df[(df['dir']==1) & (df['size'] < 200)]
        received_large = df[(df['dir']==2) & (df['size'] > 1200)]
        received_small = df[(df['dir']==2) & (df['size'] < 200)]
        
        try:
            sent_large_ratio = len(sent_large) / len(df[(df['dir']==1)])
            sent_small_ratio = len(sent_small) / len(df[(df['dir']==1)])
            received_large_ratio = len(received_large) / len(df[(df['dir']==2)])
            received_small_ratio = len(received_small) / len(df[(df['dir']==2)])
        except:
            continue
        
        #longest streaks
        longest_sent = longest_dir_streak(df['dir'], 1)
        longest_received = longest_dir_streak(df['dir'], 2)
        
        #downtime, longest time of no byte above 1200 bytes
        #downtime_sent_time = pd.Series(sent_large.index).dropna(how='any').diff().max().total_seconds()
        #downtime_received_time = pd.Series(received_large.index).dropna(how='any').diff().max().total_seconds()
            
        features = [bytes_ratio, packet_ratio, 
                    rolling_delays_10, 
                    rolling_delays_60, 
                    packet_size_means_10,
                packet_size_means_60, 
                    sent_large_ratio, sent_small_ratio, received_large_ratio, received_small_ratio,
                longest_sent, longest_received, 
                    #downtime_sent_time, downtime_received_time
                    streaming
                ]
        features_df.iloc[i] = features
    
    features_df.dropna().to_csv(os.path.join(out_dir, out_file))

    

    

