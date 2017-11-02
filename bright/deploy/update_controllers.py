workflow = 'update_controller.json'
SKIP_TASKS="""
tools
primary-rabbitmq
prepare_symlinks
pkg_upgrade
limits
api-proxy
logging
firewall
vmware-vcenter
top-role-cinder-vmware
top-role-compute-vmware
fuel_pkgs
hiera
copy_keys_ceph
generate_keys_ceph
primary-ceph-radosgw
ceph-radosgw
radosgw-keystone
ceph_create_pools
ceph_ready_check
enable_rados
updatedb
primary-dns-server
upload_cirros
override_configuration
dump_rabbitmq_definitions
primary-cluster-haproxy
restart-haproxy
hiera_default_route
netconfig
apache
primary-database
memcached
cgroups
primary-controller
cinder
cinder-block-device
cinder-vmware
mongo
primary-mongo
virt
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
primary-openstack-network-agents-metadata
openstack-network-agents-metadata
openstack-network-compute-nova
openstack-network-end
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
primary-keystone
keystone
keystone-db
workloads_collector_add
generate_changed_admin_user
copy_changed_admin_user
delete_old_admin_user
top-role-primary-mongo
top-role-mongo
horizon
""".split()