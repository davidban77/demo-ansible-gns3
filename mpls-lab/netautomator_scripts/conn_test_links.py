#!/usr/bin/env python

DOCUMENTATION = """
---
The script provide a connectivity link test by using Netmiko from netautomator to connect to the network devices and run ping test against their peers on each interface configured previously by Ansible.
this script have to run from the netautomator after do a git clone to the repository.
the script is intended to run from the folder/demo-ansible-gns3/mpls-lab/netautomator_scripts
reason for some hard-coded data in the code
"""

EXAMPLES = """
# python conn_test_links.py
"""

RETURN = """
A Dictionary with all the ping results from each interface per device as follows:
password for network devices:
Starting tests.............
{'cae-1': {'Gi0/1': 'Type escape sequence to abort.\n'
                    'Sending 5, 100-byte ICMP Echos to 70.0.0.1, timeout is 2 '
                    'seconds:\n'
                    '.!!!!\n'
                    'Success rate is 80 percent (4/5), round-trip min/avg/max '
                    '= 2/8/23 ms',
           'Gi0/3': 'Type escape sequence to abort.\n'
                    'Sending 5, 100-byte ICMP Echos to 70.0.3.2, timeout is 2 '
                    'seconds:\n'
                    '.!!!!\n'
                    'Success rate is 80 percent (4/5), round-trip min/avg/max '
                    '= 2/2/4 ms'
"""
import yaml
import time
from netmiko import Netmiko
from pprint import pprint
from netaddr import IPNetwork
from getpass import getpass

# initial hosf location file 
location = "../extra/hosts_file.conf"

# getting networks devices password --Assuming is the same for all the devices...
while True:
    pwd = getpass(prompt="password for network devices:")
    if pwd != "":
        print("Starting tests.............")
        break

# reading yamls
def doc_read(location):
    with open(location, "r") as f:
        data = yaml.safe_load(f)
        return data

# get Peer ip on the link --> address has to be of type IPNetwork
def get_peer_ip(address):
    for host in address.iter_hosts():
        if address.ip != host:
            return host


def conn_link_tests(data):
    results = dict()
    for host, mgmt_ip in data.items():
        host_response = {}
        # creating netmiko connector
        net_connect = Netmiko(
            mgmt_ip, username="netops", password=pwd, device_type="cisco_ios",
        )

        loc = "../inventory/host_vars/" + host + ".yml"
        parsed_host_data = doc_read(loc)
        # rurnning the test:
        for interface in parsed_host_data["interfaces"]:
            if interface["interface"] != "loopback0":
                target = str(get_peer_ip(IPNetwork(interface["ip"])))
                host_response.update(
                    {interface["interface"]: net_connect.send_command(f"ping {target}")}
                )
                time.sleep(2)
                # testing with names, netmiko test will be from netautomator
                # host_response.update({interface["interface"]:target})
        results.update({host: host_response})
    return results


def main():
    ## inventory data
    data = doc_read("../extra/hosts_file.conf")
    pprint(conn_link_tests(data))

if __name__ == '__main__':
    main()
