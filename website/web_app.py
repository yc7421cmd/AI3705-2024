from flask import Flask, render_template, request,jsonify
import os
import sys
import json
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from mycode import process
app = Flask(__name__, template_folder='./templates',static_folder='./static')

def process_line(line):
    pass
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
@app.route('/update', methods=['GET'])
def update():
    if request.method == 'GET':
        sentence = request.args
        # print(list(sentence.keys())[0])
        color = list(sentence.keys())[0]
        process(color)
        # read log file as lines
        with open("log.txt", "r") as f:
            lines = f.readlines()
        # 去掉每行的换行符
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        with open("state.json", "r") as f:
            state = json.load(f)
        lines=json.dumps(lines)
        state=json.dumps(state)
        return jsonify({'lines':lines,'state':state})

if __name__ == '__main__':
    app.run(debug=True)