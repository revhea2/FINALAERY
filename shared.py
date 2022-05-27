# Flask-SQL Related
from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from utils.category import *

# Utilities
import re
from dotenv import load_dotenv
import pickle

# load environments
load_dotenv()
app = Flask(__name__)
app.secret_key = "yey"

# Set Database Connection
local = True

if local:
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'aery'
else:
    app.config['MYSQL_HOST'] = 'us-cdbr-east-05.cleardb.net'
    app.config['MYSQL_USER'] = 'b3930d314dd399'
    app.config['MYSQL_PASSWORD'] = 'cf94d6ba'
    app.config['MYSQL_DB'] = 'heroku_59d2dc346c440bc'

# Initialize MySQL
mysql = MySQL(app)
# Load Model
FILE_NAME = 'model/random_forest_model.sav'
loaded_model = pickle.load(open(FILE_NAME, 'rb'))