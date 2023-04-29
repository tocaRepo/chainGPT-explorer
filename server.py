from flask import Flask, render_template, jsonify, request,send_from_directory
from chainGPT.chainGPT import chainGPT
import openai
import os

app = Flask(__name__)
task=None
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/task/start', methods=['POST'])
def start_task():
    global task
    # Your API code here
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    chainGPTInstance = chainGPT()

    task_prompt = request.json['task_prompt']

    if task is None:
        task = chainGPTInstance.create_task(
            task_prompt,
            enhance_prompt_using_chatgpt=True,
            request_type="CHAIN"
        )
        task = chainGPTInstance.start_task(task)

    return jsonify({'status': 'started'})


@app.route('/api/task/status')
def task_status():
    global task
    return jsonify({'status': task.status})

@app.route('/api/task/status/journal')
def task_status_journal():
    global task
    return jsonify({'journal': task.status_journal})

@app.route('/drop_folder')
def serve_drop_folder():
    file_list = os.listdir("./drop_folder")
    return render_template('drop_folder.html', files=file_list)

@app.route('/drop_folder/<path:path>')
def serve_file_in_drop_folder(path):
    return send_from_directory("drop_folder", path)
if __name__ == '__main__':
    app.run()