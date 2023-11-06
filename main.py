from flask import Flask, render_template, jsonify, request
import requests
import json
import time

app = Flask(__name__)

# 你的API密钥
secret_key = "sk...."
# API基础URL
base_url = "https://api.aigcbest.top/mj"

# 用于存储任务状态的全局变量
tasks = {}


@app.route('/')
def index():
    # 前端页面，包含用于显示图片和进度的元素
    return render_template('index.html')

from flask import request
@app.route('/submit', methods=['POST'])
def submit_task():
    # 提交任务到API
    url = f"{base_url}/submit/imagine"
    headers = {
        "Authorization": secret_key,
        "Content-Type": "application/json"  # 确保设置为application/json
    }

    # 从前端请求中获取prompt，如果没有提供，则使用默认值
    prompt = request.json.get('prompt', 'beautiful chinese girl') if request.json else 'beautiful chinese girl'

    data = {
        "base64Array": [],
        "notifyHook": "",
        "prompt": prompt,
        "state": ""
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        task_id = result['result']
        # 在全局任务字典中保存任务信息
        tasks[task_id] = {'progress': '0%', 'imageUrl': None}
        return jsonify({'task_id': task_id})
    else:
        # 如果请求失败，返回错误信息
        return jsonify({'error': 'Unable to submit task'}), response.status_code


@app.route('/progress/<task_id>')
def get_progress(task_id):
    # 获取特定任务的进度
    task_info = tasks.get(task_id, None)
    if not task_info:
        return jsonify({'error': 'Task not found'}), 404

    url = f"{base_url}/task/{task_id}/fetch"
    headers = {"Authorization": secret_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        task_details = response.json()
        progress = task_details['progress']
        image_url = task_details['imageUrl']
        tasks[task_id] = {'progress': progress, 'imageUrl': image_url}
        return jsonify({'progress': progress, 'imageUrl': image_url})
    else:
        return jsonify({'error': 'Unable to fetch task progress'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=8080)

