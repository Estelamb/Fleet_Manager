"""
REST API Proxy Server Module

.. module:: rest_proxy
    :synopsis: Provides a proxy server for handling CORS and forwarding requests to OpenAPI backend

.. note::
    Features:
    - Serves static HTML frontend
    - Handles CORS preflight requests
    - Proxies API requests to backend service
    - Adds necessary CORS headers to responses
"""
from flask import Flask, request, Response
import requests

FRONTEND_FILE = 'rest_client.html'
BACKEND_URL = 'http://192.168.0.42:8082/mission'
SERVER_PORT = 8090

app = Flask(__name__)

@app.route('/')
def serve_html():
    with open(FRONTEND_FILE, 'r', encoding='utf-8') as f:
        return f.read()

# CORS preflight
@app.route('/mission', methods=['OPTIONS'])
def handle_options():
    resp = Response()
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

# Proxy POST
@app.route('/mission', methods=['POST'])
def proxy_mission():
    try:
        backend_resp = requests.post(
            BACKEND_URL,
            headers={'Content-Type': request.headers.get('Content-Type', 'application/json')},
            data=request.get_data(),
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return Response(
            f"Backend connection failed: {str(e)}",
            status=502,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    resp = Response(
        backend_resp.content,
        status=backend_resp.status_code,
        mimetype=backend_resp.headers.get('Content-Type', 'application/json')
    )
    # Añadir CORS headers en la respuesta POST
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVER_PORT)
