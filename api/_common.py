import json
from email.parser import BytesParser
from email.policy import default
from urllib.parse import parse_qs
import pandas as pd


def send_json(handler, status, payload):
    body = json.dumps(payload).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def parse_upload(handler):
    content_type = handler.headers.get('Content-Type', '')
    if 'multipart/form-data' not in content_type:
        raise ValueError('Upload a CSV file using multipart/form-data.')
    raw = b'Content-Type: ' + content_type.encode() + b'\r\nMIME-Version: 1.0\r\n\r\n' + handler.rfile.read(int(handler.headers.get('Content-Length', '0')))
    message = BytesParser(policy=default).parsebytes(raw)
    for part in message.iter_parts():
        if part.get_content_disposition() == 'form-data' and part.get_param('name', header='content-disposition') == 'file':
            filename = part.get_filename() or 'data.csv'
            if not filename.lower().endswith('.csv'):
                raise ValueError('Please upload a .csv file.')
            content = part.get_payload(decode=True)
            import io
            return pd.read_csv(io.BytesIO(content))
    raise ValueError('No CSV file found in the upload.')


def query_params(handler):
    return {key: values[-1] for key, values in parse_qs(handler.path.partition('?')[2]).items() if values}
