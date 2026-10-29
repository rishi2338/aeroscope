from http.server import BaseHTTPRequestHandler
from api._common import send_json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        send_json(self, 200, {'status': 'ok', 'service': 'AeroScope ML'})
    def do_OPTIONS(self):
        send_json(self, 200, {'status': 'ok'})