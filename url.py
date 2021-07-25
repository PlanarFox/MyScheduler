import pycurl
import io
import urllib
from myjson import json_load

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

    print(url)
    curl = PycURLRunner(url, params, timeout, allow_redirects, headers, verify_keys)
    return curl(json, throw)