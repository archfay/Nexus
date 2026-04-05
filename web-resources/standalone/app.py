#!/usr/bin/env python3
"""
Standalone Nexus Website Server
Работает независимо от юзербота
"""

from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'pages'), filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'mode': 'standalone',
        'message': 'Standalone версия. Для полной функциональности запустите Nexus userbot.'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
