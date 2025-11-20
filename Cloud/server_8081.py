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
from typing import Union

# Configuration constants
FRONTEND_FILE = 'rest_client.html'
BACKEND_URL = 'http://10.32.221.188:8082/mission'
SERVER_PORT = 8081

app = Flask(__name__)

@app.route('/')
def serve_html() -> Union[str, Response]:
    """Serve the frontend HTML file with CORS headers.
    
    :return: HTML content or error response
    :rtype: Union[str, Response]
    :raises IOError: If the HTML file cannot be read
    """
    try:
        with open(FRONTEND_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        return Response(
            f"Frontend file not found: {str(e)}",
            status=500,
            mimetype='text/plain'
        )

@app.route('/mission', methods=['OPTIONS'])
def handle_options() -> Response:
    """Handle CORS preflight requests.
    
    :return: Empty response with CORS headers
    :rtype: Response
    """
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route('/mission', methods=['POST'])
def proxy_mission() -> Response:
    """Proxy mission requests to backend API with CORS support.
    
    :return: Proxied response from backend with CORS headers
    :rtype: Response
    
    .. note::
        Preserves all headers and status codes from the backend service
        while adding required CORS access headers
    """
    try:
        # Forward request to backend API
        backend_resp = requests.post(
            BACKEND_URL,
            headers={'Content-Type': 'application/json'},
            data=request.get_data(),
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return Response(
            f"Backend connection failed: {str(e)}",
            status=502,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    # Create proxy response with CORS headers
    return Response(
        backend_resp.content,
        status=backend_resp.status_code,
        headers={
            'Content-Type': backend_resp.headers.get('Content-Type', 'application/json'),
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    """Run the development server on configured port."""
    app.run(port=SERVER_PORT)