Downloads videos specified in ids.txt
---
Sometimes Google will block our IP with 429s while running this script
To avoid this, a SOCKS proxy can be used. I don't know how these proxies
avoid getting blocked

Can be used like this:
$ https_proxy=socks5://$HOST:$PORT/ python local-dl.py

