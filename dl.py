import os
import tempfile
import shutil
import traceback
from threading import Thread

from youtube_dl import YoutubeDL
from flask import Flask, request
from qtfaststart import processor, exceptions

app = Flask(__name__)

VID_PATH = b"/mnt/Data/Public/Videos/Other/Youtubes/vids/"
TMP_PATH = b"/mnt/Data/Public/Videos/Other/Youtubes/downloader/temp"

log_file = None
active_urls = []

def log(txt):
  global log_file
  log_file.write(txt)
  log_file.flush()

def download(url):
  global ydl
  global active_urls
  if url in active_urls:
    print("Double download attempt. Blocking.")
    return
  active_urls.append(url)
  print(url)
  try:
    info_dict = ydl.extract_info(url, download=False)
    filename = ydl.prepare_filename(info_dict)
    filename = filename.encode('UTF-8')

    if os.path.isfile(filename):
       print("File already downloaded")
       return ""
    ydl.download([url])

    tmp, outfile = tempfile.mkstemp(dir=TMP_PATH)
    os.close(tmp)

    try:
      processor.process(VID_PATH + filename, outfile)
      shutil.move(outfile, VID_PATH + filename)
    except exceptions.FastStartException:
      # stupid library throws exception if file is already setup properly
      print("Ignoring moov failure for already setup file")
    log("Downloaded " + url + '\n')

  except Exception as e:
    log("FAILED " + url + '. Reason: ' + str(e) + '\n')
    log(traceback.format_exc())

  active_urls.remove(url)

@app.route("/dlvid", methods=["GET"])
def dlvid():
  url = request.args.get('url')

  if "results" in url and "search_query" in url:
    return ""

  if "/channel/" in url or "/user/" in url or "/playlist" in url or "/c/" in url:
    return ""

  Thread(target=download, args=(url,)).start()

  return ""


def init():
  global ydl, log_file
  ydl_opts = { 'continuedl': True, 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]', 'noplaylist': True}
  ydl = YoutubeDL(ydl_opts)
  ydl.add_default_info_extractors()

  log_file = open("log.txt", "a")
  os.chdir(VID_PATH)

if __name__ == "__main__":
  init()
  app.run(host="0.0.0.0", port=8080, threaded=True)

