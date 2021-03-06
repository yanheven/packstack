$is_using_ssl_on_horizon = '%(CONFIG_HORIZON_SSL)s'

if $is_using_ssl_on_horizon == 'y' {
  nova_config {
    'DEFAULT/ssl_only': value => 'true';
    'DEFAULT/cert':     value => '/etc/nova/nova.crt';
    'DEFAULT/key':      value => '/etc/nova/nova.key';
  }
}

class {"nova::vncproxy":
    enabled => true,
}

class {"nova::consoleauth":
    enabled => true,
}

firewall { '001 novncproxy incoming':
    proto    => 'tcp',
    dport    => ['6080'],
    action   => 'accept',
}

