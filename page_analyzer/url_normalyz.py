from urllib.parse import urlparse


def normalize_url(url_string):
    parsed_url = urlparse(url_string)
    return f"{parsed_url.scheme}://{parsed_url.netloc}".lower()