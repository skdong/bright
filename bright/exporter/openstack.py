#!/usr/bin/env python
"""
OpenStack exporter for the prometheus monitoring system

Copyright (C) 2016 Canonical, Ltd.
Authors:
  Jacek Nykis <jacek.nykis@canonical.com>
  Laurent Sesques <laurent.sesques@canonical.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3,
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranties of
MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import yaml
import json
import ast
from os import environ as env
from os import rename, path
import traceback
import urlparse
from threading import Thread
import pickle
import requests
from time import sleep, time
from neutronclient.v2_0 import client as neutron_client
# from novaclient.v1_1 import client as nova_client
# http://docs.openstack.org/developer/python-novaclient/api.html
from cinderclient.v2 import client as cinder_client
from novaclient import client as nova_client
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ForkingMixIn
from prometheus_client import CollectorRegistry, generate_latest, Gauge, CONTENT_TYPE_LATEST
from netaddr import IPRange

import logging
import logging.handlers

log = logging.getLogger('poe-logger')


def get_creds_dict(*names):
    """Get dictionary with cred envvars"""
    return {name: env['OS_%s' % name.upper()]
            for name in names if 'OS_%s' % name.upper() in env}


def get_creds_list(*names):
    """Get list with cred envvars, error if not set"""
    return [env['OS_%s' % name.upper()] for name in names]


def maybe_get_cacert():
    """Get cacert, None if unset"""
    return env.get("OS_CACERT")


def get_clients():
    ks_version = int(env.get('OS_IDENTITY_API_VERSION', 2))
    if ks_version == 2:
        from keystoneclient.v2_0 import client as keystone_client
        # Legacy v2 env vars:
        # OS_USERNAME OS_PASSWORD OS_TENANT_NAME OS_AUTH_URL OS_REGION_NAME
        ks_creds = get_creds_dict("username", "password", "tenant_name",
                                  "auth_url", "region_name")
        cacert = maybe_get_cacert()
        if cacert:
            ks_creds["cacert"] = cacert
        nova_creds = [2] + get_creds_list("username", "password", "tenant_name",
                                          "auth_url")
        cinder_creds = get_creds_list("username", "password", "tenant_name",
                                      "auth_url")
        keystone = keystone_client.Client(**ks_creds)
        nova = nova_client.Client(*nova_creds, cacert=cacert)
        neutron = neutron_client.Client(**ks_creds)
        cinder = cinder_client.Client(*cinder_creds, cacert=cacert)

    elif ks_version == 3:
        from keystoneauth1.identity import v3
        from keystoneauth1 import session
        from keystoneclient.v3 import client
        # A little helper for the poor human trying to figure out which env vars
        # are needed, it worked for me (jjo) having:
        #  OS_USERNAME OS_PASSWORD OS_USER_DOMAIN_NAME OS_AUTH_URL
        #  OS_PROJECT_DOMAIN_NAME OS_PROJECT_DOMAIN_ID OS_PROJECT_ID OS_DOMAIN_NAME
        # Keystone needs domain creds for e.g. project list

        # project and project_domain are needed for listing projects
        ks_creds_domain = get_creds_dict(
            "username", "password", "user_domain_name", "auth_url",
            "project_domain_name", "project_name", "project_domain_id", "project_id")
        # Need non-domain creds to get full catalog
        ks_creds_admin = get_creds_dict(
            "username", "password", "user_domain_name", "auth_url",
            "project_domain_name", "project_name", "project_domain_id", "project_id")
        auth_domain = v3.Password(**ks_creds_domain)
        auth_admin = v3.Password(**ks_creds_admin)
        # Need to pass in cacert separately
        verify = maybe_get_cacert()
        if verify is None:
            verify = True
        sess_domain = session.Session(auth=auth_domain, verify=verify)
        sess_admin = session.Session(auth=auth_admin, verify=verify)

        keystone = client.Client(session=sess_domain)
        nova = nova_client.Client(2, session=sess_admin)
        neutron = neutron_client.Client(session=sess_admin)
        cinder = cinder_client.Client(session=sess_admin)

    else:
        raise(ValueError("Invalid OS_IDENTITY_API_VERSION=%s" % ks_version))
    log.debug("Client setup done, keystone ver {}".format(ks_version))
    return (keystone, nova, neutron, cinder)


class DataGatherer(Thread):
    """Periodically retrieve data from openstack in a separate thread,
    save as pickle to cache_file
    """

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.duration = 0
        self.refresh_interval = config.get('cache_refresh_interval', 900)
        self.cache_file = config['cache_file']
        self.use_nova_volumes = config.get('use_nova_volumes', True)

    def run(self):
        log.debug("Starting data gather thread")
        prodstack = {}
        while True:
            start_time = time()
            try:
                keystone, nova, neutron, cinder = get_clients()

                try:
                    prodstack['tenants'] = [x._info for x in keystone.tenants.list()]
                except AttributeError:
                    log.info("Error getting tenants.list, continue with projects.list")
                    prodstack['tenants'] = [x._info for x in keystone.projects.list()]
                    log.debug("Number of projects: %s", len(prodstack['tenants']))
                prodstack['hypervisors'] = [x._info for x in nova.hypervisors.list()]
                prodstack['services'] = [x._info for x in nova.services.list()]
                prodstack['networks'] = neutron.list_networks()['networks']
                prodstack['flavors'] = [x._info for x in nova.flavors.list(is_public=None)]
                prodstack['aggregates'] = [x.to_dict() for x in nova.aggregates.list()]
                prodstack['subnets'] = neutron.list_subnets()['subnets']
                prodstack['routers'] = neutron.list_routers()['routers']
                prodstack['ports'] = neutron.list_ports()['ports']
                prodstack['floatingips'] = neutron.list_floatingips()['floatingips']

                # Instance info is very heavy, disable until we merge this bit with pantomath
                prodstack['instances'] = []
                marker = ''
                while True:
                    search_opts = {'all_tenants': '1', 'limit': '100', 'marker': marker}
                    new_instances = [x._info for x in nova.servers.list(search_opts=search_opts)]
                    if new_instances:
                        marker = new_instances[-1]['id']
                        prodstack['instances'].extend(new_instances)
                    else:
                        break

                prodstack['volume_quotas'] = {}
                prodstack['nova_quotas'] = {}
                for t in prodstack['tenants']:
                    tid = t['id']
                    if self.use_nova_volumes:
                        prodstack['volume_quotas'][tid] = cinder.quotas.get(tid, usage=True)._info
                    # old OS versions (e.g. Mitaka) will 404 if we request details
                    try:
                        prodstack['nova_quotas'][tid] = nova.quotas.get(tid, detail=True)._info
                    except:
                        prodstack['nova_quotas'][tid] = nova.quotas.get(tid)._info

            except:
                # Ignore failures, we will try again after refresh_interval.
                # Most of them are termporary ie. connectivity problmes
                # To alert on stale cache use openstack_exporter_cache_age_seconds metric
                log.critical("Error getting stats: {}".format(traceback.format_exc()))
            else:
                with open(self.cache_file + '.new', "wb+") as f:
                    pickle.dump((prodstack, ), f, pickle.HIGHEST_PROTOCOL)
                rename(self.cache_file + '.new', self.cache_file)
                log.debug("Done dumping stats to {}".format(self.cache_file))
            self.duration = time() - start_time
            sleep(self.refresh_interval)

    def get_stats(self):
        registry = CollectorRegistry()
        labels = ['cloud']
        age = Gauge('openstack_exporter_cache_age_seconds',
                    'Cache age in seconds. It can reset more frequently '
                    'than scraping interval so we use Gauge',
                    labels, registry=registry)
        l = [config['cloud']]
        age.labels(*l).set(time() - path.getmtime(self.cache_file))
        duration = Gauge('openstack_exporter_cache_refresh_duration_seconds',
                         'Cache refresh duration in seconds.',
                         labels, registry=registry)
        duration.labels(*l).set(self.duration)
        return generate_latest(registry)


class Neutron():
    def __init__(self):
        self.registry = CollectorRegistry()
        self.prodstack = {}
        with open(config['cache_file'], 'rb') as f:
            self.prodstack = pickle.load(f)[0]

        self.tenant_map = {t['id']: t['name'] for t in self.prodstack['tenants']}
        self.network_map = {n['id']: n['name'] for n in self.prodstack['networks']}
        self.subnet_map = {n['id']: {'name': n['name'], 'pool': n['allocation_pools']} for n in self.prodstack['subnets']}
        self.routers = self.prodstack['routers']
        self.ports = self.prodstack['ports']
        self.floating_ips = self.prodstack['floatingips']

    def _get_router_ip(self, uuid):
        owner = "network:router_gateway"
        for port in self.ports:
            if port["device_id"] == uuid and port["device_owner"] == owner:
                return port["fixed_ips"][0]["ip_address"]

    def get_floating_ips(self):
        ips = {}
        for ip in self.floating_ips:
            subnet = self.network_map[ip['floating_network_id']]
            try:
                tenant = self.tenant_map[ip['tenant_id']]
            except KeyError:
                tenant = 'Unknown tenant ({})'.format(ip['tenant_id'])
            key = (config['cloud'], subnet, tenant, 'floatingip', ip['status'])
            if key in ips:
                ips[key] += 1
            else:
                ips[key] = 1
        return ips

    def get_router_ips(self):
        ips = {}
        for r in self.routers:
            if self._get_router_ip(r['id']):
                if r['tenant_id'].startswith('<Tenant {'):
                    r['tenant_id'] = ast.literal_eval(r['tenant_id'][8:-1])['id']
                try:
                    tenant = self.tenant_map[r['tenant_id']]
                except KeyError:
                    tenant = 'Unknown tenant ({})'.format(r['tenant_id'])
                subnet = self.network_map[r['external_gateway_info']['network_id']]
                key = (config['cloud'], subnet, tenant, 'routerip', r['status'])
                if key in ips:
                    ips[key] += 1
                else:
                    ips[key] = 1
        return ips

    def gen_subnet_size(self):
        labels = ['cloud', 'network_name']
        net_size = Gauge('neutron_net_size',
                         'Neutron networks size',
                         labels, registry=self.registry)
        for n in self.prodstack['networks']:
            size = 0
            for subnet in n['subnets']:
                for pool in self.subnet_map[subnet]['pool']:
                    if ':' in pool['start']:
                        # Skip IPv6 address pools; they are big enough to
                        # drown the IPv4 numbers we might care about.
                        continue
                    size += IPRange(pool['start'], pool['end']).size
            l = [config['cloud'], self.network_map[n['id']]]
            net_size.labels(*l).set(size)

    def get_stats(self):
        labels = ['cloud', 'subnet_name', 'tenant', 'ip_type', 'ip_status']
        ips = self.get_floating_ips()
        ips.update(self.get_router_ips())
        metrics = Gauge('neutron_public_ip_usage',
                        'Neutron floating IP and router IP usage statistics',
                        labels, registry=self.registry)
        for k, v in ips.items():
            metrics.labels(*k).set(v)
        self.gen_subnet_size()
        return generate_latest(self.registry)


class Cinder():
    def __init__(self):
        self.registry = CollectorRegistry()
        self.prodstack = {}
        with open(config['cache_file'], 'rb') as f:
            self.prodstack = pickle.load(f)[0]
        self.tenant_map = {t['id']: t['name'] for t in self.prodstack['tenants']}
        self.use_nova_volumes = config.get('use_nova_volumes', True)

    def gen_volume_quota_stats(self):
        gbs = Gauge('cinder_quota_volume_disk_gigabytes',
                    'Cinder volume metric (GB)',
                    ['cloud', 'tenant', 'type'], registry=self.registry)
        vol = Gauge('cinder_quota_volume_disks',
                    'Cinder volume metric (number of volumes)',
                    ['cloud', 'tenant', 'type'], registry=self.registry)
        if not self.use_nova_volumes:
            return
        for t, q in self.prodstack['volume_quotas'].items():
            if t in self.tenant_map:
                tenant = self.tenant_map[t]
            else:
                tenant = 'orphaned'
            for tt in ['limit', 'in_use', 'reserved']:
                gbs.labels(config['cloud'], tenant, tt).inc(q['gigabytes'][tt])
                vol.labels(config['cloud'], tenant, tt).inc(q['volumes'][tt])

    def get_stats(self):
        self.gen_volume_quota_stats()
        return generate_latest(self.registry)


class Nova():
    def __init__(self):
        self.registry = CollectorRegistry()
        self.prodstack = {}
        with open(config['cache_file'], 'rb') as f:
            self.prodstack = pickle.load(f)[0]
        self.hypervisors = self.prodstack['hypervisors']
        self.tenant_map = {t['id']: t['name'] for t in self.prodstack['tenants']}
        self.flavor_map = {f['id']: {'ram': f['ram'], 'disk': f['disk'], 'vcpus': f['vcpus']}
                           for f in self.prodstack['flavors']}
        self.aggregate_map = {}
        self.services_map = {}
        for s in self.prodstack['services']:
            if s['binary'] == 'nova-compute':
                self.services_map[s['host']] = s['status']
        for agg in self.prodstack['aggregates']:
            self.aggregate_map.update({i: agg['name'] for i in agg['hosts']})

    def _get_schedulable_instances(self, host):
        free_vcpus = host['vcpus'] * config['openstack_allocation_ratio_vcpu'] - host['vcpus_used']
        free_ram_mbs = host['memory_mb'] * config['openstack_allocation_ratio_ram'] - host['memory_mb_used']
        free_disk_gbs = host['local_gb'] * config['openstack_allocation_ratio_disk'] - host['local_gb_used']
        s = config['schedulable_instance_size']
        return min(int(free_vcpus / s['vcpu']),
                   int(free_ram_mbs / s['ram_mbs']),
                   int(free_disk_gbs / s['disk_gbs']))

    def _get_schedulable_instances_capacity(self, host):
        capacity_vcpus = host['vcpus'] * config['openstack_allocation_ratio_vcpu']
        capacity_ram_mbs = host['memory_mb'] * config['openstack_allocation_ratio_ram']
        capacity_disk_gbs = host['local_gb'] * config['openstack_allocation_ratio_disk']
        s = config['schedulable_instance_size']
        return min(int(capacity_vcpus / s['vcpu']),
                   int(capacity_ram_mbs / s['ram_mbs']),
                   int(capacity_disk_gbs / s['disk_gbs']))

    def gen_hypervisor_stats(self):
        labels = ['cloud', 'hypervisor_hostname', 'aggregate', 'nova_service_status', 'arch']
        vms = Gauge('hypervisor_running_vms', 'Number of running VMs', labels, registry=self.registry)
        vcpus_total = Gauge('hypervisor_vcpus_total', 'Total number of vCPUs', labels, registry=self.registry)
        vcpus_used = Gauge('hypervisor_vcpus_used', 'Number of used vCPUs', labels, registry=self.registry)
        mem_total = Gauge('hypervisor_memory_mbs_total', 'Total amount of memory in MBs', labels, registry=self.registry)
        mem_used = Gauge('hypervisor_memory_mbs_used', 'Used memory in MBs', labels, registry=self.registry)
        disk_total = Gauge('hypervisor_disk_gbs_total', 'Total amount of disk space in GBs', labels, registry=self.registry)
        disk_used = Gauge('hypervisor_disk_gbs_used', 'Used disk space in GBs', labels, registry=self.registry)
        schedulable_instances = Gauge('hypervisor_schedulable_instances',
                                      'Number of schedulable instances, see "schedulable_instance_size" option',
                                      labels, registry=self.registry)
        schedulable_instances_capacity = Gauge('hypervisor_schedulable_instances_capacity',
                                               'Number of schedulable instances we have capacity for',
                                               labels, registry=self.registry)

        def squashnone(val, default=0):
            if val is None:
                return default
            return val

        for h in self.hypervisors:
            log.debug("Hypervisor: %s", h)
            host = h['service']['host']
            log.debug("host: %s", host)
            cpu_info = h['cpu_info']
            log.debug("cpu_info: %s", cpu_info)
            arch = 'Unknown'
            if not cpu_info:
                log.info("Could not get cpu info")
            elif type(cpu_info) != dict:
                cpu_info = json.loads(cpu_info)
                arch = cpu_info['arch']
            l = [config['cloud'], host, self.aggregate_map.get(host, 'unknown'), self.services_map[host], arch]
            # Disabled hypervisors return None below, convert to 0
            vms.labels(*l).set(squashnone(h['running_vms']))
            vcpus_total.labels(*l).set(squashnone(h['vcpus']))
            vcpus_used.labels(*l).set(squashnone(h['vcpus_used']))
            mem_total.labels(*l).set(squashnone(h['memory_mb']))
            mem_used.labels(*l).set(squashnone(h['memory_mb_used']))
            disk_total.labels(*l).set(squashnone(h['local_gb']))
            disk_used.labels(*l).set(squashnone(h['local_gb_used']))

            if config.get("schedulable_instance_size", False):
                schedulable_instances.labels(*l).set(self._get_schedulable_instances(h))
                schedulable_instances_capacity.labels(*l).set(self._get_schedulable_instances_capacity(h))

    def gen_instance_stats(self):
        missing_flavors = False
        instances = Gauge('nova_instances',
                          'Nova instances metrics',
                          ['cloud', 'tenant', 'instance_state'], registry=self.registry)
        res_ram = Gauge('nova_resources_ram_mbs',
                        'Nova RAM usage metric',
                        ['cloud', 'tenant'], registry=self.registry)
        res_vcpus = Gauge('nova_resources_vcpus',
                          'Nova vCPU usage metric',
                          ['cloud', 'tenant'], registry=self.registry)
        res_disk = Gauge('nova_resources_disk_gbs',
                         'Nova disk usage metric',
                         ['cloud', 'tenant'], registry=self.registry)
        for i in self.prodstack['instances']:
            if i['tenant_id'] in self.tenant_map:
                tenant = self.tenant_map[i['tenant_id']]
            else:
                tenant = 'orphaned'
            instances.labels(config['cloud'], tenant, i['status']).inc()

            if i['flavor']['id'] in self.flavor_map:
                flavor = self.flavor_map[i['flavor']['id']]
                res_ram.labels(config['cloud'], tenant).inc(flavor['ram'])
                res_vcpus.labels(config['cloud'], tenant).inc(flavor['vcpus'])
                res_disk.labels(config['cloud'], tenant).inc(flavor['disk'])
            else:
                missing_flavors = True

        # If flavors were deleted we can't reliably find out resouerce use
        if missing_flavors:
            self.registry.unregister(res_ram)
            self.registry.unregister(res_vcpus)
            self.registry.unregister(res_disk)
            res_ram = Gauge('nova_resources_ram_mbs', 'Nova RAM usage metric unavailable, missing flavors',
                            [], registry=self.registry)
            res_vcpus = Gauge('nova_resources_vcpus', 'Nova vCPU usage metric unavailable, missing flavors',
                              [], registry=self.registry)
            res_disk = Gauge('nova_resources_disk_gbs', 'Nova disk usage metric unavailable, missing flavors',
                             [], registry=self.registry)

    def gen_overcommit_stats(self):
        labels = ['cloud', 'resource']
        openstack_overcommit = Gauge('openstack_allocation_ratio', 'Openstack overcommit ratios',
                                     labels, registry=self.registry)
        l = [config['cloud'], 'vcpu']
        openstack_overcommit.labels(*l).set(config['openstack_allocation_ratio_vcpu'])
        l = [config['cloud'], 'ram']
        openstack_overcommit.labels(*l).set(config['openstack_allocation_ratio_ram'])
        l = [config['cloud'], 'disk']
        openstack_overcommit.labels(*l).set(config['openstack_allocation_ratio_disk'])

    def gen_quota_stats(self):
        cores = Gauge('nova_quota_cores',
                      'Nova cores metric',
                      ['cloud', 'tenant', 'type'], registry=self.registry)
        fips = Gauge('nova_quota_floating_ips',
                     'Nova floating IP addresses (number)',
                     ['cloud', 'tenant', 'type'], registry=self.registry)
        inst = Gauge('nova_quota_instances',
                     'Nova instances (number)',
                     ['cloud', 'tenant', 'type'], registry=self.registry)
        ram = Gauge('nova_quota_ram_mbs',
                    'Nova RAM (MB)',
                    ['cloud', 'tenant', 'type'], registry=self.registry)
        for t, q in self.prodstack['nova_quotas'].items():
            if t in self.tenant_map:
                tenant = self.tenant_map[t]
            else:
                tenant = 'orphaned'

            # we get detailed quota information only on recent OS versions
            if isinstance(q['cores'], int):
                cores.labels(config['cloud'], tenant, 'limit').set(q['cores'])
                fips.labels(config['cloud'], tenant, 'limit').set(q['floating_ips'])
                inst.labels(config['cloud'], tenant, 'limit').set(q['instances'])
                ram.labels(config['cloud'], tenant, 'limit').set(q['ram'])
            else:
                for tt in ['limit', 'in_use', 'reserved']:
                    cores.labels(config['cloud'], tenant, tt).inc(q['cores'][tt])
                    fips.labels(config['cloud'], tenant, tt).inc(q['floating_ips'][tt])
                    inst.labels(config['cloud'], tenant, tt).inc(q['instances'][tt])
                    ram.labels(config['cloud'], tenant, tt).inc(q['ram'][tt])

    def get_stats(self):
        log.debug("get_stats")
        self.gen_hypervisor_stats()
        self.gen_instance_stats()
        self.gen_overcommit_stats()
        self.gen_quota_stats()
        return generate_latest(self.registry)


class Swift():
    def __init__(self):
        self.registry = CollectorRegistry()
        self.baseurl = 'http://{}:6000/recon/{}'
        self.swift_hosts = config.get('swift_hosts', [])

    def gen_up_stats(self):
        labels = ['cloud', 'hostname']
        swift_up = Gauge('swift_host_up', 'Swift host reachability',
                         labels, registry=self.registry)
        for h in self.swift_hosts:
            try:
                requests.get(self.baseurl.format(h, 'diskusage'))
                swift_up.labels(config['cloud'], h).set(1)
            except requests.exceptions.RequestException:
                swift_up.labels(config['cloud'], h).set(0)

    def gen_disk_usage_stats(self):
        labels = ['cloud', 'hostname', 'device', 'type']
        swift_disk = Gauge('swift_disk_usage_bytes', 'Swift disk usage in bytes',
                           labels, registry=self.registry)
        for h in self.swift_hosts:
            try:
                r = requests.get(self.baseurl.format(h, 'diskusage'))
            except requests.exceptions.RequestException:
                continue
            for disk in r.json():
                if not all([disk.get(i, False) for i in ['size', 'used', 'device']]):
                    continue
                swift_disk.labels(config['cloud'], h, disk['device'], 'size').set(int(disk['size']))
                swift_disk.labels(config['cloud'], h, disk['device'], 'used').set(int(disk['used']))

    def gen_quarantine_stats(self):
        labels = ['cloud', 'hostname', 'ring']
        swift_quarantine = Gauge('swift_quarantined_objects', 'Number of quarantined objects',
                                 labels, registry=self.registry)
        for h in self.swift_hosts:
            try:
                r = requests.get(self.baseurl.format(h, 'quarantined'))
            except requests.exceptions.RequestException:
                continue
            for ring in ['accounts', 'objects', 'containers']:
                swift_quarantine.labels(config['cloud'], h, ring).set(r.json().get(ring))

    def gen_replication_stats(self):
        labels = ['cloud', 'hostname', 'ring', 'type']
        swift_repl = Gauge('swift_replication_stats', 'Swift replication stats', labels, registry=self.registry)
        labels = ['cloud', 'hostname', 'ring']
        swift_repl_duration = Gauge('swift_replication_duration_seconds', 'Swift replication duration in seconds',
                                    labels, registry=self.registry)
        for h in self.swift_hosts:
            metrics = ['attempted', 'diff', 'diff_capped', 'empty',
                       'failure', 'hashmatch', 'no_change', 'remote_merge',
                       'remove', 'rsync', 'success', 'ts_repl']
            # Object replication is special
            try:
                r = requests.get(self.baseurl.format(h, 'replication/object'))
            except requests.exceptions.RequestException:
                continue
            try:
                swift_repl_duration.labels(config['cloud'], h, 'object').set(r.json()['object_replication_time'])
            except TypeError:
                print(traceback.format_exc())

            for ring in ['account', 'container']:
                try:
                    r = requests.get(self.baseurl.format(h, 'replication/' + ring))
                except requests.exceptions.RequestException:
                    continue
                try:
                    swift_repl_duration.labels(config['cloud'], h, ring).set(r.json()['replication_time'])
                except TypeError:
                    print(traceback.format_exc())

                for metric in metrics:
                    try:
                        swift_repl.labels(config['cloud'], h, ring, metric).set(r.json()['replication_stats'][metric])
                    except TypeError:
                        print(traceback.format_exc())

    def get_stats(self):
        self.gen_up_stats()
        self.gen_disk_usage_stats()
        self.gen_quarantine_stats()
        self.gen_replication_stats()
        return generate_latest(self.registry)


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    pass


class OpenstackExporterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        url = urlparse.urlparse(self.path)
        if url.path == '/metrics':
            try:
                neutron = Neutron()
                nova = Nova()
                cinder = Cinder()
                swift = Swift()
                log.debug("Collecting stats..")
                output = neutron.get_stats() + \
                    nova.get_stats() + \
                    cinder.get_stats() + \
                    swift.get_stats() + \
                    data_gatherer.get_stats()
                self.send_response(200)
                self.send_header('Content-Type', CONTENT_TYPE_LATEST)
                self.end_headers()
                self.wfile.write(output)
            except:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(traceback.format_exc())
        elif url.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write("""<html>
            <head><title>OpenStack Exporter</title></head>
            <body>
            <h1>OpenStack Exporter</h1>
            <p>Visit <code>/metrics</code> to use.</p>
            </body>
            </html>""")
        else:
            self.send_response(404)
            self.end_headers()


def handler(*args, **kwargs):
    OpenstackExporterHandler(*args, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage=__doc__,
                                     description='Prometheus OpenStack exporter',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('config_file', nargs='?',
                        help='Configuration file path',
                        default='/etc/prometheus/prometheus-openstack-exporter.yaml',
                        type=argparse.FileType('r'))
    args = parser.parse_args()
    log.setLevel(logging.DEBUG)
    for logsock in ('/dev/log', '/var/run/syslog'):
        if path.exists(logsock):
            log.addHandler(logging.handlers.SysLogHandler(address=logsock))
    else:
        log.addHandler(logging.StreamHandler())
    config = yaml.safe_load(args.config_file.read())
    data_gatherer = DataGatherer()
    data_gatherer.start()
    server = ForkingHTTPServer(('', config.get('listen_port')), handler)
    server.serve_forever()