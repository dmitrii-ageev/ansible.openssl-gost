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
    'libengine-gost-openssl1.1',
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
    # Check if all the packages are installed
    for package in PACKAGES:
        assert host.package(package).is_installed, 'The %s package should be installed.' % package


def test_iscdhcp_configuration(host):
    # Server configuration directories must exists and belong to the user
    for directory in DIRECTORIES:
        target = host.file(directory)
        assert target.exists, 'Service configuration directory %s should exists' % directory
        assert target.is_directory, 'Service configuration directory %s must be a _directory_ and not something else!' % directory
        assert target.user == USER, 'Service configuration directory %s should belong to the %s user.' % (directory, USER)
        assert target.group == GROUP, 'Service configuration directory %s should belong to the %s group.' % (directory, GROUP)
        if directory == '/etc/ssl/private':
            assert target.mode == 0o0700, 'Service configuration directory %s should be accessible to root user only.' % directory
        else:
            assert target.mode == 0o0755, 'Service configuration directory %s should be accessible to anyone.' % directory

    # Configuration file must be in place
    configuration = host.file('/etc/ssl/%s.cnf' % SERVICE_NAME)
    assert configuration.exists, 'Service configuration file should exist.'
    assert configuration.mode == 0o0644, 'Service configuration file mode is incorrect.'

    # Configuration file should be valid
    assert configuration.contains('[ tsa ]'), \
        'Configuration file must have pre-defined settings!'
    assert configuration.contains('accuracy = secs:1, millisecs:500, microsecs:100'), \
        'Configuration file must have pre-defined settings!'
