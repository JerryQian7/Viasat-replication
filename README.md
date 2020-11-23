# Data Science Senior Capstone - Viasat VPN Analysis

Given the fact that the user is connected to a VPN, our goal is to predict whether or not a user is streaming video by analyzing their network traffic traits such as packet size, packet arrival times, interpacket intervals, etc. Next, we engineer features for our dataset and utilize machine learning techniques, such as a classifier, to predict if there's video streaming present on the network. 

We use the `network-stats` tool from Viasat, which will output packet data on a per-second, per-connection basis from any given network interface. As you are browsing the internet or streaming video, `network-stats` will output the time, source IP, destination IP, protocol of all the packets in a flow. As an extended output, it will also produce the count, size, time, and direction of each packet within a flow.

## How to Run and Build the Project

Log on to DSMLP via `ssh <username>@dsmlp-login.ucsd.edu`

Launch a Docker container with the necessary components via `launch-180.sh -i jeq004/viasat-replication -G B05_VPN_XRAY`

Clone this repository: `git clone https://github.com/JerryQian7/viasat-replication.git`

Navigate to this repository `cd viasat-replication`

Now, you are ready to configure targets for our project build, via `python main.py <target(s)>`. Details are specified below.

## Targets

### generate
Generates data from the `network-stats` tool by capturing your network interface activity. Settings such as the network interface, output type, and file naming convention can be configured in `config/data-generation-params`.

`Ctrl-C` to stop data generation.

### data
This target will prepare the data by loading it from a source directory, cleaning and filtering the data, and saving the preprocessed the data to an output directory.

You can configure the source and output directories in 'config/etl-params'. By default, and when not using test data, the source directory will be `data/raw` and the output directory will be `data/preprocessed`.

### features
Engineers features on the preprocessed data and saves to an output directory, which can be configured in `config/feature-params`. Other feature parameters such as chunk size and rolling window lengths can also be configured. 


### train
Trains a classifier based on the new features and outputs the accuracy between the predicted and true labels. In other words, it prints out the percentage of cases that were correctly classified as streaming.








