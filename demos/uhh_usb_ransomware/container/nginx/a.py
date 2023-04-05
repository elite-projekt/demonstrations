#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-only

import urllib.request

PROTOCOL = "http"
HOST = "127.0.0.1:5000"
PATH = "orchestration/start/demo/uhh_usb_ransomware/script_downloaded"

urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")  # nosec
