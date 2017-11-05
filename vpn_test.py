import os
import sys


def create_net1(arg):
    ip1 = arg // 254
    ip2 = arg % 254
    net1_create = "neutron net-create slnvpn1_net_%s" % arg
    subnet1_create = "neutron subnet-create slnvpn1_net_%s 172.%s.%s.0/24 --name slnvpn1_subnet_%s" % (
        arg, ip1, ip2, arg)
    interface1_add = "neutron router-interface-add slnvpn1_router_1 subnet=slnvpn1_subnet_%s" % arg
    os.system(net1_create)
    os.system(subnet1_create)
    os.system(interface1_add)
    net2_create = "neutron net-create slnvpn2_net_%s" % arg
    subnet2_create = "neutron subnet-create slnvpn2_net_%s 173.%s.%s.0/24 --name slnvpn2_subnet_%s" % (
        arg, ip1, ip2, arg)
    interface2_add = "neutron router-interface-add slnvpn2_router_1 subnet=slnvpn2_subnet_%s" % arg
    os.system(net2_create)
    os.system(subnet2_create)
    os.system(interface2_add)


def create_ipsec(arg):
    ip1 = arg // 254
    ip2 = arg % 254
    ipsec1 = "neutron ipsec-site-connection-create --ikepolicy-id %s --ipsecpolicy-id %s --peer-address 192.168.114.54 --peer-id 10.0.114.74 --peer-cidr 173.%s.%s.0/24 --psk %s --vpnservice-id %s --name ipsec1_connect_%s" % (
        ikepolicy_id, ipsecpolicy_id, ip1, ip2, psk, vpnservice1_id, arg)
    os.system(ipsec1)
    ipsec2 = "neutron ipsec-site-connection-create --ikepolicy-id %s --ipsecpolicy-id %s --peer-address 192.168.114.90 --peer-id 10.0.114.98 --peer-cidr 172.%s.%s.0/24 --psk %s --vpnservice-id %s --name ipsec2_connect_%s" % (
        ikepolicy_id, ipsecpolicy_id, ip1, ip2, psk, vpnservice2_id, arg)
    os.system(ipsec2)


"""
delete resources
"""
def delete_net(arg):
    interface1_remove = "neutron router-interface-delete slnvpn1_router_1 subnet=slnvpn1_subnet_%s" % arg
    os.system(interface1_remove)
    subnet1_delete = "neutron subnet-delete slnvpn1_subnet_%s" % arg
    net1_delete = "neutron net-delete slnvpn1_net_%s" % arg
    os.system(subnet1_delete)
    os.system(net1_delete)
    interface2_remove = "neutron router-interface-delete slnvpn2_router_1 subnet=slnvpn2_subnet_%s" % arg
    subnet2_delete = "neutron subnet-delete slnvpn2_subnet_%s" % arg
    net2_delete = "neutron net-delete slnvpn2_net_%s" % arg
    os.system(interface2_remove)
    os.system(subnet2_delete)
    os.system(net2_delete)


def delete_ipsec(arg):
    ipsec1_delete = "neutron ipsec-site-connection-delete ipsec1_connect_%s" % arg
    ipsec2_delete = "neutron ipsec-site-connection-delete ipsec2_connect_%s" % arg
    os.system(ipsec1_delete)
    os.system(ipsec2_delete)

action = sys.argv[1]
num = int(sys.argv[2])
ikepolicy_id = 'f909b167-75df-427b-8bfd-dc23be9549ec'
ipsecpolicy_id = '8a0b0eda-cd12-4a91-8827-63c97e101f13'
psk = '1q2w3e'
vpnservice1_id = "b8260a8c-0f2e-4a99-866c-cda6162ec8d6"
vpnservice2_id = "e92b36ff-47eb-4494-b626-f34a16c04502"
if action == "c":
    for arg in range(2, num):
        create_net1(arg)
        create_ipsec(arg)
elif action == "d":
    for arg in range(2, num):
        delete_ipsec(arg)
        delete_net(arg)
else:
    print "prameter is not know"
