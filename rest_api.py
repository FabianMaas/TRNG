"""
This Python file implements a True Random Number Generator (TRNG) REST API using the Flask framework. 
The TRNG system consists of a laser sensor, a stepper engine, a gyroscope, and a database for storing random bits.

Attributes:

    rest_api (Flask): The Flask application object.
    __laser (LaserSensor): Instance of the LaserSensor class for generating random bits.
    __engine (StepperEngine): Instance of the StepperEngine class for controlling the stepper motor.
    __gyroscope (Gyroscope): Instance of the Gyroscope class for retrieving orientation angles.
    __testsuite (TestSuite): Instance of the TestSuite class for performing tests on random bit sequences.
    __laser_process (multiprocessing.Process): Process object for running the laser sensor.
    __db_write_process (multiprocessing.Process): Process object for writing random bits to the database.
    __engine_process (multiprocessing.Process): Process object for controlling the stepper motor.
    __test_bit_sequence (bool): Flag indicating whether to test the generated bit sequence or not.

Endpoints:

    '/': Redirects to the TRNG page.
    '/trng': Renders the TRNG page.
    '/trng/randomNum/getRandom': Retrieves random bits from the database and converts them to HEX encoding.
    '/trng/randomNum/init': Initializes the TRNG system.
    '/trng/randomNum/shutdown': Shuts down the TRNG system.
    '/trng/getCount': Retrieves the count of stored random bits from the database.

Helper Functions:

    __wait_for_rows(number_rows): Waits until the specified number of rows is available in the database.
    __get_tested_bits(test_rows, actually_required_rows): Retrieves and tests a specified number of rows from the database, ensuring the success of the tests before returning the requested rows.
    __get_not_tested_bits(actually_required_rows): Retrieves and deletes the specified number of rows from the database, returning the corresponding values.
    __contains_only_numbers(string): Validates if a string consists of only positive integers.
    __row_arr_to_split_arr(rows_arr, quantity, num_bits): Converts a row array into a split array of fixed-length substrings.
    __bin_to_hex(bin_array): Converts a list of binary strings to a list of HEX-encoded strings.

Imports:

    math: Provides mathematical functions for calculations used in the code.
    multiprocessing: Enables the creation and management of multiple processes for parallel execution.
    os: Provides functions for interacting with the operating system, such as file path operations.
    re: Provides support for regular expressions used for string pattern matching and validation.
    time: Provides functions for time-related operations, such as delays and timestamps.
    Flask: A web framework used for creating the RESTful API endpoints and handling HTTP requests.
    jsonify: A Flask function used to convert Python objects to JSON-formatted responses.
    make_response: A Flask function used to create custom HTTP responses.
    redirect: A Flask function used to perform HTTP redirects.
    render_template: A Flask function used for rendering HTML templates.
    request: A Flask object that represents an incoming HTTP request.
    url_for: A Flask function used for generating URLs for endpoints.
    models: A module that contains the database models for the application.
    db: A database instance used for interacting with the SQLite database.
    gyroscope: A module that provides functionality for interacting with a gyroscope sensor.
    laser_sensor: A module that provides functionality for interacting with a laser sensor.
    stepper_engine: A module that provides functionality for controlling a stepper motor.
    test_suite: A module that contains test functions for evaluating the quality of random bit sequences.

Note:

    The TRNG system requires proper initialization before random numbers can be generated.
    The laser sensor, stepper motor, and gyroscope processes are run as separate multiprocessing processes.
    The random bits are stored in an SQLite database.
    The TRNG page provides user interface elements to request and display random numbers.
    The generated random bits can be retrieved in HEX-encoded format.
    The system supports testing of the generated bit sequence using various tests provided by the TestSuite class.
    The system can be shut down, and the random number generator can be set to 'standby mode' after shutdown.
"""


import math
import multiprocessing
import os
import re
import time

from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for
from models.models import Randbyte, db
from hardware.gyroscope import Gyroscope
from hardware.laser_sensor import LaserSensor
from hardware.stepper_engine import StepperEngine
from tests.test_suite import TestSuite


rest_api = Flask(__name__)
rest_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TRNG.db'
db.init_app(rest_api)
__laser = LaserSensor()
__engine = StepperEngine()
__gyroscope = Gyroscope()
__testsuite = TestSuite()

__laser_process = multiprocessing.Process(target=__laser.start)
__db_write_process = multiprocessing.Process(target=__laser.write_to_db, args=(rest_api,))
__engine_process = multiprocessing.Process(target=__engine.start)

__test_bit_sequence = False


@rest_api.route('/')
def index():
    """
    Redirects to the TRNG (True Random Number Generator) page.\n
    This endpoint '/' performs a redirect to the TRNG page, which provides access to a True Random Number Generator.\n
    The endpoint returns an HTTP response with a status code of 301  and a description indicating the redirection.\n
    Returns:
    - flask.wrappers.Response: An HTTP response representing the redirect to the TRNG page.
    """
    response = make_response(redirect(url_for('trng')))
    response.status_code = 301
    response.description = 'redirecting to trng page'
    return response


@rest_api.route('/trng')
def trng():
    """
    Renders the TRNG (True Random Number Generator) page.\n
    This endpoint '/trng' renders the TRNG page, which provides access to a True Random Number Generator.
    The page typically contains user interface elements to request and display random numbers.\n
    Returns:
    - flask.wrappers.Response: An HTTP response representing the rendered TRNG page.
    """
    return render_template('index.html')


@rest_api.route('/trng/randomNum/getRandom', methods=['GET'])
def get_random_hex():
    """
    Retrieves random bits from the SQLite database and converts them to HEX encoding.\n
    This endpoint '/trng/randomNum/getRandom' retrieves random bits from the SQLite database and converts them to HEX encoding.\n
    The quantity and number of bits per array can be specified as query parameters.\n
    Returns:
    - flask.wrappers.Response: An HTTP response containing the HEX-encoded bit arrays.\n
    Raises:
    - HTTPException: If the system is not ready and needs initialization (status code 432).
    """
    if not __laser_process.is_alive():
        response = make_response('system not ready; try init', 432)
        return response
    
    quantity = request.args.get('quantity',default=1)
    num_bits = request.args.get('numBits', default=1)

    if not __contains_only_numbers(str(quantity)) or not __contains_only_numbers(str(num_bits)):
        response = make_response('invalid query parameter', 400)
        return response

    quantity = int(quantity)
    num_bits = int(num_bits)
    
    if ((quantity < 1) or (num_bits < 1)):
        response = make_response('invalid query parameter', 400)
        return response

    test_blocks = math.ceil(((quantity*num_bits) / 256))
    test_rows = (test_blocks * 256) / 8

    actually_required_rows = math.ceil((quantity*num_bits)/8) 

    rows_arr = []

    if(__test_bit_sequence == True):
        rows_arr = __get_tested_bits(test_rows, actually_required_rows)
    else:
        rows_arr = __get_not_tested_bits(actually_required_rows)

    print("rows_arr =",rows_arr)
    
    split_arr = __row_arr_to_split_arr(rows_arr, quantity, num_bits)
    
    print("split_arr =",split_arr)
    hex_arr = __bin_to_hex(split_arr)
    print("hex_arr =",hex_arr)
    data = {
        'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
        'randomBits': hex_arr
    }

    response = make_response(jsonify(data), 200)
    return response


@rest_api.route('/trng/randomNum/init', methods=['GET'])
def init_system():
    """
    Initializes the true random number generator system.\n
    This endpoint '/trng/randomNum/init' initializes the true random number generator system by starting the necessary processes and components.\n
    The system requires multiple global variables (__laser_process, __db_write_process, and __engine_process) to be set properly.\n
    Returns:
    - flask.wrappers.Response: An HTTP response indicating the initialization status.\n
    Raises:
    - HTTPException: If the system fails to initialize within a timeout of 60 seconds (status code 555).
    """    
    global __laser_process
    global __db_write_process
    global __engine_process
    
    # angle_map = __gyroscope.get_angles()
    # if angle_map["x_angle"] > 95 or angle_map["x_angle"] < 85 or angle_map["y_angle"] > 95 or angle_map["y_angle"] < 85:
    #     return 'Could not initalize system, system must be properly aligned before. X_Angle='+ str(angle_map["x_angle"]) + 'Y_Angle' + str(angle_map["y_angle"]) + '.'
        
    if __laser_process.is_alive():
        return "system already initialized"
    
    error_event = multiprocessing.Event()
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


@rest_api.route('/trng/randomNum/shutdown', methods=['GET'])
def shutdown_system():
    """
    Shuts down the true random number generator system.\n
    This endpoint '/trng/randomNum/shutdown' shuts down the random number generator system by stopping the necessary processes and resetting components.\n
    The system relies on global variables (__laser_process, __db_write_process, and __engine_process) to perform the shutdown.\n
    Returns:
    - flask.wrappers.Response: An HTTP response indicating the successful shutdown.\n
    Notes:
        The random number generator will be set to 'standby mode' after the shutdown.
    """
    if not __laser_process.is_alive():
        response = make_response('shutdown is not possible if system is not initialized', 400)
        return response

    __laser_process.terminate()
    __db_write_process.terminate()
    __engine_process.terminate()

    time.sleep(0.5)

    response = make_response(
        'successful operation; random number generator has been set to \'standby mode\'',
        200,
    )
    return response


@rest_api.route('/trng/getCount', methods=['GET'])
def get_safed_number_count():
    """
    Retrieves the count of stored random bits.\n
    This endpoint '/trng/getCount' retrieves the count of stored random bits from the database.\n
    It calculates the total number of bits by multiplying the count of database rows with 8, because the DB stores 8 bit per row.\n
    Returns:
    - flask.wrappers.Response: An HTTP response containing the count of stored random numbers in bits.
    """
    with rest_api.app_context():
        rows = db.session.query(Randbyte).count()
        bitCount = rows * 8
    response = make_response(jsonify(bitCount), 200)
    return response


def __wait_for_rows(number_rows):
    """
    Waits until the specified number of rows is available in the database.\n
    Parameters:
    - number_rows (int): The desired number of rows to wait for.\n
    Note:
        This method uses a loop to continuously check the count of rows in the database
        until the desired number of rows is reached. It sleeps for 1 second between each check.\n
    """
    while db.session.query(Randbyte).count() < number_rows:
        time.sleep(1)


def __get_tested_bits(test_rows, actually_required_rows):
    """
    Retrieves and tests a specified number of rows from the database,
    ensuring the success of the tests before returning the requested rows.\n
    Parameters:
    - test_rows (int): The number of rows to be tested.
    - actually_required_rows (int): The number of rows required in the final result.\n
    Returns:
    - list: A list of the requested rows if the tests are successful,
              otherwise a response indicating test failure.\n
    Note:
        This method retrieves the specified number of rows from the database and
        performs a series of tests on the values. The tests are repeated up to
        five times or until the tests succeed. If the tests succeed, the method
        returns a list of the requested rows, deletes them from the database, and
        commits the changes. If the tests fail, all retrieved rows are deleted from
        the database, and a response with an appropriate status code is returned.
    """
    test_success = False
    test_count = 0
    test_arr = []
    rows_arr = []
    while ((test_success == False) and (test_count < 5)):
        test_arr.clear()
        __wait_for_rows(test_rows)
        rows = Randbyte.query.order_by(Randbyte.id).limit(test_rows).all()

        for row in rows:
            test_arr.append(row.value)
            
        test_success = __testsuite.run_all_tests(test_arr)
        test_count += 1
        

        if (test_success == True):
            counter = 0
            for row in rows:
                if(counter < actually_required_rows):
                    rows_arr.append(row.value)
                    db.session.delete(row)
                    counter += 1
                else:
                    break
            db.session.commit()

        if(test_success == False):
            for row in rows:
                db.session.delete(row)
            db.session.commit()

    if(test_success == False):

        response = make_response(
            'tests for the requested bit sequence failed',
            543,
        )
        return response 
    
    return rows_arr


def __get_not_tested_bits(actually_required_rows):
    """
    Retrieves and also deletes the specified number of rows from the database,
    and returns the corresponding values.\n
    Parameters:
    - actually_required_rows (int): The number of rows required in the final result.\n
    Returns:
    - list: A list of the values from the requested rows.\n
    Note:
        This method waits until the specified number of rows is available in the database.
        Once the required rows are available, it retrieves and also deletes them from the database,
        and commits the changes.
        Finally, it returns a list of the values from the requested rows.
    """
    rows_arr = []
    __wait_for_rows(actually_required_rows)
    rows = Randbyte.query.order_by(Randbyte.id).limit(actually_required_rows).all()
    for row in rows:
        rows_arr.append(row.value)
        db.session.delete(row)
    db.session.commit()
    return rows_arr


def __contains_only_numbers(string):
    """
    Validates if a string consists of only positive integers.\n
    Parameters:
    - string (str): The string to be validated.\n
    Returns:
    - bool: True if the string consists of only positive integers, False otherwise.
    """
    pattern = r'^[1-9][0-9]*$'
    print(string)
    if re.match(pattern, string):
        print("True")
        return True
    else:
        print("False")
        return False


def __row_arr_to_split_arr(rows_arr, quantity, num_bits):
    """
    Converts a row array into a split array of fixed-length substrings.\n
    Parameters:
    - rows_arr (list): A list of strings representing rows each containing 8 bit.\n
    - quantity (int): The number of substrings to split the row array into.\n
    - num_bits (int): The desired length of each substring.\n
    Returns:
    - list: A list of fixed-length substrings created from the row array.\n
    Example:
        rows_arr = ['11001100', '10101010', '00110011', '10100110']\n
        quantity = 2\n
        num_bits = 16\n
        __row_arr_to_split_arr(rows_arr, quantity, num_bits)\n
        Output: ['1100110010101010', '0011001110100110']
    """
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
    return split_arr


def __bin_to_hex(bin_array):
    """
    Converts a list of binary strings to a list of HEX-encoded strings.\n
    This function takes a list of binary strings and converts each string to a corresponding HEX-encoded string.\n
    The binary strings are padded with leading zeros to ensure each binary string has a length divisible by 4 before conversion.\n
    The resulting HEX-encoded strings are returned in a list.\n
    Parameters:
    - bin_array (list): A list of binary strings.\n
    Returns:
    - list: A list of HEX-encoded strings.
    """    
    hex_array = []
    for binary in bin_array:
        binary = binary.zfill((len(binary) + 3) // 4 * 4)
        hex_string = format(int(binary, 2), '0' + str(len(binary) // 4) + 'X')
        hex_array.append(hex_string)
    return hex_array
    

if __name__ == "__main__":
    cert_file = os.path.join(os.path.dirname(__file__), '/home/Wave/certs/cert-wave.pem')
    key_file = os.path.join(os.path.dirname(__file__), '/home/Wave/certs/cert-wave-key.pem')

    with rest_api.app_context():
        db.create_all()
    rest_api.run(host='0.0.0.0', threaded=True, port=443, ssl_context=(cert_file, key_file))