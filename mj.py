# coding=utf-8
import requests
import json
import time

# 公共变量
secret_key = "自己密钥"
headers = {
    "Authorization": secret_key,
    "Content-Type": "application/json"
}


# 下载图片并保存到本地文件
def download_image(image_url, local_file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(local_file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {local_file_name}")
    else:
        print(f"Error: Unable to download image from {image_url}")


# 提交新任务
def submit_task(prompt):
    url = "https://ai69.vip/mj/submit/imagine"
    data = {
        "base64Array": [],
        "notifyHook": "",
        "prompt": prompt,
        "state": ""
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        task_id = response.json().get('result')
        print(f"Task submitted successfully. Task ID: {task_id}")
        return task_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# 检索任务状态和结果
def fetch_task_details(task_id):
    url = f"https://ai69.vip/mj/task/{task_id}/fetch"
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            task_details = response.json()
            progress = task_details.get("progress", "")
            if progress == "100%":
                print("Task completed.")
                return task_details
            else:
                print(f"Task in progress: {progress}. Waiting...")
                time.sleep(5)  # 等待5秒后再次检查进度
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


# 提交变换任务（用户可选）
# 提交变换任务（用户可选）
def submit_change(task_id):
    actions = {"1": "UPSCALE", "2": "VARIATION", "3": "REROLL"}
    action_input = input("Enter the action (1 for UPSCALE, 2 for VARIATION, 3 for REROLL): ")
    action = actions.get(action_input, None)

    if not action:
        print("Invalid action selected.")
        return None

    index = int(input("Enter the index (1-4): "))

    url = "https://api.aigcbest.top/mj/submit/change"
    data = {
        "action": action,
        "index": index,
        "notifyHook": "",
        "state": "",
        "taskId": task_id
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        change_response = response.json()
        print(change_response)
        return change_response.get('result')
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None



# 主程序流程
def main():
    prompt = input("Please enter the prompt for the image: ")
    task_id = submit_task(prompt)
    if task_id:
        task_details = fetch_task_details(task_id)
        if task_details:
            image_url = task_details.get("imageUrl")
            if image_url:
                local_file_name = f"image_{task_id}.jpg"
                download_image(image_url, local_file_name)

            # 询问用户是否想要执行变换操作
            change = input("Do you want to change the image? (yes/no): ")
            if change.lower() == 'yes':
                new_task_id = submit_change(task_id)
                if new_task_id:
                    # 获取新任务详情并下载图片
                    new_task_details = fetch_task_details(new_task_id)
                    if new_task_details:
                        new_image_url = new_task_details.get("imageUrl")
                        if new_image_url:
                            new_local_file_name = f"changed_image_{new_task_id}.jpg"
                            download_image(new_image_url, new_local_file_name)


if __name__ == "__main__":
    main()