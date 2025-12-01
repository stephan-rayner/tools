#!/usr/bin/env python

import sys

def clean_url(url):
     principal_url = url.split("&tr=")[0]
     print(principal_url, end="")

data = sys.stdin.read()
clean_url(data)
