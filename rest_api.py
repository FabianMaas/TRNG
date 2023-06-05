from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from laser_sensor import LaserSensor
from stepper_engine import StepperEngine
from test_suite import TestSuite
from gyroscope import Gyroscope
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
__gyroscope = Gyroscope()

__laser_process = multiprocessing.Process(target=__laser.start)
__db_write_process = multiprocessing.Process(target=__laser.write_to_db, args=(rest_api,))
__engine_process = multiprocessing.Process(target=__engine.start)


@rest_api.route('/')
def index():
    """
    Redirects to the TRNG (True Random Number Generator) page.

    This endpoint '/' performs a redirect to the TRNG page, which provides access to a True Random Number Generator.\n
    The endpoint returns an HTTP response with a status code of 301  and a description indicating the redirection.

    Returns:
        flask.wrappers.Response: An HTTP response representing the redirect to the TRNG page.
    """
    response = make_response(redirect(url_for('trng')))
    response.status_code = 301
    response.description = 'redirecting to trng page'
    return response


@rest_api.route('/trng')
def trng():
    """
    Renders the TRNG (True Random Number Generator) page.

    This endpoint '/trng' renders the TRNG page, which provides access to a True Random Number Generator.
    The page typically contains user interface elements to request and display random numbers.

    Returns:
        flask.wrappers.Response: An HTTP response representing the rendered TRNG page.
    """
    return render_template('index.html')


@rest_api.route('/randomNum/getRandom', methods=['GET'])
def get_random_hex():
    """
    Retrieves random bits from the SQLite database and converts them to HEX encoding.

    This endpoint '/randomNum/getRandom' retrieves random bits from the SQLite database and converts them to HEX encoding.\n
    The quantity and number of bits per array can be specified as query parameters.

    Returns:
        flask.wrappers.Response: An HTTP response containing the HEX-encoded bit arrays.

    Raises:
        HTTPException: If the system is not ready and needs initialization (status code 432).
    """
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
        if(not remainder == 0):
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
    """
    Initializes the true random number generator system.

    This endpoint '/randomNum/init' initializes the true random number generator system by starting the necessary processes and components.\n
    The system requires multiple global variables (__laser_process, __db_write_process, and __engine_process) to be set properly.

    Returns:
        flask.wrappers.Response: An HTTP response indicating the initialization status.

    Raises:
        HTTPException: If the system fails to initialize within a timeout of 60 seconds (status code 555).
    """    
    global __laser_process
    global __db_write_process
    global __engine_process
    
    # angle_map = __gyroscope.get_angles()
    # if angle_map["x_angle"] > 95 or angle_map["x_angle"] < 85 or angle_map["y_angle"] > 95 or angle_map["y_angle"] < 85:
    #     return 'Could not initalize system, system must be properly aligned before. X_Angle='+ str(angle_map["x_angle"]) + 'Y_Angle' + str(angle_map["y_angle"]) + '.'
        
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
    """
    Shuts down the true random number generator system.

    This endpoint '/randomNum/shutdown' shuts down the random number generator system by stopping the necessary processes and resetting components.\n
    The system relies on global variables (__laser_process, __db_write_process, and __engine_process) to perform the shutdown.

    Returns:
        flask.wrappers.Response: An HTTP response indicating the successful shutdown.

    Notes:
        The random number generator will be set to 'standby mode' after the shutdown.

    """
    __laser.setStopFlag()
    __engine.reset()

    __laser_process.terminate()
    __db_write_process.terminate()
    __engine_process.terminate()

    time.sleep(0.5)

    response = make_response(
        'successful operation; random number generator has been set to \'standby mode\'',
        200,
    )
    return response


@rest_api.route('/getCount', methods=['GET'])
def get_safed_number_count():
    """
    Retrieves the count of stored random bits.

    This endpoint '/getCount' retrieves the count of stored random bits from the database.\n
    It calculates the total number of bits by multiplying the count of database rows with 8, because the DB stores 8 bit per row.

    Returns:
        flask.wrappers.Response: An HTTP response containing the count of stored random numbers in bits.
    """
    with rest_api.app_context():
        rows = db.session.query(Randbyte).count()
        bitCount = rows * 8
    response = make_response(jsonify(bitCount), 200)
    return response


def __bin_to_hex(bin_array):
    """
    Converts a list of binary strings to a list of HEX-encoded strings.

    This function takes a list of binary strings and converts each string to a corresponding HEX-encoded string.\n
    The binary strings are padded with leading zeros to ensure each binary string has a length divisible by 4 before conversion.\n
    The resulting HEX-encoded strings are returned in a list.

    Args:
        bin_array (list): A list of binary strings.

    Returns:
        list: A list of HEX-encoded strings.

    """    
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
    rest_api.run(host='0.0.0.0', port=8080, threaded=True)