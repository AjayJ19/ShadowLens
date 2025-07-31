from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🚀 Starting ShadowLens Dashboard Server on port 8080")
    print("📊 Open http://localhost:8080 to view the dashboard")
    app.run(host='0.0.0.0', port=8080, debug=False) 