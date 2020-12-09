import sys
import os

#python3.8 network_stats.py -i en0 -s -e jeq004-novideo-vpn-20201128.csv

def collect_data(params):
    """
    Captures data from network_stats
    """
    username = params['username']
    provider = params["provider"]
    quality = params["quality"]
    speed = params["speed"]
    vpn = params["vpn"]
    platform = params["platform"]
    clean = params["clean"]
    date = params["date"]
    interface = params["interface"]
    csvmode = params["csvmode"]
    path = params['path']
    output_path = './data/collected/'

    output_file = '{}_{}_{}_{}_{}_{}_{}_{}.csv'.format(username, provider, quality, speed, vpn, platform, clean, date)
    command = 'python3.8 {} -i {} -s {} {}'.format(path, interface, csvmode, output_file)
    os.system(command)
    
    return