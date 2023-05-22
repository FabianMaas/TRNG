from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from laser_sensor import LaserSensor
from stepper_engine import StepperEngine
from test_suite import TestSuite
from models import db, Randbyte
import multiprocessing
from multiprocessing import Event
import time
import math

class RestApi:
    rest_api = Flask(__name__)
    rest_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TRNG.db'
    db.init_app(rest_api)
    __laser = LaserSensor()
    __engine = StepperEngine()

    __laser_process = multiprocessing.Process(target=__laser.start)
    __db_write_process = multiprocessing.Process(target=__laser.write_to_db, args=(rest_api,))
    __engine_process = multiprocessing.Process(target=__engine.start)



    def start(self):
        #cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
        #key_file = os.path.join(os.path.dirname(__file__), 'key.pem')
        #app.run(host='localhost', port=443, ssl_context=(cert_file, key_file))

        with self.rest_api.app_context():
            db.create_all()
        self.rest_api.run(host='0.0.0.0', port=8080, threaded=False)


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
    def get_random_hex(self):
        if not self.__laser_process.is_alive:
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
        
        joined_string = ''.join(rows_arr)
        print("numbits=",num_bits)
        split_arr = [joined_string[i:i+num_bits] for i in range(0, (quantity*num_bits), num_bits)]
        print(split_arr)
        hex_arr = self.__bin_to_hex(split_arr)
        print(hex_arr)
        data = {
            'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
            'randomBits': hex_arr
        }

        response = make_response(jsonify(data), 200)
        return response


    @rest_api.route('/randomNum/init', methods=['GET'])
    def init_system(self):

        if self.__laser_process.is_alive():
            return "system already initialized"
        
        self.__laser.setStartFlag()
        
        error_event = Event()
        if not self.__laser_process.is_alive():
            self. __laser_process = multiprocessing.Process(target=self.__laser.start)
            self.__laser_process.start()
        if not self.__db_write_process.is_alive():
            self.__db_write_process = multiprocessing.Process(target=self.__laser.write_to_db, args=(self.rest_api, error_event,))
            self.__db_write_process.start()      
        if not self.__engine_process.is_alive():
            self.__engine_process = multiprocessing.Process(target=self.__engine.start, args=(error_event,))
            self.__engine_process.start()   

        time.sleep(0.5)
    
        if not self.__laser_process.is_alive() or not self.__db_write_process.is_alive() or not self.__engine_process.is_alive():
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
    def shutdown_system(self):
        self.__laser.setStopFlag()
        self.__engine.destroy()

        self.__laser_process.terminate()
        self.__db_write_process.terminate()
        self.__engine_process.terminate()

        time.sleep(0.5)

        response = make_response(
            'successful operation; random number generator has been set to \'standby mode\'',
            200,
        )
        return response


    def __bin_to_hex(binaryArray):
        hexArray = [hex(int(binary, 2))[2:] for binary in binaryArray]
        return hexArray
    
if __name__ == "__main__":
    RestApi.start(RestApi)