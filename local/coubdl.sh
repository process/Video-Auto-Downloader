#!/usr/bin/env bash
set -e
youtube-dl -o 1.mp4 "$1"
youtube-dl -f html5-audio-high -o 1.mp3 "$1"
printf '\x00\x00' | dd of=1.mp4 bs=1 count=2 conv=notrunc
for i in `seq 1 100`; do echo "file '1.mp4'" >> 1.txt; done
ffmpeg -hide_banner -f concat -i 1.txt -i 1.mp3 -c copy -shortest -movflags faststart out.mp4
rm 1.mp4 1.mp3 1.txt

