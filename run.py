#! /usr/bin/env python3
from flask import Flask

from app import app

if __name__ == '__main__':
    app.run(debug=True)
