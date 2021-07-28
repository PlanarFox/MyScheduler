import pycurl
import io
import urllib
from myjson import json_load, json_dump

class URLException(Exception):
    pass

class PycURLRunner(object):

    def __init__(self, url, params, bind, timeout, allow_redirects, headers, verify_keys):
        """Constructor"""

        self.curl = pycurl.Curl()

        full_url = url if params is None else "%s?%s" % (url, urllib.parse.urlencode(params))
        self.curl.setopt(pycurl.URL, str(full_url))

        if bind is not None:
            self.curl.setopt(pycurl.INTERFACE, str(bind))

        self.curl.setopt(pycurl.FOLLOWLOCATION, allow_redirects)

        if headers is not None:            
            self.curl.setopt(pycurl.HTTPHEADER, [
                "%s: %s" % (str(key), str(value))
                for (key, value) in list(headers.items())
            ])

        if timeout is not None:
            self.curl.setopt(pycurl.TIMEOUT_MS, int(timeout * 1000.0))

        # True/false doesn't work here.  See
        # https://curl.haxx.se/libcurl/c/CURLOPT_SSL_VERIFYHOST.html
        self.curl.setopt(pycurl.SSL_VERIFYHOST, 2 if verify_keys else 0)
        self.curl.setopt(pycurl.SSL_VERIFYPEER, verify_keys)

        self.buf = io.BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, self.buf.write)



    def __call__(self, json, throw):
        """Fetch the URL"""

        try:
            self.curl.perform()
            status = self.curl.getinfo(pycurl.HTTP_CODE)
            # PycURL returns a zero for non-HTTP URLs
            if status == 0:
                status = 200
            text = self.buf.getvalue().decode()
        except pycurl.error as ex:
            code, message = ex.args
            status = 400
            text = message
        finally:
            self.curl.close()
            self.buf.close()

        # 200-299 is success; anything else is an error.
        if status < 200 or status > 299:

            if throw:
                raise URLException(text)
            else:
                return (status, text)

        if json:
            return (status, json_load(text))
        else:
            return (status, text)



def url_get( url,          # GET URL
             params=None,  # GET parameters
             json=True,    # Interpret result as JSON
             throw=True,   # Throw if status isn't 200
             timeout=None, # Seconds before giving up
             allow_redirects=True, # Allows URL to be redirected
             headers=None, # Hash of HTTP headers
             verify_keys=False  # Verify SSL keys
             ):
    """
    Fetch a URL using GET with parameters, returning whatever came back.
    """

    curl = PycURLRunner(url, params, None, timeout, allow_redirects, headers, verify_keys)
    return curl(json, throw)


def __content_type_data(content_type, headers, data):

    """Figure out the Content-Type based on an incoming type and data and
    return that plus data in a type that PycURL can handle."""

    assert(content_type is None or isinstance(content_type, str))
    assert(isinstance(headers, dict))

    if content_type is None or "Content-Type" not in headers:

        # Dictionaries are JSON
        if isinstance(data, dict):
            content_type = "application/json"
            data = json_dump(data)

        # Anything else is plain text.
        else:
            content_type = "text/plain"
            data = str(data)

    return content_type, data


def url_post( url,          # GET URL
              params={},    # GET parameters
              data=None,    # Data to post
              content_type=None,  # Content type
              bind=None,    # Bind request to specified address
              json=True,    # Interpret result as JSON
              throw=True,   # Throw if status isn't 200
              timeout=None, # Seconds before giving up
              allow_redirects=True, #Allows URL to be redirected
              headers={},   # Hash of HTTP headers
              verify_keys=False  # Verify SSL keys
              ):
    """
    Post to a URL, returning whatever came back.
    """

    content_type, data = __content_type_data(content_type, headers, data)
    headers["Content-Type"] = content_type

    curl = PycURLRunner(url, params, bind, timeout, allow_redirects, headers, verify_keys)

    curl.curl.setopt(pycurl.POSTFIELDS, data)

    return curl(json, throw)
