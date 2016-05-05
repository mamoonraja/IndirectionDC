# Using Datacenter as Indirection point in mobility scenario  

How to make it work:
- to run experiments run 'python main.py 1 exptype expnum'
- to get results run 'python main.py 0 exptype expnum'
- to parse results run 'python main.py 2 exptype expnum'


Below is the file structure for project, More details inside directories and modules.  

./
README.md

---Source_core/           Main codes to run experiments and get results and parse them  
------main.py             runs different experiments defined by command line arguments  
------Ping_experiments.py modules to run different kind of ping experiments defined here  
------fetch_results.py    to fetch results of ping experiments and plot cdfs  
------helpers.py          has helper functions used in the process of running experiments  
------batch_ping.py       usually ran at remote host, and run pings to servers in input file  
------DC_list             List of Datacenters  
------DC_list_new         Updated list of Datacenters after we have to restart all the machines  
------active_nodes        PL_nodes used for 1st experiment, where only 10 planet lab nodes were used as pairs  
------Any_v3_node_list    List of filtered nodes from Iplane dataset  
------blacklisted         Pl nodes with problems not detected in filtering process # need to automate that  
------install_tcpping     script to install TCP ping on remote hosts  
------filtered_servers    list of filtered servers from ./../data_files/ directory, used for exp 3 and 4  
------servers             list of only 10 servers, used for initial experiments  
------future_work/        directory contains codes that can be used for throughput experiments  
------OLD/                some old results from starting stages, not very helpful though  
------Results*/           contains log files for experiments  
  
---data_files/            Data files to be used in different experiments are generated here  
------ip_to_city.py       module used to get location for IP address  
------parse_links.py      Parser for iplane  
------test_pings.py       module used to test different kind of pings and ssh  
------filter_servers.py   Used to filter servers and get top n servers  
  
---misc/  
------top1m.csv          contains top 1m servers list by alexa  
  
---Experiments/          Contains results and plots for different experiments  
