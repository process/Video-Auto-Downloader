import time
import sys
sys.path.append("..")

from dl import download, init

if __name__ != "__main__":
  print("This should be run explicitly")

ids = [id.strip() for id in open('ids.txt')]
init()
for vid in ids:
  download(vid)

