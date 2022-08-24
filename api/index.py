from cgi import parse_header
from http.server import BaseHTTPRequestHandler
import json
from api.services.mongodb import test

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        rawData = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
        data_dict = json.loads(rawData)

        # NAME, VENMOID, EMAIL, NUM_TICKETS, PAID
        print(data_dict)
        return

    def do_GET(self):
        test()
        # self.send_response(200)
        # self.send_header('Content-type', 'text/plain')
        # self.end_headers()
        # self.wfile.write(b"SERVERLESS FUNCTIONS UP AND RUNNING")
        return
