import os
import tempfile
import shutil
from threading import Thread

from youtube_dl import YoutubeDL
from flask import Flask, request
from qtfaststart import processor, exceptions

app = Flask(__name__)

VID_PATH = "/mnt/Data/Public/Videos/Other/Youtubes/vids/"
TMP_PATH = "/mnt/Data/Public/Videos/Other/Youtubes/downloader/temp"

def download(url):
  f = open(os.path.join(original_path, "log.txt"), "a")
  try:
    info_dict = ydl.extract_info(url, download=False)
    filename = ydl.prepare_filename(info_dict)
    if os.path.isfile(filename):
       print "File already downloaded"
       return ""
    ydl.download([url])
    tmp, outfile = tempfile.mkstemp(dir=TMP_PATH)
    os.close(tmp)
    try:
      processor.process(VID_PATH + filename, outfile)
      shutil.move(outfile, VID_PATH + filename)
    except exceptions.FastStartException:
      # stupid library throws exception if file is already setup properly
      print "Ignoring moov failure for already setup file"
    f.write("Downloaded " + url + '\n')
  except Exception as e:
    f.write("FAILED " + url + ' . because ' + e.message + '\n')
  f.close()

@app.route("/dlvid", methods=["GET"])
def dlvid():
  url = request.args.get('url')
  if 'results' in url and 'search_query' in url:
    # This is a search page
    return ""
  Thread(target=download, args=(url,)).start()
  return ""

if __name__ == "__main__":
  ydl_opts = { 'continuedl': True, 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]', 'noplaylist': True }
  ydl = YoutubeDL(ydl_opts)
  ydl.add_default_info_extractors()

  original_path = os.getcwd()
  os.chdir(VID_PATH)
  app.run(host="0.0.0.0", port=8080, threaded=True)
