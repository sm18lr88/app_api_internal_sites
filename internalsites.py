from flask import Flask, request, Response, render_template, jsonify
import requests
import json

app = Flask(__name__)

# Store IPs and Ports
ip_dict = {}

@app.route('/')
def index():
    return render_template('index.html', ip_dict=ip_dict)

@app.route('/add_ip', methods=['POST'])
def add_ip():
    data = request.json
    ip_dict[data['nickname']] = {"ip": data['ip'], "port": data['port']}
    return jsonify({"status": "success"}), 200

@app.route('/remove_ip/<nickname>', methods=['DELETE'])
def remove_ip(nickname):
    del ip_dict[nickname]
    return jsonify({"status": "deleted"}), 200

@app.route('/proxy/<nickname>', methods=['GET'])
def proxy(nickname):
    if nickname not in ip_dict:
        return jsonify({"error": "Not found"}), 404

    ip = ip_dict[nickname]['ip']
    port = ip_dict[nickname]['port']
    url = f'http://{ip}:{port}'
    resp = requests.get(url)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    app.run(debug=True)
