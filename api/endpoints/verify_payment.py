

from http.server import BaseHTTPRequestHandler
from lib.services.email import EmailService

from lib.services.mongodb import TransactionsService, UsersService
from lib.services.venmo import VenmoService


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self._verify_payment()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"VERIFIED PAYMENT")
        except Exception as e:
            print(e)
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"ERROR VERIFYING PAYMENT")


    def _verify_payment(self):

        transactionsService = TransactionsService()
        venmoService = VenmoService()
        usersService = UsersService()

        unpaid_transactions = transactionsService.getUnpaidTransactions()
        unpaid_count = unpaid_transactions.explain().get("executionStats", {}).get("nReturned")
        # CHECK VENMO TRANSACTIONS IFF THERE ARE PENDING TICKET PURCHASES
        if unpaid_count > 0:
            # GET SETTLED VENMO TRANSACTIONS
            settled_transaction_ids = venmoService.getSettledTransactionIds()
            for u_t in unpaid_transactions:
                # IF A TRANSACTION HAS BEEN NEWLY SETTLED
                if (transaction_id := u_t["transaction_id"]) in settled_transaction_ids:

                    venmo_id = u_t["venmo_id"]
                    num_tickets = u_t["num_tickets"]

                    # UPDATE PAID STATUS IN TRANSACTIONS COLLECTION
                    transactionsService.fulfillTransaction(
                        transaction_id=transaction_id)

                    # UPDATE NUM TICKETS BOUGHT IN USERS COLLECTION
                    usersService.addTicketsBought(
                        venmo_id=venmo_id, num_tickets=num_tickets)

                    user = usersService.findUserByVenmoId(venmo_id=venmo_id)

                    # SEND CONFIRMATION EMAIL TO NEW CUSTOMER
                    EmailService(user=user, num_tickets=num_tickets).sendEmail()