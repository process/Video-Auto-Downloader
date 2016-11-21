from youtube_dl import YoutubeDL
from flask import Flask, request
app = Flask(__name__)

import os
	
@app.route("/dlvid")
def dlvid():
  url = request.args.get('url')
  
  #f = open(os.path.join(original_path, "log.txt"), "a")
  f = open(os.path.join(original_path, "todo.txt"), "a")
  
  try:
    #ydl.download([url])
    #f.write("Downloaded " + url + '\n')
	f.write("pls download this -> " + url + '\n')
  except Exception as e:
    f.write("FAILED " + url + ' . because' + e + '\n')

  f.close()
  
  return ""

if __name__ == "__main__":
  ydl_opts = { 'continuedl': True, 'format': 'bestvideo[ext=mp4]+bestaudio', 'noplaylist': True }
  ydl = YoutubeDL(ydl_opts)
  ydl.add_default_info_extractors()

  original_path = os.getcwd()
  os.chdir("Z:/Videos/Other/Youtubes/vids")
  app.run(port=8080)