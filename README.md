
1. Save to Mongo DB
    - Name              string
    - Venmo ID          string
    - Email             string
    - Num Tickets       number
    - Paid              boolean
2. Request payment with link {root_address}/verify_payment/{venmoID}
3. If link is clicked
    - Check if Paid
        - If Paid
            - Display success page
            - Update DB list            (QUERY w/ venmoID)
            - Generate QR code          ()
            - Send email with QR code as attachment
            - Update Google Sheets
        - If Not paid
            - Display error page