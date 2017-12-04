#!/usr/bin/env python  
import os
for port in range(3, 65535):
    cmd = "neutron lbaas-listener-create --loadbalancer LB_listener --protocol TCP --protocol-port %s" % port
    print cmd
    os.system(cmd)
