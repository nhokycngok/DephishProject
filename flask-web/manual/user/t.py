from functools import wraps
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_pymongo import PyMongo, MongoClient
import json
import math
import re
from passlib.hash import pbkdf2_sha256
import uuid
import urllib.parse
# from werkzeug.wrappers import request

page_size = 15

index_tmp = -1

app = Flask(__name__)
app.secret_key = b'\x82}\xb1\xc0J\xa8\xd6\x81\xf9"\x9dm\xd7\xdf\xb7\xb4'
from user.models import User

# config connect to database
import urllib.parse

username = urllib.parse.quote_plus('dephish_rw')
password = urllib.parse.quote_plus('d3ph1sh@DB{rw}')
client = MongoClient('mongodb://%s:%s@127.0.0.1/dephish' % (username, password))

db = client.dephish



if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8080)
