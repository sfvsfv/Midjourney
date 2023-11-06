from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import requests
import json
import time

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret!'

API_URL = "https://api.aigcbest.top/mj"
SECRET_KEY = "sk-wWi2UGe20JEuukZGC955863dFaDf47FfA0802559734c4432"

HEADERS = {
    "Authorization": SECRET_KEY,
    "Content-Type": "application/json"
}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('submit_prompt')
def handle_submit_prompt(json_data):
    prompt = json_data['prompt']
    response = requests.post(
        f"{API_URL}/submit/imagine",
        headers=HEADERS,
        data=json.dumps({
            "base64Array": [],
            "notifyHook": "",
            "prompt": prompt,
            "state": ""
        })
    )
    if response.status_code == 200:
        task_id = response.json().get('result')
        print('任务id：')
        print(task_id)
        polling_task_status(task_id)


def polling_task_status(task_id):
    while True:
        try:
            response = requests.get(f"{API_URL}/task/{task_id}/fetch", headers=HEADERS)
            if response.status_code == 200:
                task_details = response.json()
                progress = task_details.get('progress', '0%')
                image_url = task_details.get('imageUrl')
                socketio.emit('task_status', {'progress': progress, 'imageUrl': image_url})
                if progress == '100%':
                    break
            else:
                # Handle non-200 responses
                print(f"Error fetching task status: {response.status_code}")
                socketio.emit('task_status', {'progress': 'Error', 'imageUrl': None})
                break
        except requests.RequestException as e:
            # Handle request exception
            print(f"Request failed: {e}")
            socketio.emit('task_status', {'progress': 'Error', 'imageUrl': None})
            break
        time.sleep(1)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
