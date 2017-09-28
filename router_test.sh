#!/bin/bash
function delete_router(){
    while [ $ip1 -le 3000 ]
    do
        neutron router-interface-delete sln_router_$ip1 subnet=sln_subnet_$ip1
        sleep 2
        neutron subnet-delete sln_subnet_$ip1
        sleep 1
        neutron net-delete sln_net_$ip1
        sleep 1
        neutron router-delete sln_router_$ip1
        ip1=`expr $ip1 + 1`
    done
}

function create_router(){
    while [ $ip1 -le 3000 ]
    do
        neutron net-create sln_net_$ip1
        sleep 1
        neutron subnet-create sln_net_$ip1 119.0.0.0/24 --name sln_subnet_$ip1
        sleep 2
        neutron router-create sln_router_$ip1
        sleep 1
        neutron router-interface-add sln_router_$ip1 subnet=sln_subnet_$ip1
        ip1=`expr $ip1 + 1`
    done
}
ip1=27
