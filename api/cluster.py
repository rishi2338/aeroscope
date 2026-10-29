from http.server import BaseHTTPRequestHandler
from api._common import parse_upload, query_params, send_json
from python_ml_engine import cluster_data

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        send_json(self, 200, {'status': 'ok'})
    def do_POST(self):
        try:
            params = query_params(self)
            clusters = int(params.get('clusters', '3'))
            df = parse_upload(self)
            send_json(self, 200, cluster_data(df, clusters))
        except ValueError as exc:
            send_json(self, 400, {'detail': str(exc)})
        except Exception as exc:
            send_json(self, 500, {'detail': f'Could not analyze CSV: {exc}'})