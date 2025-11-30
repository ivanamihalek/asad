#! /usr/bin/python3

# this is for Apache - does not matter in dev

import sys
import logging

from flask import Flask
from app import app

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/dogmatic_org")

app.run()

