import pandas as pd
import numpy as np
#IP ranges to filter out
internal_ranges = ('10.0.', '0.0.', '172.16.', '192.168.', '169.254.')
multicast_ranges = tuple(str(i)+'.' for i in range(224,239+1))
broadcast_ranges = ('255.',)
hopbyhop_protocol = 0

internal_comm = lambda df: (
    (df.IP1.str.startswith(internal_ranges))
    & (df.IP2.str.startswith(internal_ranges))
)
multicast_comm = lambda df: (
    (df.IP2.str.startswith(multicast_ranges))
)
broadcast_comm = lambda df: (
    (df.IP2.str.startswith(broadcast_ranges))
)
hopbyhop_comm = lambda df: (
    df.Proto == hopbyhop_protocol
)

def isolate_vpn(df):
    """
    Returns flows between client service and VPN service.
    """
    return df[
        ~internal_comm(df)
        & ~multicast_comm(df)
        & ~broadcast_comm(df)
        & ~hopbyhop_comm(df)
    ]

def unpack(s):
    """
    Splitting packet sizes and times into individual values.
    """
    s_unpacked = s[:-1].split(';')
    s_unpacked = [eval(i) for i in s_unpacked]
    return s_unpacked

def packet_data(row):
    """
    Unpack flow level data into packet level data
    """
    unpacked_data = []
    times = unpack(row['packet_times'])
    sizes = unpack(row['packet_sizes'])
    dirs = unpack(row['packet_dirs'])
    entry = [list(a) for a in zip(times,sizes,dirs)]
    return entry