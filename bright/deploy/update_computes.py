workflow = 'update_compute.json'
SKIP_TASKS = """
tools
rabbitmq
primary-rabbitmq
prepare_symlinks
pkg_upgrade
limits
api-proxy
primary-cluster
cluster
cluster_health
logging
generate_vms
firewall
vmware-vcenter
top-role-cinder-vmware
top-role-compute-vmware
cluster-vrouter
virtual_ips
conntrackd
fuel_pkgs
hiera
copy_keys_ceph
generate_keys_ceph
primary-ceph-radosgw
ceph-radosgw
radosgw-keystone
primary-ceph-mon
ceph-mon
ceph-compute
ceph_create_pools
ceph_ready_check
enable_rados
updatedb
primary-dns-server
dns-server
upload_cirros
vcenter_compute_zones_create
disable_keystone_service_token
primary_public_vip_ping
public_vip_ping
configure_default_route
clear_nodes_info
copy_keys
generate_keys
generate_haproxy_keys
copy_haproxy_keys
sync_time
override_configuration
dump_rabbitmq_definitions
ironic_post_swift_key
ironic_upload_images
ironic_copy_bootstrap_key
generate_deleted_nodes
copy_deleted_nodes
create_resources
primary-cluster-haproxy
cluster-haproxy
restart-haproxy
hiera_default_route
netconfig
sriov_iommu_check
apache
openstack-haproxy
openstack-haproxy-horizon
openstack-haproxy-keystone
openstack-haproxy-nova
openstack-haproxy-heat
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
memcached
cgroups
primary-controller
cinder
cinder-block-device
cinder-vmware
compute-vmware
mongo
primary-mongo
virt
ironic
ceilometer-controller
ceilometer-compute
ceilometer-keystone
ceilometer-radosgw-user
openstack-cinder
cinder-db
cinder-keystone
create-cinder-types
primary-openstack-controller
nova-db
nova-keystone
glance
glance-db
glance-keystone
neutron-db
neutron-keystone
openstack-network-start
openstack-network-common-config
primary-openstack-network-server-config
openstack-network-server-config
primary-openstack-network-plugins-l2
openstack-network-plugins-l2
openstack-network-networks
openstack-network-routers
openstack-network-routers-ha
primary-openstack-network-agents-l3
openstack-network-agents-l3
openstack-network-agents-sriov
openstack-network-server-nova
primary-openstack-network-agents-dhcp
openstack-network-agents-dhcp
primary-openstack-network-agents-metadata
openstack-network-agents-metadata
openstack-network-compute-nova
openstack-network-end
sahara
sahara-db
sahara-keystone
primary-heat
heat
heat-db
heat-keystone
ironic-api
ironic-db
ironic-keystone
ironic-compute
aodh
aodh-keystone
aodh-db
openrc-delete
keystone-openrc-generate
primary-keystone
keystone
keystone-db
workloads_collector_add
generate_changed_admin_user
copy_changed_admin_user
delete_old_admin_user
enable_cinder_volume_service
top-role-primary-mongo
top-role-mongo
ironic-conductor
enable_nova_compute_service
allocate_hugepages
murano
murano-db
murano-keystone
murano-rabbitmq
murano-cfapi
murano-cfapi-keystone
upload_murano_package
horizon
swift-proxy_storage
swift-rebalance-cron
swift-keystone

""".split()
