from urlparse import urlparse

def parse(self, response):
    parsed_uri = urlparse(response.url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print domain

    