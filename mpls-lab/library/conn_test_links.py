# Krlosromero 20200321,test link connectivity
import yaml
import time
from netmiko import Netmiko  
from pprint import pprint
from netaddr import IPNetwork

# initial hosf location file --> it should be with args
location = '../extra/hosts_file.conf'

# reading yamls
def doc_read(location):
    with open(location, 'r') as f:
        data = yaml.load(f)
        return(data)

# get Peer ip on the link --> address has to be of type IPNetwork
def get_peer_ip(address):
    for host in address.iter_hosts():
        if address.ip != host:
            return host

def conn_link_tests(data):
    results = dict()
    for host,mgmt_ip in data.items(): 
        host_response = {}
        # creating netmiko connector
        net_connect = Netmiko(mgmt_ip, username="netops", password="netops123456",   device_type="cisco_ios",)

        loc = "../inventory/host_vars/"+host+".yml"    
        parsed_host_data = doc_read(loc)
        # rurnning the test:
        for interface in parsed_host_data["interfaces"]:
            if interface["interface"] != "loopback0":
                target = str(get_peer_ip(IPNetwork(interface["ip"])))
                host_response.update({interface["interface"]:net_connect. send_command(f"ping {target}")})
                time.sleep(2)
                # testing with names, netmiko test will be from netautomator
                # host_response.update({interface["interface"]:target})  
        results.update({host: host_response})
    return(results)

def main():
    ## inventory data
    data = (doc_read('../extra/hosts_file.conf'))
    pprint(conn_link_tests(data))

main()




 

