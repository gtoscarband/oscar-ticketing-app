from http.server import BaseHTTPRequestHandler
import json
from lib.services.venmo import VenmoService
import ast
from lib.venmo_api.models.exception import ResourceNotFoundError, HttpCodeError
from lib.services.mongodb import UsersService

class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        rawData = (self.rfile.read(
            int(self.headers['content-length']))).decode('utf-8')
        data_dict = json.loads(rawData)

        try:
            VenmoService().requestPayment(
                num_tickets=int(data_dict["num_tickets"]),
                name=data_dict["name"],
                target_venmo_id=data_dict["venmo_id"]
            )

            UsersService().addNewUser(
                name=data_dict["name"],
                email=data_dict["email"],
                venmo_id=data_dict["venmo_id"]
            )

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Venmo Request Successfully Sent")
            return
        except ResourceNotFoundError:
            self.handleError("Unable to find user with Venmo ID")
        except HttpCodeError as HCE:
            error_info = ast.literal_eval(HCE.msg)
            error_msg = error_info['error']['message']
            self.handleError(error_msg)
        except Exception as e:
            print(e)
            self.handleError(str(e))

    def handleError(self, message: str):
        self.send_response(400)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str.encode(message))
