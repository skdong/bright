import json

work_flow_file = 'C:\Users\cgj\Downloads\update_compute-cluster (3).json'
with open(work_flow_file) as fp:
    work_flow = json.load(fp)
tasks = set()
for task in work_flow:
    if task['type'] != 'skipped':
        tasks.add(task['id'])
import pprint

pprint.pprint(tasks)


def test_test():
    need_tasks = """
    primary-cluster
    cluster
    cluster_health
    generate_vms
    hosts
    cluster-vrouter
    virtual_ips
    conntrackd
    setup_repositories
    fuel_pkgs
    hiera
    copy_keys_ceph
    generate_keys_ceph
    top-role-ceph-osd
    primary-ceph-mon
    ssl-keys-saving
    ssl-add-trust-chain
    ssl-dns-setup
    dns-server
    upload_nodes_info
    upload_configuration
    configuration_symlink
    update_hosts
    disable_keystone_service_token
    public_vip_ping
    rsync_core_puppet
    clear_nodes_info
    copy_keys
    generate_keys
    generate_haproxy_keys
    copy_haproxy_keys
    sync_time
    pre_hiera_config
    override_configuration
    ironic_post_swift_key
    ironic_upload_images
    ironic_copy_bootstrap_key
    generate_deleted_nodes
    copy_deleted_nodes
    create_resources
    ntp-server
    ntp-client
    ntp-check
    primary-cluster-haproxy
    cluster-haproxy
    restart-haproxy
    netconfig
    reserved_ports
    globals
    plugins_rsync
    plugins_setup_repositories
    openstack-haproxy
    openstack-haproxy-horizon
    openstack-haproxy-keystone
    openstack-haproxy-nova
    openstack-haproxy-glance
    openstack-haproxy-cinder
    openstack-haproxy-neutron
    openstack-haproxy-mysqld
    openstack-haproxy-swift
    openstack-haproxy-radosgw
    openstack-haproxy-ceilometer
    openstack-haproxy-aodh
    openstack-haproxy-sahara
    openstack-haproxy-murano
    openstack-haproxy-stats
    openstack-haproxy-ironic
    database
    primary-database
    umm
    cgroups
    pre_deployment_start
    pre_deployment_end
    deploy_start
    deploy_end
    post_deployment_start
    post_deployment_end
    controller
    mongo
    base-os
    openstack-controller
    openstack-network-agents-dhcp
    openrc-delete
    keystone-openrc-generate
    top-role-compute
    top-role-cinder
    swift-proxy_storage
    swift-rebalance-cron
    swift-keystone
    
    """.splitlines()

    need_tasks = set(need_tasks)
    import pprint

    print 'more'
    pprint.pprint(tasks - need_tasks)

    print 'less'
    pprint.pprint(need_tasks - tasks)
