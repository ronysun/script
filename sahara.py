from keystoneauth1.identity import v2
from keystoneauth1 import session
from saharaclient import client 

import sys 

from oslo_utils import importutils

AUTH_URL = 'http://192.168.104.100:5000/v2.0'
USERNAME = 'sln1'
PASSWORD = '1q2w3e'
PROJECT_ID = 'sln1'

auth = v2.Password(auth_url=AUTH_URL,
                   username=USERNAME,
                   password=PASSWORD,
                   tenant_name=PROJECT_ID)

ses = session.Session(auth=auth)

sahara = client.Client('1.1', session=ses)

#print(sahara.plugins.list()[0])
#print(sahara.node_group_templates.list()[0])
#print(sahara.cluster_templates.list()[0])
#print(sahara.clusters.list()[0])
#print(sahara.clusters.list(search_opts={'name':'test1'}))

#print(sahara.images.list({'tags': ['vanilla', '2.7.1']})[0])
#a = sahara.node_group_templates.create("tient", "vanilla", "2.7.1", "fb388319-518d-402c-a102-9d7ac6150836", node_processes=["namenode","resourcemanager"])


cluster_template = {
    "plugin_name": "vanilla",
    "hadoop_version": "2.7.1",
    "node_groups": [
        {
            "name": "worker",
            "count": 3,
            "node_group_template_id": "6527029c-93a0-4c95-b5af-30221b1a9c96"
        },
        {
            "name": "master",
            "count": 1,
            "node_group_template_id": "891edaf0-2212-4f0b-8c0f-1401c772c8f2"
        }
    ],
    "name": "vanilla-default-cluster2",
    "cluster_configs": {}
}

b = sahara.cluster_templates.create(cluster_template["name"], cluster_template["plugin_name"], cluster_template["hadoop_version"], node_groups=cluster_template["node_groups"])


from neutronclient.v2_0 import client as nclient
neutron = nclient.Client(session=ses)
network_list = neutron.list_networks(id="17203b92-d91d-4acf-84fb-3a337cfffd3c")
print(network_list.get('networks'))
#sg = neutron.list_security_groups(name="default")
#print(sg)

from novaclient import client as novaclient
nova = novaclient.Client(2,session=ses)
#print(flavor_list)
#server_list = nova.servers.list(detailed=True, search_opts={"metadata": '{"hidden": "1"}'})
#print(server_list)


