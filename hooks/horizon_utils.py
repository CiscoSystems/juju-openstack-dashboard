import horizon_contexts
import charmhelpers.contrib.openstack.context as context
import charmhelpers.contrib.openstack.templating as templating
import subprocess
from collections import OrderedDict

from charmhelpers.contrib.openstack.utils import (
    get_os_codename_package
)

PACKAGES = [
    "openstack-dashboard", "python-keystoneclient", "python-memcache",
    "memcached", "haproxy", "python-novaclient",
    "nodejs", "node-less"
]

LOCAL_SETTINGS = "/etc/openstack-dashboard/local_settings.py"
HAPROXY_CONF = "/etc/haproxy/haproxy.cfg"
APACHE_CONF = "/etc/apache2/conf.d/openstack-dashboard.conf"
PORTS_CONF = "/etc/apache2/ports.conf"
APACHE_SSL = "/etc/apache2/sites-available/default-ssl"
APACHE_DEFAULT = "/etc/apache2/sites-available/default"

TEMPLATES = 'templates'

CONFIG_FILES = OrderedDict([
    (LOCAL_SETTINGS, {
        'hook_contexts': [horizon_contexts.HorizonContext(),
                          horizon_contexts.IdentityServiceContext()],
        'services': ['apache2']
    }),
    (HAPROXY_CONF, {
        'hook_contexts': [context.HAProxyContext(),
                          horizon_contexts.HAProxyContext()],
        'services': ['haproxy'],
    }),
    (APACHE_CONF, {
        'hook_contexts': [horizon_contexts.HorizonContext()],
        'services': ['apache2'],
    },)
    (APACHE_SSL, {
        'hook_contexts': [horizon_contexts.ApacheSSLContext(),
                          horizon_contexts.ApacheContext()],
        'services': ['apache2'],
    },)
    (APACHE_DEFAULT, {
        'hook_contexts': [horizon_contexts.ApacheContext()],
        'services': ['apache2'],
    },)
    (PORTS_CONF, {
        'hook_contexts': [horizon_contexts.ApacheContext()],
        'services': ['apache2'],
    },)
])


def register_configs():
    # Register config files with their respective contexts.
    release = get_os_codename_package('openstack-dashboard', fatal=False) or \
        'essex'
    configs = templating.OSConfigRenderer(templates_dir=TEMPLATES,
                                          openstack_release=release)

    confs = [LOCAL_SETTINGS,
             HAPROXY_CONF,
             APACHE_CONF,
             APACHE_SSL,
             APACHE_DEFAULT,
             PORTS_CONF]

    for conf in confs:
        configs.register(conf, CONFIG_FILES[conf]['hook_contexts'])

    return configs


def restart_map():
    '''
    Determine the correct resource map to be passed to
    charmhelpers.core.restart_on_change() based on the services configured.

    :returns: dict: A dictionary mapping config file to lists of services
                    that should be restarted when file changes.
    '''
    _map = []
    for f, ctxt in CONFIG_FILES.iteritems():
        svcs = []
        for svc in ctxt['services']:
            svcs.append(svc)
        if svcs:
            _map.append((f, svcs))
    return OrderedDict(_map)


def enable_ssl():
    subprocess.call(['a2ensite', 'default-ssl'])
    subprocess.call(['a2enmod', 'ssl'])
