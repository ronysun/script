#!/usr/bin/env python
import os

def create_listener(arg):
    cmd2 = "neutron lbaas-listener-create --loadbalancer LB_test --protocol TCP --protocol-port %s --name LB_listener_%s" % (arg, arg)
    os.system(cmd2)

cmd1 = "neutron lbaas-loadbalancer-create LB_subnet --name LB_test"
os.system(cmd1)
for port in range(171, 175):
    create_listener(port)
