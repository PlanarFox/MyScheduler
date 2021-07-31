import queue
import socket
import threading
import dns.reversename
import dns.resolver 

def __check_ip_version__(ip_version):
    if not ip_version in [4, 6]:
        raise ValueError("Invalid IP version '%s'; must be 4 or 6" % (str(ip_version)))

def __dns_resolve_host(host, ip_version, timeout):
    """
    Resolve a host using the system's facilities
    """
    family = socket.AF_INET if ip_version == 4 else socket.AF_INET6

    def proc(host, family, timing_queue):
        try:
            timing_queue.put(socket.getaddrinfo(host, 0, family))
        except socket.gaierror as ex:
            # TODO: Would be nice if we could isolate just the not
            # found error.
            timing_queue.put([])
        except socket.timeout:
            # Don't care, we just want the queue to be empty if
            # there's an error.
            pass

    timing_queue = queue.Queue()
    thread = threading.Thread(target=proc, args=(host, family, timing_queue))
    thread.setDaemon(True)
    thread.start()
    try:
        results = timing_queue.get(True, timeout)
        if len(results) == 0:
            return None
        family, socktype, proto, canonname, sockaddr = results[0]
    except queue.Empty:
        return None

    # NOTE: Don't make any attempt to kill the thread, as it will get
    # Python all confused if it holds the GIL.

    (ip) = sockaddr
    return str(ip[0])

def dns_resolve(host,
                query=None,
                ip_version=4,
                timeout=2
                ):
    """
    Resolve a hostname to its A record, returning None if not found or
    there was a timeout.
    """
    __check_ip_version__(ip_version)

    if query is None:

        # The default query is for a host,

        return __dns_resolve_host(host, ip_version, timeout)

    else:

        # Any other explicit query value is forced to use DNS.

        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = timeout
            resolver.lifetime = timeout
            if query is None:
                query = 'A' if ip_version == 4 else 'AAAA'
            answers = resolver.query(host, query)
        except (dns.exception.Timeout,
                dns.name.EmptyLabel,
                dns.resolver.NXDOMAIN,
                dns.resolver.NoAnswer,
                dns.resolver.NoNameservers):
            return None

        return str(answers[0])
