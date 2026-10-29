from http.server import BaseHTTPRequestHandler
from api._common import parse_upload, query_params, send_json
from python_ml_engine import forecast_data

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        send_json(self, 200, {'status': 'ok'})
    def do_POST(self):
        try:
            params = query_params(self)
            target = params.get('target', 'PM2.5')
            periods = int(params.get('periods', '7'))
            df = parse_upload(self)
            send_json(self, 200, forecast_data(df, target, periods))
        except ValueError as exc:
            send_json(self, 400, {'detail': str(exc)})
        except Exception as exc:
            send_json(self, 500, {'detail': f'Could not forecast CSV: {exc}'})