# Data Science Senior Capstone - Viasat VPN Analysis

Given the fact that the user is connected to a VPN, our goal is to predict whether or not a user is streaming video by analyzing their network traffic traits such as packet size, packet arrival times, interpacket intervals, etc. Next, we engineer features for our dataset and utilize machine learning techniques, such as a classifier, to predict if there's video streaming present on the network. 

We use the `network-stats` tool from Viasat, which will output packet data on a per-second, per-connection basis from any given network interface. As you are browsing the internet or streaming video, `network-stats` will output the time, source IP, destination IP, protocol of all the packets in a flow. As an extended output, it will also produce the count, size, time, and direction of each packet within a flow.

## How to Run and Build the Project

Log on to DSMLP via `ssh <username>@dsmlp-login.ucsd.edu`

Clone this repository: `git clone https://github.com/JerryQian7/viasat-replication.git`

Now, you are ready to configure targets for our project build, via `python main.py <target(s)>`

## Targets

### generate


