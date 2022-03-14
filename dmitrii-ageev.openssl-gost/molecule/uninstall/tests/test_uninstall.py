import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

ROOT = 'root'
USER = ROOT
GROUP = USER
SERVICE_NAME = 'openssl'
PACKAGES = [
    'openssl',
    'libengine-gost-openssl1.1'
    'ca-certificates'
]
DIRECTORIES = [
    '/etc/ssl',
    '/etc/ssl/certs',
    '/etc/ssl/private'
]


def test_os_type(host):
    assert host.system_info.type == 'linux', 'Only the Linux operating system is supported!'


def test_package(host):
    # Check if the packages were removed
    for package in PACKAGES:
        assert not host.package(package).is_installed, 'The %s package should be removed.' % package


def test_configuration(host):
    # Service directories should be removed
    for directory in DIRECTORIES:
        target = host.file(directory)
        assert not target.exists, 'Service directory %s should be removed.' % directory
