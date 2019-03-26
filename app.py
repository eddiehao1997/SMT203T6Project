from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy 
import datetime
import os

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
# psql_DB_URI = 'postgresql://t6testuser:t6user@localhost:5432/ilndrytest'
psql_DB_URI = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = psql_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

########################################################
# Import Tables 
########################################################

from models import *

########################################################
# Routes (Classified)
########################################################

@app.route('/machine_regi', methods = ['POST']) # Status: tested (bowen)
def machine_regi():
    errors = []
    regi_status = True
    machine_info = []
    try:
        machine_id = request.json['machine_id']
        machine_type = request.json['type']
        duration = request.json['duration']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
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
    if regi_status:
        try:
            new_machine = Machine(machine_id = machine_id, machine_type = machine_type, duration = duration)
            db.session.add(new_machine) 
            db.session.commit() # this must be done before adding sensors and usages  
            for s in sensors: 
                new_sensor = Sensor(sensor_id = s['sensor_id'], sensor_type = s['sensor_type'], deployment_date = s['deployment_date']) 
                db.session.add(new_sensor) 
                db.session.commit() 
            for u in usages: 
                new_usage = Usage(machine_id = new_machine.machine_id, start_timestamp = u['start_timestamp'], end_time = (u['start_timestamp'] + new_machine.duration)) 
                db.session.add(new_usage) 
                db.session.commit() 
            machine_info = new_machine.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))

    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "new_machine_info": machine_info
    }
    return jsonify(response)

@app.route('/user_regi', methods = ['POST']) # Status: tested (bowen)
def user_regi():
    errors = []
    regi_status = True
    user_info = []
    try:
        chat_id = request.json['chat_id']
        username = request.json['username']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    try: 
        # inputs will come as [{'service_type': XX, 'input_timestamp': YY, 'receive_timestamp': ZZ}, ...]
        inputs = request.json['inputs']
    except: 
        inputs = []

    if regi_status:
        try:
            new_user = User(chat_id = chat_id, username = username)
            db.session.add(new_user) 
            db.session.commit() # this must be done before adding inputs and prompt_reqs  

            for i in inputs: 
                new_input = User_input(chat_id = new_user.chat_id, service_type = i['service_type'], input_timestamp = i['input_timestamp']) 
                db.session.add(new_input) 
                db.session.commit() 
            user_info = new_user.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))

    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "new_user_info": user_info
    }
    return jsonify(response)

@app.route('/sensor_regi', methods = ['POST']) # Status: tested (bowen)
def sensor_regi():  
    errors = []
    regi_status = True
    sensor_info = []
    try:
        sensor_id = request.json['sensor_id']
        machine_id = request.json['machine_id']
        sensor_type = request.json['sensor_type']
        deployment_date = request.json['deployment_date']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')
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
    
    if regi_status:
        try:
            new_sensor = Sensor(sensor_id = sensor_id, machine_id = machine_id,sensor_type = sensor_type, deployment_date = deployment_date)
            db.session.add(new_sensor) 
            db.session.commit() # this must be done before adding inputs and prompt_reqs  
            for v in v_sensor_readings: 
                new_reading = Vib_sensor_data(sensor_id = new_sensor.sensor_id, timestamp = v['timestamp'], sensor_figure = v['sensor_figure'], status_conclusion =v['status_conclusion']) 
                db.session.add(new_reading) 
                db.session.commit() 
            for m in m_sensor_readings: 
                new_reading = Mot_sensor_data(sensor_id = new_sensor.sensor_id, timestamp = m['timestamp'], sensor_figure = m['sensor_figure'], status_conclusion =m['status_conclusion']) 
                db.session.add(new_reading) 
                db.session.commit() 
            sensor_info = new_sensor.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))
    
    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "new_sensor_info": sensor_info
    }
    return jsonify(response)

@app.route('/receive_sensor_readings', methods = ['POST']) # Status: tested (bowen)
def rcv_sensor_readings():
    errors = []
    regi_status = True
    reading_info = []
    try:
        sensor_id = request.json['id']
        timestamp = request.json['lastSeen']
        sensor_figure = request.json['eddystoneUrl']['url']
        # status_conclusion = request.json['status_conclusion']
        status_conclusion = True
        sensor_figure = sensor_figure.split(',')[1]
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    if regi_status:
        curr_sensor = Sensor.query.filter_by(sensor_id = sensor_id)
        try:
            new_reading = Vib_sensor_data(sensor_id = sensor_id, timestamp = timestamp, sensor_figure = sensor_figure, status_conclusion = status_conclusion)
            db.session.add(new_reading) 
            db.session.commit() # this must be done before adding inputs and prompt_reqs  
            
            curr_sensor.v_sensor_readings.append(new_reading)
            db.session.commit()

            reading_info = new_reading.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))

    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "new_reading_info": reading_info
    }
    return jsonify(response)

@app.route('/receive_user_input', methods = ['POST']) # Status: tested (bowen)
def rcv_user_input():
    errors = []
    regi_status = True
    input_info = []
    try:
        chat_id = request.json['chat_id']
        service_type = request.json['service_type']
        input_timestamp = request.json['input_timestamp']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    if regi_status:
        try:
            curr_user = User.query.filter_by(chat_id)
            if curr_user is None:
                regi_status = False
                errors.append('User not exist!')
            else:
                new_input = User_input(chat_id = chat_id, service_type = service_type, input_timestamp = input_timestamp)
                db.session.add(new_input) 
                db.session.commit() # this must be done before adding inputs and prompt_reqs  
                
                curr_user.inputs.append(new_input)
                db.session.commit()

            input_info = new_input.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))

    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "input_info": input_info
    }
    return jsonify(response)

@app.route('/record_usage', methods = ['POST']) # Status: tested (bowen)
def record_usage():
    errors = []
    regi_status = True
    usage_info = []
    try:
        machine_id = request.json['machine_id']
        start_timestamp = request.json['start_timestamp']
        end_time = request.json['end_time']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    if regi_status:
        try:
            new_usage = Usage(machine_id = machine_id, start_timestamp = start_timestamp, end_time = end_time)
            db.session.add(new_usage) 
            db.session.commit() # this must be done before adding inputs and prompt_reqs 
            curr_machine = Machine.query.filter_by(machine_id = machine_id).first()
            curr_machine.usages.append(new_usage) 

            usage_info = new_usage.serialize()
        except Exception as e: 
            regi_status = False
            errors.append(str(e))

    response = {
        "regi_status": regi_status,
        "error_messages": errors,
        "usage_info": usage_info
    }
    return jsonify(response)

@app.route('/DeletePrompt/<int:usage_id>', methods=['DELETE']) 
def delete_prompt(usage_id): 
    errors = []
    delete_status = True
    try:
        curr_prompt = Prompt.query.get(usage_id) 
        if curr_prompt is None:
            delete_status = False
            errors.append('No record found!')
        else: 
            db.session.delete(curr_prompt)
            db.session.commit() 
            errors.append('Prompt for user <{}> machine <{}> was deleted'.format(curr_prompt.chat_id, curr_prompt.machine_id))
    except Exception as e:
        delete_status = False
        errors.append(str(e))

    response = {
        'Delete_status': delete_status,
        'error_messages': errors
    }
    return jsonify(response)

@app.route('/DeleteUser/<int:chat_id>', methods=['DELETE']) 
def delete_user(chat_id): 
    errors = []
    delete_status = True
    try:
        curr_user = User.query.get(chat_id) 
        if curr_user is None:
            delete_status = False
            errors.append('No user found!')
        else: 
            db.session.delete(curr_user)
            db.session.commit() 
            errors.append('User <{}> is deleted'.format(curr_user.chat_id))
    except Exception as e:
        delete_status = False
        errors.append(str(e))

    response = {
        'Delete_status': delete_status,
        'error_messages': errors
    }
    return jsonify(response)

########################################################
# Routes (Public)
########################################################

@app.route('/AvailiabilityInfo/', defaults = {'machine_id': '', 'machine_type': ''})
@app.route('/AvailiabilityInfo/<string:machine_id><string:machine_type>', methods=['GET']) 
def getAvaInfo(machine_id, machine_type):  # Status: tested (bowen)
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
        latest_usage = Usage.query.filter_by(machine_id = m.machine_id).order_by(Usage.end_time.desc()).first()
        if latest_usage is None:
            occupancy_info = 'Machine off line'
            time_remain = 9999;
        else:
            if latest_usage.end_time <= now :
                occupancy_info = 'Unoccupied'
                time_remain = 0;
            else :
                occupancy_info = 'Occupied'
                time_remain = latest_usage.end_time.minute - now.minute
        occupancy_of_machine.append({'Machine_id': str(m.machine_id), 'Occupancy_info': occupancy_info, 'Time-remaining': time_remain}) 
    
    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow(),
        'Occupancy_of_machine': occupancy_of_machine
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id

    return jsonify(response)   

@app.route('/HistoryUsage/', defaults = {'machine_id': ''})
@app.route('/HistoryUsage/<string:machine_id>', methods=['GET']) # Status: tested (bowen)
def getHistoryUsage(machine_id): 
# """Takes in chat_id, machine_id, machine_type
# reply with specific machine usage
# """
    errors = []
    usages = []
    curr_usage = []

    if machine_id == '':
        machines = Machine.query.all()
    else: 
        machines = Machine.query.filter_by(machine_id = machine_id)

    for m in machines:
        curr_usage = Usage.query.filter_by(machine_id = m.machine_id).order_by(Usage.start_timestamp)
        usages.append({'Machine_ID': m.machine_id, 'Usage_detail': [c.srl_without_id() for c in curr_usage]})

    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow(),
        'Usage_info': usages
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id
    
    return jsonify(response) 

@app.route('/readingData/', methods=['GET']) 
def getReadingData():
    errors = []
    modi_status = True

    readings = Vib_sensor_data.query.all()

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id
    
    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow(),
        'Reading_info': [r.serialize() for r in readings]
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id

    return jsonify(response) 

@app.route('/SensorData/', defaults = {'sensor_id': ''})
@app.route('/SensorData/<string:sensor_id>', methods=['GET']) 
def getSensorData(sensor_id):
    errors = []
    modi_status = True

    if sensor_id == '':
        sensors = Sensor.query.all()
    else: 
        sensors = Sensor.query.filter_by(sensor_id = sensor_id)

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id
    
    response = {
        'Chat_id': None,
        'Timestamp': datetime.datetime.utcnow(),
        'Sensor_info': [s.serialize() for s in sensors]
    }

    if 'chat_id' in request.args:
        chat_id = request.args.get('chat_id')
        response['Chat_id'] = chat_id
    
    return jsonify(response) 

@app.route('/CreatePrompt', methods = ['POST'])
def createPrompt():
    errors = []
    regi_status = True
    prompt_time = ''

    try:
        machine_id = request.json['machine_id']
        time_interval = request.json['time_interval']
        chat_id = request.json['chat_id']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    curr_prompt = Prompt.query.filter_by(machine_id = machine_id)
    if curr_prompt is None:
            
        curr_usage = Usage.query.filter_by(machine_id = machine_id).order_by(Usage.end_time.desc()).first()
        now = datetime.datetime.utcnow()
        if curr_usage is None:
            regi_status = False
            errors.append('No available usage can be found for machine <{}>!'.format(machine_id))
        else:
            if curr_usage.end_time < now:
                curr_usage = None
                regi_status = False
                errors.append('No available usages can be found for machine <{}>!'.format(machine_id))
            else: 
                ending_time = curr_usage.end_time
                prompt_time = ending_time - time_interval

        curr_user = User.query.filter_by(chat_id = chat_id).first()
        if curr_user is None:
            regi_status = False
            errors.append('No user <> can be found!'.format(chat_id))

        new_prompt = Prompt(chat_id = chat_id, usage_id = curr_usage.id, machine_id = machine_id, start_timestamp = start_timestamp, time_to_prompt = prompt_time, ending_time = ending_time)
        db.session.add(new_usage) 
        db.session.commit()

        curr_usage.prompt_req.append(new_prompt)
        db.session.commit() 
        curr_user.prompt_reqs.append(new_prompt)
        db.session.commit() 

    else: 
        regi_status = False
        errors.append('This machine has already been registrated with a promput request')

    response = {
        'Chat_id': chat_id,
        'Timestamp': datetime.datetime.utcnow(),
        'Machine_NO': machine_id,
        'prompt_status': regi_status,
        'Error_Message': errors,
        'Prompt_Timing': prompt_time
    }

    return jsonify(response)

@app.route('/UpdatePrompt', methods = ['PUT'])
def updatePrompt():
    errors = []
    regi_status = True

    try:
        machine_id = request.json['machine_id']
        time_interval = request.json['time_interval']
        chat_id = request.json['chat_id']
    except KeyError as e:
        regi_status = False
        errors.append(str(e) + ':Please chesk your parameters.')

    if regi_status:
        try:
            curr_prompt = Prompt.query.filter_by(usage_id = usage_id).first()
            if curr_prompt is None:
                errors.append('No prompt request found!')
            else:
                ending_time = curr_prompt.ending_time
                curr_prompt.time_to_prompt = ending_time - time_interval
        except Exception as e:
            regi_status = False
            errors.append(str(e) + ':Please chesk your parameters.')

    response = {
        'Chat_ID': chat_id,
        'Timestamp': datetime.datetime.utcnow(),
        'Modification_status': modi_status,
        'Error_Message': errors,
        'Prompt_info': curr_prompt.serialize()
    }
    return (response)

########################################################
# Not sure what the following is for 
########################################################

if __name__ == '__main__':
    app.run(debug = True)