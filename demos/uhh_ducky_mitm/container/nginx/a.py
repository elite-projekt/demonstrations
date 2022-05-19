#!/usr/bin/env python3

import urllib.request

PROTOCOL = "http"
HOST = "127.0.0.1:5000"
PATH = "orchestration/start/demo/uhh_ducky_mitm/script_downloaded"

urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")  # nosec
