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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:professional@localhost:5432/t6database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

########################################################
# Import Tables 
########################################################

from models import *

########################################################
# Routes (Classified)
########################################################

@app.route('/machine_regi', methods = ['POST'])
def machine_regi():
"""Create a machine in the database with: 
'machine_id', 'machine location', 'machine_type', 'machine_duration', 'sensors', usage'
Return with: registration status and error messages.
"""
    errors = []
    regi_status = True
    try:
        machine_id = request.json['machine_id']
        machine_type = request.json['type']
        duration = request.json['duration']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try: 
        # sensors will come as [{'sensor_id': XX, 'sensor_type': YY, 'deployment_date': ZZ}, ...]
        sensors = request.json['sensors']
    except: 
        sensors = []
    try:
        # usages will come as [{'start_timestamp': XX}, ...]
        usages = request.json['usages']
    except: 
        usages = []
    try:
        new_machine = Machine(machine_id = machine_id, machine_type = machine_type, duration = duration)
        db.session.add(new_machine) 
        db.session.commit() # this must be done before adding sensors and usages  

        for s in sensors: 
            new_sensor = Sensor(sensor_id = s['sensor_id'], sensor_type = s['sensor_type'], deployment_date = s['deployment_date']) 
            db.session.add(new_sensor) 
        for u in usages: 
            new_usage = Usage(machine_id = new_machine.machine_id, start_timestamp = u['start_timestamp'], end_time = (u['start_timestamp'] + new_machine.duration)) 
            db.session.add(new_usage) 
            
            db.session.commit() 
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors)

@app.route('/user_regi', methods = ['POST'])
def user_regi():
"""Create a user in the database with: 
'chat_id', 'username', 'modified_timestamp', 'inputs'
Return with: registration status and error messages.
"""
    errors = []
    regi_status = True
    try:
        chat_id = request.json['chat_id']
        username = request.json['username']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try: 
        # inputs will come as [{'service_type': XX, 'input_timestamp': YY, 'receive_timestamp': ZZ}, ...]
        inputs = request.json['inputs']
    except: 
        inputs = []
    try:
        new_user = User(chat_id = chat_id, username = username)
        db.session.add(new_user) 
        db.session.commit() # this must be done before adding inputs and prompt_reqs  

        for i in inputs: 
            new_input = User_input(chat_id = new_user.chat_id, service_type = i['service_type'], input_timestamp = i['input_timestamp']) 
            db.session.add(new_input) 
            db.session.commit() 
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors)

@app.route('/sensor_regi', methods = ['POST'])
def sensor_regi():
"""Create a user in the database with: 
'sensor_id', 'sensor_type', 'deployment_date', 'v_sensor_readings', 'm_sensor_readings'
Return with: registration status and error messages.
"""    
    errors = []
    regi_status = True
    try:
        sensor_id = request.json['sensor_id']
        sensor_type = request.json['sensor_type']
        deployment_date = request.json['deployment_date']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try: 
        # m_sensor_readings will come as [{'service_type': XX, 'input_timestamp': YY, 'receive_timestamp': ZZ}, ...]
        v_sensor_readings = request.json['v_sensor_readings']
    except: 
        v_sensor_readings = []
    try: 
        # inputs will come as [{'service_type': XX, 'input_timestamp': YY, 'receive_timestamp': ZZ}, ...]
        m_sensor_readings = request.json['m_sensor_readings']
    except: 
        m_sensor_readings = []
    try:
        new_sensor = Sensor(sensor_id = sensor_id, sensor_type = sensor_type, deployment_date = deployment_date)
        db.session.add(new_user) 
        db.session.commit() # this must be done before adding inputs and prompt_reqs  

        for i in inputs: 
            new_input = User_input(chat_id = new_user.chat_id, service_type = i['service_type'], input_timestamp = i['input_timestamp']) 
            db.session.add(new_input) 
            db.session.commit() 
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors)

@app.route('/receive_sensor_readings', methods = ['POST'])
def rcv_sensor_readings():
    errors = []
    regi_status = True
    try:
        sensor_id = request.json['sensor_id']
        timestamp = request.json['timestamp']
        sensor_figure = request.json['sensor_figure']
        status_conclusion = request.json['status_conclusion']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try:
        new_reading = Vib_sensor_data(sensor_id = sensor_id, timestamp = timestamp, sensor_figure = sensor_figure, status_conclusion = status_conclusion)
        db.session.add(new_reading) 
        db.session.commit() # this must be done before adding inputs and prompt_reqs  
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors)

@app.route('/receive_user_input', methods = ['POST'])
def rcv_user_input():
    errors = []
    regi_status = True
    try:
        chat_id = request.json['chat_id']
        service_type = request.json['service_type']
        input_timestamp = request.json['input_timestamp']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try:
        new_input = User_input(chat_id = chat_id, service_type = service_type, input_timestamp = input_timestamp)
        db.session.add(new_input) 
        db.session.commit() # this must be done before adding inputs and prompt_reqs  
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors)

@app.route('/record_usage', methods = ['POST'])
def record_usage():
    errors = []
    regi_status = True
    try:
        machine_id = request.json['machine_id']
        start_timestamp = request.json['start_timestamp']
        end_time = request.json['end_time']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
        return (regi_status, errors) 
    try:
        new_usage = Usage(machine_id = machine_id, start_timestamp = start_timestamp, end_time = end_time)
        db.session.add(new_usage) 
        db.session.commit() # this must be done before adding inputs and prompt_reqs  
    except Exception as e: 
        regi_status = False
        errors.append(str(e))
    return(regi_status, errors) 

########################################################
# Routes (Public)
########################################################

@app.route('/AvailiabilityInfo/', defaults = {'machine_id': '', 'machine_type': ''})
@app.route('/AvailiabilityInfo/<string:machine_id><string:machine_type>', methods=['GET']) 
def getAvaInfo(machine_id, machine_type):
"""Takes in chat_id, machine_id, machine_type
reply with specific machine usage
"""
    errors = []
    occupancy_of_machine = []

    if machine_id == '':
        if machine_type == '':
            machines = Machine.query.all()
        else:
            machines = Machine.query.filter_by(machine_type = machine_type)
    else: 
        machines = Machine.query.filter_by(machine_id = machine_id)

    now = datetime.datetime.utcnow()
    for m in machines:
        latest_usage = Usage.query.filter_by(machine_id = m.machine_id).order_by(Usage.end_time)[-1]
        if latest_usage.end_time <= now :
            occupancy_info = 'Unoccupied'
            time_remain = 0;
        else :
            occupancy_info = 'Occupied'
            time_remain = latest_usage.end_time.minute - now.minute
        occupancy_of_machine.append({str(m.machine_id): occupancy_info, 'Time-remaining': time_remain}) 
    
    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow()
        'Occupancy_of_machine': occupancy_of_machine
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id

    return jsonify(response)     

@app.route('/HistoryUsage/', defaults = {'machine_id': ''})
@app.route('/HistoryUsage/<string:machine_id>', methods=['GET']) 
def getHistoryUsage(machine_id):
"""Takes in chat_id, machine_id, machine_type
reply with specific machine usage
"""
    if machine_id == '':
        usages = Usage.query.all()
    else: 
        usages = Usage.query.filter_by(machine_id = machine_id).order_by(Usage.start_timestamp)

    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow()
        'Usage': occupancy_of_machine
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id
    
    return jsonify([u.serialize() for u in usages]) 

@app.route('/SensorData', defaults = {'sensor_id': ''})
@app.route('/SensorData/<string:sensor_id>', methods=['GET']) 
def getSensorData(sensor_id):
    return 

@app.route('/CreatePrompt',  methods = ['POST'])
def createPrompt():
    return 

@app.route('/UpdatePrompt',  methods = ['PUT'])
def updatePrompt():
    return 

########################################################
# Not sure what the following is for 
########################################################

if __name__ == '__main__':
    app.run(debug = True)