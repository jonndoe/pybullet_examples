
# Simple downloading with progress indicator, by Cees Timmerman, 16mar12.

import urllib.request, urllib.error, urllib.parse

remote = r"http://some.big.file"
#remote = r"/media/habrauser/easystore/MASTER_FOLDER/COMPUTERS/02 SOFT FOR WINDOWS/CES51.exe"
local = r"."

u = urllib.request.urlopen(remote)
h = u.info()
totalSize = int(h["Content-Length"])

print("Downloading %s bytes..." % totalSize, end=' ')
fp = open(local, 'wb')

blockSize = 8192 #100000 # urllib.urlretrieve uses 8192
count = 0
while True:
    chunk = u.read(blockSize)
    if not chunk: break
    fp.write(chunk)
    count += 1
    if totalSize > 0:
        percent = int(count * blockSize * 100 / totalSize)
        if percent > 100: percent = 100
        print("%2d%%" % percent, end=' ')
        if percent < 100:
            print("\b\b\b\b\b", end=' ')  # Erase "NN% "
        else:
            print("Done.")

fp.flush()
fp.close()
if not totalSize:
    print()

