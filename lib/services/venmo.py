import os

import lib.services.utils as utils
from lib.services.mongodb import TransactionsService
from lib.venmo_api import Client, PaymentStatus


class VenmoService:

    def __init__(self):
        super().__init__()

        self._CLIENT = Client(
            access_token=os.environ.get("VENMO_ACCESS_TOKEN"))

        self._ACTOR = self._CLIENT.user.get_user(
            user_id=os.environ.get("VENMO_USERNAME"))

    # REQUEST PAYMENT TO USER WITH USER_ID
    def requestPayment(self, num_tickets: int, name: str, target_venmo_id: str):
        TARGET = self._CLIENT.user.get_user(
            user_id=utils.format_username(target_venmo_id))

        REQUEST_MESSAGE = f"GT OSCAR BAND - {os.environ.get('CONCERT_NAME')} \n{num_tickets} Tickets For: {name}\n\nPlease wait upto 5 minutes to receive a payment confirmation through email."

        transaction_id = self._CLIENT.payment.request_money(
            target_user=TARGET,
            note=REQUEST_MESSAGE,
            amount=utils.compute_price(num_tickets)
        )

        TransactionsService().addNewTransaction(
            transaction_id=transaction_id,
            venmo_id=target_venmo_id,
            num_tickets=num_tickets
        )

    # GET ALL SETTLED TRANSACTIONS, WITH A LIMIT OF 10
    def getSettledTransactionIds(self):
        p_list = self._CLIENT.payment.get_charge_payments(limit=10)
        return [p.id for p in p_list if p.status is PaymentStatus.SETTLED]
