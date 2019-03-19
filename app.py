from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy 
import datetime

# your code starts here 
app = Flask(__name__) 
app.debug = True

########################################################
# Define DB configration info 
########################################################

# psql_username = 'T6user'
# psql_password = "professional" 
# psql_hostname = 'localhost' # 127.0.0.1
# psql_port = 5432
# psql_database_name = 't6database'
# psql_DB_URL = 'postgresql://{}:{}@{}:{}/{}'.format(psql_username, psql_password, psql_hostname, psql_port, psql_database_name)
psql_DB_URI = 'postgresql://T6user:professional@localhost:5432/t6database'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://t6testuser:t6user@localhost:5432/t6testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

########################################################
# Import Tables 
########################################################

from models import *

########################################################
# Routes (Classified)
########################################################

########################################################
# Not sure what the following is for 
########################################################

if __name__ == '__main__':
    app.run(debug = True)
