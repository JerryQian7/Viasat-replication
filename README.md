# Data Science Senior Capstone - Viasat VPN Analysis

## Purpose

Our goal is to predict whether a user is streaming video on a VPN by analyzing their network traffic traits such as video signatures, interpacket intervals, packet size, etc. through a machine learning classifier, then repeat the analysis with other noise present on the network.

Our data collection process uses the network-stats script from Viasat, which will output packet data on a per-second, per-connection basis from any given network interface. This tool was designed to focus more on connection-to-connection data rather than individual packet data. Once running, network-stats will output the time, source, destination, and protocol of the packets sent within any connection, as well as the count, size, time, and direction of each packet’s arrival at the destination.

