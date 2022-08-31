from datetime import datetime
from pymongo import MongoClient
import os

# SET UP DB AND CLIENT FOR MONGO SERVICE


class MongoDBService():

    def __init__(self):
        super().__init__()

        self._CLIENT = MongoClient(os.environ.get("MONGODB_URI"))
        self._DB = self._CLIENT[os.environ.get("CONCERT_NAME")]
        self._USERS = self._DB["USERS"]
        self._TRANSACTIONS = self._DB["TRANSACTIONS"]

# MANAGES USERS COLLECTION


class UsersService(MongoDBService):

    def __init__(self):
        super().__init__()

    def _getKey(self, venmo_id: str):
        return {"venmo_id": venmo_id}

    # ADD A NEW USER TO THE COLLECTION
    def addNewUser(self, name: str, email: str, venmo_id: str):
        document = {
            "name": name,
            "email": email,
            "venmo_id": venmo_id,
            "tickets_bought": 0
        }
        self._USERS.update_one(self._getKey(venmo_id), {
            "$set": document
        }, upsert=True)

    # ADD TO USER'S TOTAL TICKETS BOUGHT
    def addTicketsBought(self, venmo_id: str, num_tickets: int):
        self._USERS.find_one_and_update(self._getKey(venmo_id), {
            "$inc": {"num_tickets", num_tickets}
        })

    # FIND USER BY VENMO ID
    def findUserByVenmoId(self, venmo_id: str):
        return self._USERS.find_one(self._getKey(venmo_id))

# MANAGES TRANSACTIONS COLLECTION


class TransactionsService(MongoDBService):

    def __init__(self):
        super().__init__()

    def _getKey(self, transaction_id: str):
        return {"_id": transaction_id}

    # ADD A NEW TRANSACTION TO THE COLLECTION
    def addNewTransaction(self, transaction_id: str, venmo_id: str, num_tickets: int):
        document = {
            "venmo_id": venmo_id,
            "num_tickets": num_tickets,
            "transaction_id": transaction_id,
            "fulfilled": False,
            "date": datetime.utcnow()
        }
        self._TRANSACTIONS.insert_one(document)

    # GET ALL UNPAID TRANSACTIONS
    def getUnpaidTransactions(self):
        return self._TRANSACTIONS.find({"paid": False})

    # CHANGE PAID STATUS OF A TRANSACTION TO TRUE
    def fulfillTransaction(self, transaction_id: str):
        self._TRANSACTIONS.find_one_and_update(self._getKey(transaction_id), {
            "$set": {"paid": True}
        })
