#!/bin/bash
function create_router1(){
    neutron router-create slnvpn1_router_$arg
    sleep 1
    neutron router-gateway-set slnvpn1_router_$arg ext_net --fixed-ip subnet_id=internal
    sleep 2
    router1_id=`neutron router-show slnvpn1_router_$arg|grep " id"|awk '{print $4}'`
    router1_addr=`neutron router-show slnvpn1_router_$arg|grep "10.0"|awk -F '"' '{print $20}'`
    floatingip1_id=`neutron floatingip-create ext_net|grep " id"|awk '{print $4}'`
    floatingip1_addr=`neutron floatingip-show $floatingip1_id|grep "floating_ip_address"|awk '{print $4}'`
    neutron floatingip-router-associate $floatingip1_id $router1_id
}

function create_router2(){
    neutron router-create slnvpn2_router_$arg
    sleep 1
    neutron router-gateway-set slnvpn2_router_$arg ext_net --fixed-ip subnet_id=internal
    sleep 2
    router2_id=`neutron router-show slnvpn2_router_$arg|grep " id"|awk '{print $4}'`
    router2_addr=`neutron router-show slnvpn2_router_$arg|grep "10.0"|awk -F '"' '{print $20}'`
    floatingip2_id=`neutron floatingip-create ext_net|grep " id"|awk '{print $4}'`
    floatingip2_addr=`neutron floatingip-show $floatingip2_id|grep "floating_ip_address"|awk '{print $4}'`
    neutron floatingip-router-associate $floatingip2_id $router2_id
}

function create_net1(){
    neutron net-create slnvpn1_net_$arg
    sleep 1
    neutron subnet-create slnvpn1_net_$arg 172.0.$arg.0/24 --name slnvpn1_subnet_$arg
    sleep 2
    neutron router-interface-add slnvpn1_router_$arg subnet=slnvpn1_subnet_$arg
    neutron net-create slnvpn2_net_$arg
    sleep 1
    neutron subnet-create slnvpn2_net_$arg 173.0.$arg.0/24 --name slnvpn2_subnet_$arg
    sleep 2
    neutron router-interface-add slnvpn2_router_$arg subnet=slnvpn2_subnet_$arg
}

function create_net2(){
    pass
}

function create_vpn_service1(){
    vpnservice1_id=`neutron vpn-service-create slnvpn1_router_$arg slnvpn1_subnet_$arg --name slnvpn1_vpnserver_$arg |grep " id"|awk '{print $4}'`
    neutron ipsec-site-connection-create --ikepolicy-id $ikepolicy_id --ipsecpolicy-id $ipsecpolicy_id \
        --peer-address $floatingip2_addr --peer-id $router1_addr --peer-cidr 173.0.$arg.0/24 --psk $psk \
        --vpnservice-id $vpnservice1_id --name ipsec1_connect_$arg
    vpnservice2_id=`neutron vpn-service-create slnvpn2_router_$arg slnvpn2_subnet_$arg --name slnvpn2_vpnserver_$arg|grep " id"|awk '{print $4}'`
    neutron ipsec-site-connection-create --ikepolicy-id $ikepolicy_id --ipsecpolicy-id $ipsecpolicy_id \
        --peer-address $floatingip2_addr --peer-id $router2_addr --peer-cidr 172.0.$arg.0/24 --psk $psk \
        --vpnservice-id $vpnservice2_id --name ipsec2_connect_$arg
}

function create_vpn_service2(){
    pass
}

function delete_net1(){
    neutron router-interface-delete slnvpn1_router_$arg subnet=slnvpn1_subnet_$arg
    neutron subnet-delete slnvpn1_subnet_$arg
    neutron net-delete slnvpn1_net_$arg
    neutron router-interface-delete slnvpn2_router_$arg subnet=slnvpn2_subnet_$arg
    neutron subnet-delete slnvpn2_subnet_$arg
    neutron net-delete slnvpn2_net_$arg
}

function delete_net2(){
    pass
}

function delete_vpn_service1(){
    neutron ipsec-site-connection-delete ipsec1_connect_$arg
    neutron vpn-service-delete slnvpn1_vpnserver_$arg
    neutron ipsec-site-connection-delete ipsec2_connect_$arg
    neutron vpn-service-delete slnvpn2_vpnserver_$arg
}

function delete_vpn_service2(){
    pass
}

function delete_router(){
    neutron router-delete slnvpn1_router_$arg
    neutron router-delete slnvpn2_router_$arg
}

arg=1
ikepolicy_id='f909b167-75df-427b-8bfd-dc23be9549ec'
ipsecpolicy_id='8a0b0eda-cd12-4a91-8827-63c97e101f13'
psk='1q2w3e'
# create_vpn_service2
if [ "$1" == "c" ]; then
    while [[ $arg -ge 1 ]]; do
        create_router1
        create_router2
        create_net1
        # create_net2
        create_vpn_service1
        # create_vpn_service2
        arg=`expr $arg - 1`
        #statements
    done
elif [ "$1" == "d" ]; then
    while [[ $arg -ge 1 ]]; do
        delete_vpn_service1
        # delete_vpn_service2
        delete_net1
        # delete_net2
        delete_router
        arg=`expr $arg - 1`
    done
else
    echo "$1 is not a parameter can be recive"
    #statements
fi

#create_router
#create_vpn_service

