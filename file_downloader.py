"""Download with automatic resume.

1. Find full path to file to be downloaded.
    - Try to download file with Firefox and then stop it.
    - Go to Firefox history, click on file, select option 'copy download link'
2. Insert download link into download_file().
3. Run it: python file_downloader.py
4. File will be saved in local directory, or you can pass directory as a parameter to download_file() function
5. TODO: add progress bar to see download status.
    - For now you can "ls -la" in directory and see the file size, thus so-called monitoring download process.
    - Also you can open System Monitor tool and see current network download speed.

some torch links:  https://nero-mirror.stanford.edu/pypi/web/simple/torch/


2018-06-28 v1.0 by Cees Timmerman
2018-07-09 v1.1 Added If-Unmodified-Since header for consistency."""
import os, shutil, sys, time
import requests  # python -m pip install requests


def download_file(url, local_filename=None):
    if not local_filename:
        local_filename = url.split('/')[-1]

    resume_byte_pos = 0
    try:
        resume_byte_pos = os.path.getsize(local_filename)
        mtime = os.path.getmtime(local_filename)
    except:
        pass

    headers = {}
    if resume_byte_pos:
        headers.update(Range='bytes=%d-' % resume_byte_pos)
        # headers.update({"If-Range": time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(mtime))})  # Never matches?
        headers.update({"If-Unmodified-Since": time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(mtime))})
        print("Requesting", headers)

    with requests.get(
            url,
            headers=headers,
            stream=True,  # Save RAM.
            verify=False,
            allow_redirects=True
    ) as r:
        print("Received", r.headers)
        if r.status_code == 206:
            print('Resuming download')
            mode = 'ab'
        elif r.status_code == 200:
            print('(Re)starting download')
            mode = 'wb'
        else:
            raise Exception("Unexpected HTTP status in", r)
        with open(local_filename, mode) as f:
            shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    '''
    open('test_server_data', 'wb').write(b'1234567890'*20)
    sent = open('test_server_data', 'rb').read()
    print("Wrote:")
    print(sent[:50], sent[-50:])
    download_file('http://localhost:8000/test_server_data', 'downloaded_data')  # python -m http.server
    print("Received:")
    received = open('downloaded_data', 'rb').read()
    print(received[:50], received[-50:])
    '''

    download_file(

        'https://nero-mirror.stanford.edu/pypi/web/packages/88/95/90e8c4c31cfc67248bf944ba42029295b77159982f532c5689bcfe4e9108/torch-1.3.1-cp36-cp36m-manylinux1_x86_64.whl#sha256=0cec2e13a2e95c24c34f17d437f354ee2a40902e8d515a524556b350e12555dd'

    )


    """
    Received {'x-amz-id-2': '62GbFKUpcBCcdmNASaQOnkDKP8pqpkuQyZlJZ7E/E5XKRWH2UYHo3GoLgdH7mjoFGcTKlkgGL1k=', 'x-amz-request-id': 'D197A6E08A790C75', 'Last-Modified': 'Mon, 02 Jul 2018 10:08:26 GMT', 'ETag': '"1423c667f7a669b86fb726047c6622bb-12"', 'x-amz-version-id': 'tGHd1dEMyUmr0S68pWjuVsaUmSE.Cf1P', 'Content-Type': 'binary/octet-stream', 'Server': 'AmazonS3', 'Cache-Control': 'max-age=365000000, immutable, public', 'Accept-Ranges': 'bytes, bytes', 'Age': '617529', 'Content-Length': '93349595', 'Date': 'Mon, 09 Jul 2018 13:41:01 GMT', 'Connection': 'keep-alive', 'X-Served-By': 'cache-sea1036-SEA, cache-ams4431-AMS', 'X-Cache': 'HIT, HIT', 'X-Cache-Hits': '0, 0', 'X-Timer': 'S1531143662.786994,VS0,VE1', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload', 'X-Frame-Options': 'deny', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Robots-Header': 'noindex'}
    Requesting {'Range': 'bytes=58966016-'}
    Received {'x-amz-id-2': '62GbFKUpcBCcdmNASaQOnkDKP8pqpkuQyZlJZ7E/E5XKRWH2UYHo3GoLgdH7mjoFGcTKlkgGL1k=', 'x-amz-request-id': 'D197A6E08A790C75', 'Last-Modified': 'Mon, 02 Jul 2018 10:08:26 GMT', 'ETag': '"1423c667f7a669b86fb726047c6622bb-12"', 'x-amz-version-id': 'tGHd1dEMyUmr0S68pWjuVsaUmSE.Cf1P', 'Content-Type': 'binary/octet-stream', 'Server': 'AmazonS3', 'Cache-Control': 'max-age=365000000, immutable, public', 'Accept-Ranges': 'bytes, bytes', 'Age': '617810', 'Content-Range': 'bytes 58966016-93349594/93349595', 'Content-Length': '34383579', 'Date': 'Mon, 09 Jul 2018 13:45:43 GMT', 'Connection': 'keep-alive', 'X-Served-By': 'cache-sea1036-SEA, cache-ams4448-AMS', 'X-Cache': 'HIT, HIT', 'X-Cache-Hits': '0, 0', 'X-Timer': 'S1531143943.365115,VS0,VE1', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload', 'X-Frame-Options': 'deny', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Robots-Header': 'noindex'}
    Resuming download
    """