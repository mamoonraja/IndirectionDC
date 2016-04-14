# Indirection,

Below is the file structure for now, More details inside directories and modules

./
---Source_core/ 		  Main codes to run experiments and get results and parse them reside here
------main.py 			  runs different experiments defined by command line arguments
------Ping_experiments.py modules to run different kind of ping experiments defined here
------fetch_results.py    to fetch results of ping experiments and plot cdfs
------helpers.py          has helper functions used in the process of running experiments
------batch_ping.py       usually ran at remote host, and run pings to servers in input file

---data_files/          Data files to be used in different experiments are generated here
------ip_to_city.py 	module used to get location for IP address
------parse_links.py    Parser for iplane
------test_pings.py     module used to test different kind of pings and ssh

---misc/  
------top1m.csv        contains top 1m servers list by alexa

---Experments/         Contains results and plots for different experiments
