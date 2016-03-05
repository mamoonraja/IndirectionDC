# Indirection
Source files contains scripts we will use for measurement study for the project,overhead of using Data centers as indirection point. 
Scripts are not final yet. 

fetch_node_list.py  used to get required node from dpip-city dataset
Ping_experiments.py modules to run different kind of ping experiments defined here
fetch_results.py    to fetch results of ping experiments
helpers.py   has helper functions used in the process of running experiments
runall.py    will run different experiments

//still need to be updated based on results, not final
udp_send.py  will send packet directly to destination and also to nearest datacenter, discovery of neearest data center is automated now.
udp_rec.py   will listen on specified port and log entries
udp_dc.py    will act as indirection point # change logging method here, 

//next step: one big experiment to latency benefits using approx 200 nodes, using zmap or king 
