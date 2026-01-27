from flask import Flask, send_from_directory, request
from datetime import datetime
import os

app = Flask(__name__, static_folder='../public')
PORT = 3000

# Request logging middleware
@app.before_request
def log_request():
    timestamp = datetime.utcnow().isoformat()
    ip = request.remote_addr
    print(f"[{timestamp}] {request.method} {request.path} - {ip}")

# Serve static files from public directory
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print(f"Frontend running at http://0.0.0.0:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
