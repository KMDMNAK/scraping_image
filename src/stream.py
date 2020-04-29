
from urllib import request
import zlib
import gzip
import urllib
print(urllib.__path__)

response = request.urlopen("https://datasets.imdbws.com/title.basics.tsv.gz")


def readByChunk(response):
    CHUNKSIZE = 1024
    c = 0
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)
    while c < 4:
        chunk = response.read(CHUNKSIZE)
        if (not chunk):
            break
        # decodedItem=gzip.decompress(chunk).decode("cp932")
        rv = str(dec.decompress(chunk).decode("utf-8"))
        print(rv)
        c += 1


def readByLine(response):
    c = 0
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)
    for line in response:
        print(dec.decompress(line).decode("utf-8"))
        c += 1
        if (c == 1):
            break


readByLine(response)
