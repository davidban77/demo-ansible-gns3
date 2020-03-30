#!/usr/bin/env python
"""
---
The script provide a connectivity link test by using Netmiko from netautomator to
connect to the network devices and run ping test against their peers on each interface
 configured previously by Ansible.
this script have to run from the netautomator after do a git clone to the repository.
the script is intended to run from the folder/demo-ansible-gns3/mpls-lab/
netautomator_scripts
reason for some hard-coded data in the code

Example:
# python conn_test_links.py

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
import os
import yaml
from netmiko import Netmiko
from netaddr import IPNetwork
from getpass import getpass, getuser
from tabulate import tabulate

NET_DEVICE_USER = os.getenv("NET_DEVICE_USER")
NET_DEVICE_PASSWORD = os.getenv("NET_DEVICE_PASSWORD")


def get_creds():
    user = NET_DEVICE_USER if NET_DEVICE_USER is not None else getuser()
    pwd = (
        NET_DEVICE_PASSWORD
        if NET_DEVICE_PASSWORD is not None
        else getpass(prompt="password for network devices:")
    )
    return user, pwd


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
    user, pwd = get_creds()
    for host, mgmt_ip in data.items():
        host_response = []
        # creating netmiko connector
        net_connect = Netmiko(
            mgmt_ip, username=user, password=pwd, device_type="cisco_ios",
        )

        loc = "../inventory/host_vars/" + host + ".yml"
        parsed_host_data = doc_read(loc)
        # rurnning the test:
        for interface in parsed_host_data["interfaces"]:
            if interface["interface"] != "loopback0":
                target = str(get_peer_ip(IPNetwork(interface["ip"])))
                host_response.append(
                    {
                        "Interface": interface["interface"],
                        "Response": net_connect.send_command(f"ping {target}")
                    }
                )
        print(f"\n{'#' * 20} DEVICE: {host} {'#' * 20}\n")
        print(tabulate(host_response, "keys"))


def main():
    data = doc_read("../extra/hosts_file.conf")
    conn_link_tests(data)


if __name__ == "__main__":
    main()
