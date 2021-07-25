import socket
from urllib.parse import urlparse
import mydns
import url

def api_local_host():
    return 'localhost'

def api_root():
    return '/myscheduler'

def __host_per_rfc_2732(host):
    "Format a host name or IP for a URL according to RFC 2732"

    try:
        socket.inet_pton(socket.AF_INET6, host)
        return "[%s]" % (host)
    except socket.error:
        return host  # Not an IPv6 address

def api_host_port(hostport):
    """Return the host and port parts of a host/port pair"""
    if hostport is None:
        return (None, None)
    formatted_host = __host_per_rfc_2732(hostport)
    # The "bogus" is to make it look like a real, parseable URL.
    parsed = urlparse("bogus://%s" % (formatted_host))        
    return (None if parsed.hostname == "none" else parsed.hostname,
            parsed.port)

def api_url(host = None,
            path = None,
            port = None,
            protocol = None
            ):
    """Format a URL for use with the pScheduler API."""

    host = api_local_host() if host is None else str(host)
    # Force the host into something valid for DNS
    # See http://stackoverflow.com/a/25103444/180674
    try:
        host = host.encode('idna').decode("ascii")
    except UnicodeError:
        raise ValueError("Invalid host '%s'" % (host))
    host = __host_per_rfc_2732(host)

    if path is not None and path.startswith('/'):
        path = path[1:]

    if protocol is None:
        protocol = 'https'

    return protocol + '://' \
        + host \
        + ('' if port is None else (':' + str(port))) \
        + api_root() + '/'\
        + ('' if path is None else str(path))

def api_url_hostport(hostport=None,
            path=None,
            protocol=None
            ):
    """Format a URL for use with the pScheduler API where the host name
    may include a port."""
    (host, port) = api_host_port(hostport)
    return api_url(host=host, port=port, path=path, protocol=protocol)


def api_has_MyScheduler(hostport, timeout=5):
    if hostport is None:
        hostport = api_host_port()
    
    host, port = api_host_port(hostport)

    resolved = None
    for ip_version in [4, 6]:
        resolved = mydns.dns_resolve(host,
                               ip_version=ip_version,
                               timeout=timeout)
        if resolved:
            break

    if not resolved:
        return False

    status, raw_spec = url.url_get(api_url_hostport(hostport),
                               timeout=timeout,
                               throw=False,
                               json=False,
    )

    return status == 200
    