from app import db
import datetime

########################################################
# Many to Many Tables
########################################################

########################################################
# One to Many Tables
########################################################

class User(db.Model):
    __tablename__ = 'user'

    chat_id = db.Column(db.String(10), primary_key = True, autoincrement=False)
    username = db.Column(db.String(80), unique = False, nullable = False)
    modified_timestamp = db.Column(db.DateTime, default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)

    # one-to-many relationship 
    inputs = db.relationship('User_input',  back_populates = 'user', cascade = 'all', lazy = True, uselist = True)
    prompt_reqs = db.relationship('Prompt', back_populates = 'user', cascade = 'all', lazy = True, uselist = True)

    # many-to-many relationship 

    # build-in functions
    def __init__(self, chat_id, username, inputs = None, prompt_reqs = None): 
        self.chat_id = chat_id
        self.username = username
        inputs = [] if inputs is None else inputs
        self.inputs = inputs
        prompt_reqs = [] if prompt_reqs is None else prompt_reqs
        self.prompt_reqs = prompt_reqs

    def serialize(self):
        return {
            'chat_id': self.chat_id,
            'username': self.username,
            'modified_timestamp': self.modified_timestamp,
            'user_inputs': [i.serialize() for i in self.inputs],
            'prompt_requests': [r.serialize() for r in self.prompt_reqs]
        }

class User_input(db.Model):
    __tablename__ = 'user_input'

    id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.String, db.ForeignKey('user.chat_id'), nullable = False)
    service_type = db.Column(db.String, unique = False, nullable = False)
    input_timestamp = db.Column(db.DateTime, unique = False, nullable = False)
    receive_timestamp = db.Column(db.DateTime, default = datetime.datetime.utcnow)
  
    # one-to-many relationship 
    user = db.relationship('User', back_populates = 'inputs')

    # many-to-many relationship 

    # build-in functions
    def __init__(self, chat_id, service_type, input_timestamp): 
        self.chat_id = chat_id
        self.service_type = service_type
        self.input_timestamp = input_timestamp

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id, 
            'service_type': self.service_type,
            'input_timestamp': self.input_timestamp,
            'receive_timestamp': self.receive_timestamp
        }

class Machine(db.Model):
    __tablename__ = 'machine'

    machine_id = db.Column(db.String, primary_key = True, autoincrement=False)
    machine_type = db.Column(db.String, unique = False, nullable = False)
    duration = db.Column(db.Integer, unique = False)

    # one-to-many relationship 
    sensors = db.relationship('Sensor', back_populates = 'machine', cascade = 'all', lazy = True, uselist = True)
    usages = db.relationship('Usage', back_populates = 'machine', cascade = 'all', lazy = True, uselist = True)
    # many-to-many relationship 

    # build-in functions
    def __init__(self, machine_id, machine_type, duration, sensors = None, usages = None): 
        self.machine_id = machine_id
        self.machine_type = machine_type
        self.duration = duration
        sensors = [] if sensors is None else sensors
        self.sensors = sensors
        usages = [] if usages is None else usages
        self.usages = usages
    
    def serialize(self):
        return {
            'machine_id': self.machine_id, 
            'machine_type': self.machine_type,
            'duration': self.duration,
            'sensors': [s.serialize() for s in self.sensors],
            'usage': [u.serialize() for u in self.usages]
        }

    def get_machine_id(self):
        return self.machine_id
        
class Usage(db.Model):
    __tablename__ = 'usage'

    id = db.Column(db.Integer, primary_key = True, nullable = False) # how to make it auto increase?
    machine_id = db.Column(db.String, db.ForeignKey('machine.machine_id'), nullable = False)
    start_timestamp = db.Column(db.DateTime, unique = False, nullable = False)
    end_time = db.Column(db.DateTime, unique = False, nullable = False)

    # one-to-many relationship 
    machine = db.relationship('Machine', back_populates = 'usages')
    prompt_req = db.relationship('Prompt', back_populates = 'usage')

    # many-to-many relationship 

    # build-in functions
    def __init__(self, machine_id, start_timestamp, end_time): 
        self.machine_id = machine_id
        self.start_timestamp = start_timestamp
        self.end_time = end_time

    def serialize(self):
        return {
            'id': self.id,
            'machine_id': self.machine_id, 
            'start_timestamp': self.start_timestamp,
            'end_time': self.end_time
        }
    
    def srl_without_id(self):
        return {
            'start_timestamp': self.start_timestamp,
            'end_time': self.end_time
        }

class Prompt(db.Model):
    __tablename__ = 'prompt'

    chat_id = db.Column(db.String, db.ForeignKey('user.chat_id'))
    usage_id = db.Column(db.Integer, db.ForeignKey('usage.id'), unique = True, primary_key = True, autoincrement=False)
    machine_id = db.Column(db.String, unique = False, nullable = False)
    start_timestamp = db.Column(db.DateTime, unique = False, nullable = False)
    time_to_prompt = db.Column(db.DateTime, unique = False, nullable = True)
    ending_time = db.Column(db.DateTime, unique = False, nullable = False)
    
    # one-to-many relationship 
    usage = db.relationship('Usage', back_populates = 'prompt_req')
    user = db.relationship('User', back_populates = 'prompt_reqs')

    # many-to-many relationship 

    # build-in functions
    def __init__(self, chat_id, usage_id, machine_id, start_timestamp, time_to_prompt, ending_time): 
        self.chat_id = chat_id
        self.usage_id = usage_id
        self.machine_id = machine_id
        self.start_timestamp = start_timestamp
        self.time_to_prompt = time_to_prompt
        self.ending_time = ending_time

    def serialize(self):
        return {
            'chat_id': self.chat_id,
            'usage_id': self.usage_id,
            'machine_id': self.machine_id, 
            'start_timestamp': self.start_timestamp,
            'time_to_prompt': self.time_to_prompt,
            'ending_time': self.ending_time
        }

class Sensor(db.Model):
    __tablename__ = 'sensor'

    sensor_id = db.Column(db.String, primary_key = True, autoincrement=False)
    machine_id = db.Column(db.String, db.ForeignKey('machine.machine_id'), nullable = False)
    sensor_type = db.Column(db.String, unique = False, nullable = False)
    deployment_date = db.Column(db.DateTime, unique = False, nullable = False)

    # one-to-many relationship 
    v_sensor_readings = db.relationship('Vib_sensor_data', back_populates = 'sensor', cascade = 'all', lazy = True, uselist = True)
    m_sensor_readings = db.relationship('Mot_sensor_data', back_populates = 'sensor', cascade = 'all', lazy = True, uselist = True)
    
    machine = db.relationship('Machine', back_populates = 'sensors')
    # many-to-many relationship 

    # build-in functions
    def __init__(self, sensor_id, machine_id, sensor_type, deployment_date, v_sensor_readings = None, m_sensor_readings = None):
        self.sensor_id = sensor_id
        self.machine_id = machine_id
        self.sensor_type = sensor_type
        self.deployment_date = deployment_date
        v_sensor_readings = [] if v_sensor_readings is None else v_sensor_readings
        self.v_sensor_readings = v_sensor_readings
        m_sensor_readings = [] if m_sensor_readings is None else m_sensor_readings
        self.m_sensor_readings = m_sensor_readings
    
    def serialize(self):
        if self.sensor_type == 'vibration_sensor':
            sensor_readings = self.v_sensor_readings
        else :
            sensor_readings = []
        if self.sensor_type == 'motion_sensor':
            sensor_readings = self.m_sensor_readings
        else :
            sensor_readings = []
        return {
            'sensor_id': self.sensor_id, 
            'sensor_type': self.sensor_type,
            'deployment_date': self.deployment_date,
            'sensor_readings': [s.serialize() for s in sensor_readings]
        }

class Vib_sensor_data(db.Model):
    __tablename__ = 'vibration_sensor_data'

    id = db.Column(db.Integer, primary_key = True)
    sensor_id = db.Column(db.String, db.ForeignKey('sensor.sensor_id'), nullable = False)
    timestamp = db.Column(db.String, unique = False, nullable = False)
    sensor_figure = db.Column(db.Integer, unique = False, nullable = False)
    status_conclusion = db.Column(db.Boolean, unique = False, nullable = False)

    # one-to-many relationship 
    sensor = db.relationship('Sensor', back_populates = 'v_sensor_readings')

    # many-to-many relationship 

    # build-in functions
    def __init__(self, sensor_id, timestamp, sensor_figure, status_conclusion):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.sensor_figure = sensor_figure
        self.status_conclusion = status_conclusion

    def serialize(self):
        return{
            'id': self.id,
            'sensor_id': self.sensor_id, 
            'timestamp': self.timestamp,
            'sensor_figure': self.sensor_figure,
            'status_conclusion': self.status_conclusion
        }

class Mot_sensor_data(db.Model):
    __tablename__ = 'motion_sensor_data'

    id = db.Column(db.Integer, primary_key = True)
    sensor_id = db.Column(db.String, db.ForeignKey('sensor.sensor_id'), nullable = False)
    timestamp = db.Column(db.String, unique = False, nullable = False)
    sensor_figure = db.Column(db.Integer, unique = False, nullable = False)
    status_conclusion = db.Column(db.Boolean, unique = False, nullable = False)

    # one-to-many relationship 
    sensor = db.relationship('Sensor', back_populates = 'm_sensor_readings')

    # many-to-many relationship 

    # build-in functions
    def __init__(self, sensor_id, timestamp, sensor_figure, status_conclusion):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.sensor_figure = sensor_figure
        self.status_conclusion = status_conclusion

    def serialize(self):
        return{
            'id': self.id,
            'sensor_id': self.id, 
            'timestamp': self.timestamp,
            'sensor_figure': self.sensor_figure,
            'status_conclusion': self.status_conclusion
        }