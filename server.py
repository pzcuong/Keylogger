import os
import datetime
import json
import csv
import base64
from flask import Flask, request, jsonify

app = Flask('app')


def make_dir(os_data):
    os_data = json.loads(os_data)
    file_name = os_data['osName'] + os_data['osInfo'][0] + os_data['appName']
    dir = os.path.join(os.getcwd(), 'logs', file_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def get_date_time(format="%Y-%m-%d %H:%M:%S:%f"):
    now = datetime.datetime.now()
    return now.strftime(format)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/init', methods=['GET', 'POST'])
def init():
    try:
        os_data = request.headers.get("os_data")

        dir = make_dir(os_data)
        os_data = json.loads(os_data)
        print(os_data["osName"], os_data["osInfo"][0], os_data["appName"])

        header_data = ['time', 'appName', 'key', 'type']

        with open(dir + "/" + get_date_time(format="%Y-%m-%d") + ".csv", "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header_data)
            writer.writerow(
                [os_data['osName'], os_data['osInfo'][0], os_data['appName']])
            writer.writerow(["Start recored at", get_date_time()])

        return ({
            'status': 'success',
            'message': 'init success',
            'data': os_data
        })
    except Exception as error:
        return error_handler(error)


@app.route('/send', methods=['POST'])
def send():
    try:
        os_data = request.headers.get("os_data")
        dir = make_dir(os_data)
        request_data = request.get_json()

        with open(dir + "/" + get_date_time(format="%Y-%m-%d") + ".csv", "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([request_data['time'], request_data['appName'],
                            request_data['key'], request_data['type']])

        print(request_data)

        return ({
            'status': 'success',
            'message': 'send success',
            'data': request_data
        })
    except Exception as error:
        return error_handler(error)


@app.route('/screenshots', methods=['POST'])
def screenshots():
    try:
        request_data = request.get_json()

        # Check that the required data is present in the request
        if 'time' not in request_data or 'appName' not in request_data or 'screenshot' not in request_data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required data in the request'
            }), 400

        # Decode the base64 encoded image
        screenshot = base64.b64decode(request_data['screenshot'])

        # Create a directory for the screenshots
        os_data = request.headers.get("os_data")
        dir = make_dir(os_data)

        file_name = f"{request_data['time']}_{request_data['appName']}_screenshot.png"

        # Write the screenshot to the file
        with open(dir + file_name, "wb") as f:
            f.write(screenshot)

        return jsonify({
            'status': 'success',
            'message': 'screenshot saved success',
        })
    except Exception as error:
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 500



def error_handler(error):
    return ({
        'status': 'error',
        'message': str(error),
    })


cwd = os.getcwd()
print(cwd)
app.run(port=5000)
