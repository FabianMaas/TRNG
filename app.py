from threading import Thread
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from lasersensor import Lasersensor
from testsuite import Testsuite
import time
import random


app = Flask(__name__)
laser = Lasersensor()


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

    random_bits = []
    for i in range(quantity):
        loop_thread = Thread(target=laser.consumer(num_bits))
        loop_thread.start()
        while (not laser.getFinished()):
            time.sleep(1)

        tmp = laser.getCurrentRandomArr()
        result = "".join(str(x) for x in tmp)
        random_bits.append(result)
        print(random_bits)
        laser.setNotFinished()
    
    hex_array = binaryToHex(random_bits)

    data = {
        'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
        'randomBits': hex_array
    }

    response = make_response(jsonify(data), 200)
    return response


@app.route('/randomNum/init', methods=['GET'])
def start_laser():
    laser.setStartFlag()
    producer_thread = Thread(target=laser.producer)
    producer_thread.start()

    if not laser.getIsActive():
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
    with laser.q.mutex:
        laser.q.queue.clear()
        laser.q.all_tasks_done.notify_all()
        laser.q.unfinished_tasks = 0
    #print("queue size =", laser.q.qsize)

    response = make_response(
        'successful operation; random number generator has been set to \'standby mode\'',
        200,
    )
    return response


def binaryToHex(binaryArray):
    hexArray = [hex(int(binary, 2))[2:] for binary in binaryArray]
    print(hexArray)
    return hexArray


if __name__ == '__main__':
    #cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
    #key_file = os.path.join(os.path.dirname(__file__), 'key.pem')
    #app.run(host='localhost', port=443, ssl_context=(cert_file, key_file))
    app.run(host='localhost', port=8080)