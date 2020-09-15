from os.path import exists, getsize, basename, isdir, join
from urllib.parse import urlparse

import requests
from tqdm import tqdm


def download(uri, output=None):
    head = requests.head(uri)
    accept_ranges = head.headers.get('Accept-Ranges', None) == 'bytes'
    content_length = int(head.headers.get('Content-Length', 0))
    basename_ = basename(urlparse(uri).path)

    if output is None:
        output = basename_
    elif isdir(output):
        output = join(output, basename_)

    headers_ = {}
    size_ = 0

    if exists(output) and accept_ranges:
        size_ = getsize(output)
        headers_['Range'] = f"bytes={size_}-"

    resp = requests.get(uri, stream=True, headers=headers_)
    filename_ = basename(output)
    progress_bar_ = tqdm(total=content_length, unit='iB', unit_scale=True, desc=filename_, initial=size_)
    with open(output, 'ab') as file:
        for chunk in resp.iter_content(chunk_size=4096):
            file.write(chunk)
            progress_bar_.update(len(chunk))

    progress_bar_.close()
