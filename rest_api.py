from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from laser_sensor import LaserSensor
from stepper_engine import StepperEngine
from test_suite import TestSuite
from models import db, Randbyte
import multiprocessing
from multiprocessing import Event
import time
import math


rest_api = Flask(__name__)
rest_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TRNG.db'
db.init_app(rest_api)
__laser = LaserSensor()
__engine = StepperEngine()

__laser_process = multiprocessing.Process(target=__laser.start)
__db_write_process = multiprocessing.Process(target=__laser.write_to_db, args=(rest_api,))
__engine_process = multiprocessing.Process(target=__engine.start)


@rest_api.route('/')
def index():
    response = make_response(redirect(url_for('trng')))
    response.status_code = 301
    response.description = 'redirecting to trng page'
    return response


@rest_api.route('/trng')
def trng():
    return render_template('index.html')


@rest_api.route('/randomNum/getRandom', methods=['GET'])
def get_random_hex():
    if not __laser_process.is_alive:
        response = make_response('system not ready; try init', 432)
        return response
    
    quantity = request.args.get('quantity',default=1, type=int)
    num_bits = request.args.get('numBits', default=1, type=int)

    number_rows = math.ceil((quantity*num_bits)/8)

    while db.session.query(Randbyte).count() < number_rows:
        time.sleep(1)

    rows_arr = []

    oldest_rows = Randbyte.query.order_by(Randbyte.id).limit(number_rows).all()
    
    for row in oldest_rows:
        rows_arr.append(row.value)
        db.session.delete(row)

    db.session.commit()
    
    remainder = num_bits % 4
    joined_string = ''.join(rows_arr)
    print("numbits=",num_bits)
    split_arr = []
    for i in range(0, quantity * num_bits, num_bits):
        substring = joined_string[i : i + num_bits]
        for i in range(4-remainder):
            substring = "0" + substring
        split_arr.append(substring)
    
    print(split_arr)
    hex_arr = __bin_to_hex(split_arr)
    print(hex_arr)
    data = {
        'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
        'randomBits': hex_arr
    }

    response = make_response(jsonify(data), 200)
    return response


@rest_api.route('/randomNum/init', methods=['GET'])
def init_system():
    global __laser_process
    global __db_write_process
    global __engine_process
    
    if __laser_process.is_alive():
        return "system already initialized"
    
    __laser.setStartFlag()
    
    error_event = Event()
    if not __laser_process.is_alive():
        __laser_process = multiprocessing.Process(target=__laser.start)
        __laser_process.start()
    if not __db_write_process.is_alive():
        __db_write_process = multiprocessing.Process(target=__laser.write_to_db, args=(rest_api, error_event,))
        __db_write_process.start()      
    if not __engine_process.is_alive():
        __engine_process = multiprocessing.Process(target=__engine.start, args=(error_event,))
        __engine_process.start()   

    time.sleep(0.5)

    if not __laser_process.is_alive() or not __db_write_process.is_alive() or not __engine_process.is_alive():
        response = make_response(
            'unable to initialize the random number generator within a timeout of 60 seconds',
            555,
        )
        return response

    response = make_response(
        'successful operation; random number generator is ready and random numbers can be requested',
        200,
    )
    return response


@rest_api.route('/randomNum/shutdown', methods=['GET'])
def shutdown_system():
    __laser.setStopFlag()
    __engine.destroy()

    __laser_process.terminate()
    __db_write_process.terminate()
    __engine_process.terminate()

    time.sleep(0.5)

    response = make_response(
        'successful operation; random number generator has been set to \'standby mode\'',
        200,
    )
    return response


def __bin_to_hex(bin_array):
    hex_array = []
    for binary in bin_array:
        binary = binary.zfill((len(binary) + 3) // 4 * 4)
        hex_string = format(int(binary, 2), '0' + str(len(binary) // 4) + 'X')
        hex_array.append(hex_string)
    return hex_array
    
if __name__ == "__main__":
    #cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
    #key_file = os.path.join(os.path.dirname(__file__), 'key.pem')
    #app.run(host='localhost', port=443, ssl_context=(cert_file, key_file))

    with rest_api.app_context():
        db.create_all()
    rest_api.run(host='0.0.0.0', port=8080, threaded=False)