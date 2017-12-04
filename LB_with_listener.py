#!/usr/bin/env python
import os

def create_LB(arg):
    cmd1 = "neutron lbaas-loadbalancer-create LB_subnet --name LB_%s" % arg
    os.system(cmd1)
    cmd2 = "neutron lbaas-listener-create --loadbalancer LB_%s --protocol TCP --protocol-port 8081 --name LB_listener_%s" % (arg, arg)
    os.system(cmd2)

for port in range(171, 175):
    create_LB(port)
