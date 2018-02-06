#!/usr/bin/env python

# Created on 2017-05-11
# 
# @author: Galvarado - guillermo@sentinel.la
# 
#Depends on vspk, https://github.com/nuagenetworks/vspk-python/blob/4.0/doc/quickstart.rst

from vspk import v4_0 as vspk
import logging
from vspk.utils import set_log_level

# Auth vars
vsd_ip = 'http://lab01.sentinel.la'
api_url = "http://lab01.sentinel.la:8443"
username = "csproot"
password = "csproot"
enterprise = "csp"


def setup_logging():
    pass
    #set_log_level(logging.DEBUG, logging.Streamhandler())

def start_csproot_session():
    session = vspk.NUVSDSession(
        username=username,
        password=password,
        enterprise=enterprise,
        api_url=api_url
    )
    try:
        session.start()
    except:
        logging.error('Failed to start the session')
    return session.user


def detail():
    response = {}

    for enterprise in csproot.enterprises.get(filter='ID is "6e51eafc-a2d7-4f6b-9a34-bb5262b60688" '):
        nsg_branch_up = 0
        nsg_branch_dow = 0
        nsgs = []

        for g in enterprise.ns_redundant_gateway_groups.get(filter='ID is "79ad6616-3e75-4d98-b80f-efea2997d17a"'):
            for p in g.ns_gateways.get():
                if p.bootstrap_status != "ACTIVE":
                    nsg_branch_dow = nsg_branch_dow + 1
                else:
                    nsg_branch_up = nsg_branch_up +1
                nsg_ports = []
                for np in p.ns_ports.get():
                    nsg_port = {
                        "id": np.id,
                        "name": np.name,
                        "description" : np.description,
                        "status" : np.status,
                        "nsg-brach" : p.name,
                        "nsg-branch-id" : p.id
                    }
                    nsg_ports.append(nsg_port)


                nsg = {
                    "id": p.id,
                    "name": p.name,
                    "status" : p.bootstrap_status,
                    "cpu_usage" : 0.949485449,
                    "memory_usage" : 1.3994949,
                    "nsg_ports" : nsg_ports
                }
                nsgs.append(nsg)
        response['nsgs'] = nsgs
        response['nsg-branch-dow'] = nsg_branch_dow
        response['nsg-branch-up'] = nsg_branch_up
    return response
