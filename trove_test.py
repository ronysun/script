# coding: utf-8

from keystoneauth1.identity import v2
from keystoneauth1 import session
from troveclient.v1 import client as trove_client
from saharaclient import client as sahara_client


def trove_create(num, env_config):
    print env_config
    trove = trove_client.Client(env_config['USERNAME'], env_config['PASSWORD'], env_config['OPENSTACK_USER_TENANT'],
                                env_config['OS_AUTH_URL'], region_name=env_config['OPENSTACK_REGION'])
    datastore = "mysql"
    datastore_version = "5.6"
    for arg in xrange(1, 2):
        name = "%sitest%s" % (num, arg)
        instances = [
            {
                "flavorRef": '69f3505c-3cc0-48f8-ac2c-1eb2bd0d792e',
                "volume": {
                    'sys_volume_size': 5,
                    'sys_volume_type': None,
                    'size': 10,
                    'type': "CEPH",
                },
                "nics": [{"net-id": env_config['network_id'], "v4-fixed-ip": ""}],
                "root_password": 'aaaaaa',
                "database_name": name,
                "configuration_id": None  # 可以为null
            }
        ]
        cluster = trove.clusters.create(
            name,
            datastore,
            datastore_version,
            instances=instances)
        cluster_status = trove.clusters.get(cluster)
        print cluster_status


def sahara_create(num, env_config):
    master_template_name = "masterTT"
    cluster_template_name = "clusterTT"
    worker_template_name = "workerTT"
    worker_flavor_id = "c9a6f4cd-1a7c-451a-afe7-ee1358d2fd67"
    availability_zone = "default_availability_zone"
    worker_volume_size = 5
    volumes_availability_zone = "default_availability_zone"
    worker_volume_type = "ceph"
    worker_count = 1
    default_image_id = "c2b6210e-a421-4a4f-96c1-70f4be9a23cb"
    networks = env_config['network_id']
    bfc_volume_size = 60
    bfc_volume_type = "ceph"
    # 如果是bfc模式
    dev_mapping = {'device_name': 'vda',
                   'delete_on_termination': True,
                   'image_id': default_image_id,
                   'boot_index': 0,
                   'volume_size': bfc_volume_size,
                   'volume_type': bfc_volume_type
                   }

    auth = v2.Password(auth_url=env_config['OS_AUTH_URL'], username=env_config['USERNAME'],
                       password=env_config['PASSWORD'], tenant_name=env_config['OPENSTACK_USER_TENANT'])
    ses = session.Session(auth=auth)
    sahara = sahara_client.Client('1.1', session=ses, region_name=env_config['OPENSTACK_REGION'])
    SAHARA_NODE_GROUP_TEMPLATE_DICT = {
        "vanilla": {
            "master": ["namenode", "resourcemanager"],
            "slave": ["nodemanager", "datanode"]
        },
        "spark": {
            "master": ["master", "namenode"],
            "slave": ["slave", "datanode"]
        }
    }
    #
    plugin_name = "vanilla"  # 或者 "spark"
    hadoop_version = "2.7.1"  # 或者 spark时为"1.3"

    master_node_group_template = sahara.node_group_templates.create(
        master_template_name,
        plugin_name,
        hadoop_version,
        worker_flavor_id,
        node_processes=SAHARA_NODE_GROUP_TEMPLATE_DICT[plugin_name]['master'],
        availability_zone=availability_zone)
    print "master_node_group_template is: %s" % master_node_group_template
    worker_node_group_template = sahara.node_group_templates.create(
        worker_template_name,
        plugin_name,
        hadoop_version,
        worker_flavor_id,
        node_processes=SAHARA_NODE_GROUP_TEMPLATE_DICT[plugin_name]['slave'],
        availability_zone=availability_zone,
        volumes_size=worker_volume_size,
        volumes_availability_zone=volumes_availability_zone,
        volume_type=worker_volume_type,
        volumes_per_node=1)
    print "worker_node_group_template is: %s" % worker_node_group_template
    cluster_template = sahara.cluster_templates.create(
        cluster_template_name,
        plugin_name,
        hadoop_version,
        node_groups=[
            {
                "name": "worker",
                "count": int(worker_count),
                "node_group_template_id": worker_node_group_template.id
            },
            {
                "name": "master",
                "count": 1,
                "node_group_template_id": master_node_group_template.id
            }
        ])
    print "cluster_template is: %s" % cluster_template
    # cluster_template = {'id': 'e6d4eddb-e688-48c8-beae-11ffac6f9c8b'}
    for arg in xrange(1, 21):
        name = 'saharaTT%s' % arg
        new_cluster = sahara.clusters.create(
            name,
            plugin_name,
            hadoop_version,
            # cluster_template['id'],
            cluster_template.id,
            default_image_id,
            block_device_mapping_v2=None,  # 该参数不为none时为BFC创建
            neutron_internal_network=networks)


sp = 'pbkdf2_sha256$20000$pwdB2CYO$zQ772K3ICmMOt+3udBTDf0CmzXjY30H6wZgujpKGsNc=',
for num in xrange(2, 3):
    name = "sln%s" % num
    # name = 's@s.com'
    env_config = {'USERNAME': name,
                  'PASSWORD': '1q2w3e',
                  'OPENSTACK_USER_TENANT': name,
                  'OS_AUTH_URL': 'http://192.168.104.100:35357/v2.0',
                  'OS_SERVICE_ENDPOINT': 'http://192.168.104.103:35357/v2.0',
                  'OPENSTACK_REGION': "BJPOC-REGION1",
                  'network_id': 'ca3ba411-5f49-448c-aa8b-00d9b95f571e'}
    # trove_create(num, env_config)
    sahara_create(num, env_config)
