package { 'python':
    ensure => 2.7,
}

package { 'python-virtualenv':
    ensure => present,
}

package { 'nginx':
    ensure => present,
}