#! /usr/bin/env python3
from flask import Flask

app = Flask(__name__)

# Import routes at the bottom to avoid circular dependencies
from routes import *