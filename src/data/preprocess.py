import pandas as pd
import numpy as np



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
    Attempts to find which IP belongs to the client machine. Works by ignoring
    all internal network communications, multicasts, and broadcasts. The local
    address will always be in the IP1 column due to how network-stats works, and
    this method should be enough to narrow IP1 down to one address. In the event
    that multiple addresses are still present, the most frequent address is
    assumed to belong to the client.
    """
    return df[
        ~internal_comm(df)
        & ~multicast_comm(df)
        & ~broadcast_comm(df)
        & ~hopbyhop_comm(df)
    ]

def unpack(s):
    s_unpacked = s[:-1].split(';')
    s_unpacked = [eval(i) for i in s_unpacked]
    return s_unpacked

def packet_data(row):
    unpacked_data = []
    times = unpack(row['packet_times'])
    sizes = unpack(row['packet_sizes'])
    dirs = unpack(row['packet_dirs'])
    entry = [list(a) for a in zip(times,sizes,dirs)]
    return entry