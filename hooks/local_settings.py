###
# Juju managed local_settings.py for Horizon / openstack-dashboard
# Closely based on local_settings.py.example shipped with Horizon
import os
import sys

# various defaults shipped in this file in ubuntu packaging.
# these will be used if juju generated configuration doesn't exist (yet)
OPENSTACK_HOST="127.0.0.1"
OPENSTACK_KEYSTONE_URL = "http://%s:5000/v2.0" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_ADMIN_URL = "http://%s:35357/v2.0" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROD = False
USE_SSL = False
# end defaults

sys.path.append("/etc/openstack-dashboard")
try:
    # import /etc/openstack-dashboard/juju_dashboard_config.py
    # which contains charm generated configuration
    import juju_dashboard_config

    # use the bits of config that have been set, rely on defaults
    # for those that haven't.
    if hasattr(juju_dashboard_config, "KEYSTONE_HOST"):
        OPENSTACK_HOST = juju_dashboard_config.KEYSTONE_HOST
    if hasattr(juju_dashboard_config, "KEYSTONE_URL"):
        OPENSTACK_KEYSTONE_URL = juju_dashboard_config.KEYSTONE_URL
    if hasattr(juju_dashboard_config, "KEYSTONE_ADMIN_URL"):
        OPENSTACK_KEYSTONE_ADMIN_URL = juju_dashboard_config.KEYSTONE_ADMIN_URL
    if hasattr(juju_dashboard_config, "KEYSTONE_ROLE"):
        OPENSTACK_KEYSTONE_ROLE = juju_dashboard_config.KEYSTONE_ROLE
except ImportError:
    # juju config is missing, but fall back to defaults set above.
    print "Could not import juju_dashboard_config. Falling back to defaults"

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/openstack-dashboard/dashboard_openstack.sqlite',
        'TEST_NAME': os.path.join(LOCAL_PATH, 'test.sqlite3'),
    },
}

# We recommend you use memcached for development; otherwise after every reload
# of the django development server, you will have to login again. To use
# memcached set CACHE_BACKED to something like 'memcached://127.0.0.1:11211/' 
CACHE_BACKEND = 'locmem://'

# Send email to the console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Or send them to /dev/null
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Configure these for your outgoing email host
# EMAIL_HOST = 'smtp.my-company.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'djangomail'
# EMAIL_HOST_PASSWORD = 'top-secret!'

HORIZON_CONFIG = {
    'dashboards': ('nova', 'syspanel', 'settings',),
    'default_dashboard': 'nova',
    'user_home': 'dashboard.views.user_home',
}

# The number of Swift containers and objects to display on a single page before
# providing a paging element (a "more" link) to paginate results.
SWIFT_PAGINATE_LIMIT = 1000

# Configure quantum connection details for networking
QUANTUM_ENABLED = False
QUANTUM_URL = '%s'  % OPENSTACK_HOST
QUANTUM_PORT = '9696'
QUANTUM_TENANT = '1234'
QUANTUM_CLIENT_VERSION='0.1'

# If you have external monitoring links, eg:
# EXTERNAL_MONITORING = [
#     ['Nagios','http://foo.com'],
#     ['Ganglia','http://bar.com'],
# ]

LOGGING = {
        'version': 1,
        # When set to True this will disable all logging except
        # for loggers specified in this configuration dictionary. Note that
        # if nothing is specified here and disable_existing_loggers is True,
        # django.db.backends will still log unless it is disabled explicitly.
        'disable_existing_loggers': False,
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
                },
            'console': {
                # Set the level to "DEBUG" for verbose output logging.
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                },
            },
        'loggers': {
            # Logging from django.db.backends is VERY verbose, send to null
            # by default.
            'django.db.backends': {
                'handlers': ['null'],
                'propagate': False,
                },
            'horizon': {
                'handlers': ['console'],
                'propagate': False,
            },
            'novaclient': {
                'handlers': ['console'],
                'propagate': False,
            },
            'keystoneclient': {
                'handlers': ['console'],
                'propagate': False,
            },
            'nose.plugins.manager': {
                'handlers': ['console'],
                'propagate': False,
            }
        }
}

# How much ram on each compute host?
COMPUTE_HOST_RAM_GB = 16
