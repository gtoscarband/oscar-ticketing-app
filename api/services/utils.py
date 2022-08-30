import io
import os
import qrcode


# COMPUTE PRICE BASED ON NUMBER OF TICKETS
def compute_price(numTickets: int) -> float:
    cost = {
        1: float(os.environ.get("TICKET_PRICE_1")),
        2: float(os.environ.get("TICKET_PRICE_2")),
    }
    return (numTickets % 2) * cost[1] + (numTickets // 2) * cost[2]


# STRIP @ AND CONVERT USERNAME TO LOWERCASE
def format_username(username: str) -> str:
    return username[1:] if username.startswith("@") else username

# CREATE QR CODE WITH DATA
def createQRcode(data):
    bytesIO = io.BytesIO()
    qrcode.make(data).save(bytesIO, format="PNG")
    return bytesIO.getvalue()

