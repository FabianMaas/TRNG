import multiprocessing
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from lasersensor import Lasersensor
from testsuite import Testsuite
from models import db, Randbyte
import time
import math


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TRNG.db'
db.init_app(app)
laser = Lasersensor()
laser_process = multiprocessing.Process(target=laser.producer)
db_write_process = multiprocessing.Process(target=laser.write_to_db, args=(app,))


@app.route('/')
def index():
    response = make_response(redirect(url_for('trng')))
    response.status_code = 301
    response.description = 'redirecting to trng page'
    return response


@app.route('/trng')
def trng():
    return render_template('index.html')


@app.route('/randomNum/getRandom', methods=['GET'])
def get_random_bits():
    if not laser.getIsActive():
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
    hex_arr = bin_to_hex(split_arr)
    print(hex_arr)
    data = {
        'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
        'randomBits': hex_arr
    }

    response = make_response(jsonify(data), 200)
    return response


@app.route('/randomNum/init', methods=['GET'])
def start():
    
    global laser_process
    global db_write_process
    
    if laser_process.is_alive():
        return "system already initialized"
    laser.setStartFlag()

    if not laser_process.is_alive():
        laser_process = multiprocessing.Process(target=laser.producer)
        laser_process.start()
    if not db_write_process.is_alive():
        db_write_process = multiprocessing.Process(target=laser.write_to_db, args=(app,))
        db_write_process.start()

    if not laser_process.is_alive() or db_write_process.is_alive():
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


@app.route('/randomNum/shutdown', methods=['GET'])
def stop_laser():
    laser.setStopFlag()

    laser_process.terminate()
    db_write_process.terminate()

    time.sleep(0.5)

    response = make_response(
        'successful operation; random number generator has been set to \'standby mode\'',
        200,
    )
    return response


def bin_to_hex(binaryArray):
    hexArray = [hex(int(binary, 2))[2:] for binary in binaryArray]
    return hexArray


if __name__ == '__main__':
    #cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
    #key_file = os.path.join(os.path.dirname(__file__), 'key.pem')
    #app.run(host='localhost', port=443, ssl_context=(cert_file, key_file))

    # Datenbank-Tabellen erstellen
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, threaded=False)