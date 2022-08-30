

import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api.services.config.config import getConcertInfo
from api.services.utils import createQRcode


class EmailService():

    def __init__(self, user, num_tickets):
        super().__init__()

        self.user = user
        self.num_tickets = num_tickets

        self._EMAIL_ID = os.environ.get("EMAIL_ID")
        self._EMAIL_PW = os.environ.get("EMAIL_PW")

        self.CONCERT_INFO = getConcertInfo()

    def sendEmail(self):

        smtp_server = "smtp.gmail.com"
        port = 587

        info = self.CONCERT_INFO

        target_email = self.user["email"]

        # CREATE MESSAGE INSTANCE
        msg = MIMEMultipart("alternative")
        msg['Subject'] = info["email_subject"]
        msg['From'] = self._EMAIL_ID
        msg['To'] = target_email

        # ATTACH BODY TO MESSAGE CONTAINER
        msg.attach(MIMEText(self.generateText(), 'plain'))
        msg.attach(MIMEText(self.generateHTML(), 'html'))

        # ATTACH QR CODE AS EMAIL ATTACHMENT
        qr_code = createQRcode(self.user)
        img = MIMEImage(qr_code)
        img.add_header("Content-Disposition", "attachment",
                       filename=self.generateFilename())
        msg.attach(img)

        # SEND EMAIL VIA SMTP
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self._EMAIL_ID, self._EMAIL_PW)
            server.sendmail(self._EMAIL_ID, target_email, msg.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()

    def generateFilename(self):
        return f'{self.user["name"]}_TICKET_QR'

    def generateText(self):
        return f"Ticket Order Confirmation for {self.user['name']} - {self.num_tickets} Tickets Bought - Total Tickets {self.user['tickets_bought']}"

    def generateHTML(self):

        return f"""
        <body class="" style="background-color: #eaebed;font-family: sans-serif;-webkit-font-smoothing: antialiased;font-size: 14px;line-height: 1.4;margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;min-width: 100%;width: 100%;background-color: #eaebed;">
            <tr>
                <td style="font-family: sans-serif;font-size: 14px;vertical-align: top;">&nbsp;</td>
                <td class="container" style="font-family: sans-serif;font-size: 14px;vertical-align: top;display: block;max-width: 580px;padding: 10px;width: 580px;margin: 0 auto !important;">
                    <div class="header" style="padding: 20px 0;">
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;min-width: 100%;width: 100%;">
                            <tr>
                                <td class="align-center" width="100%" style="font-family: sans-serif;font-size: 14px;vertical-align: top;text-align: center;">
                                    <h1 style="color: #06090f;font-family: sans-serif;font-weight: 300;line-height: 1.4;margin: 0;margin-bottom: 30px;font-size: 35px;text-align: center;text-transform: capitalize;"> Ticket Order Confirmation </h1>
                                    <h2 style="color: #06090f;font-family: sans-serif;font-weight: 400;line-height: 1.4;margin: 0;margin-bottom: 30px;"> {self.num_tickets} Tickets Purchased By: <b>{self.user["name"]}</b></h2>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="content" style="box-sizing: border-box;display: block;margin: 0 auto;max-width: 580px;padding: 10px;">
                        <!-- START CENTERED WHITE CONTAINER -->
                        <span class="preheader" style="color: transparent;display: none;height: 0;max-height: 0;max-width: 0;opacity: 0;overflow: hidden;mso-hide: all;visibility: hidden;width: 0;">{self.CONCERT_INFO["concert_name"]}</span>
                        <table role="presentation" class="main" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;min-width: 100%;width: 100%;background: #ffffff;border-radius: 3px;">
                            <!-- START MAIN CONTENT AREA -->
                            <tr>
                                <td class="wrapper" style="font-family: sans-serif;font-size: 14px;vertical-align: top;box-sizing: border-box;padding: 20px;">
                                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;min-width: 100%;width: 100%;">
                                        <tr>
                                            <td style="font-family: sans-serif;font-size: 14px;vertical-align: top;">
                                                <p style="font-family: sans-serif;font-size: 14px;font-weight: normal;margin: 0;margin-bottom: 15px;">👋&nbsp; Thank you for puchasing tickets for {self.CONCERT_INFO["concert_name"]}</p>
                                                <p style="font-family: sans-serif;font-size: 14px;font-weight: normal;margin: 0;margin-bottom: 15px;">✨&nbsp; Please download the QR code in the attachment and show at the venue</p>
                                                <p style="font-family: sans-serif;font-size: 14px;font-weight: normal;margin: 0;margin-bottom: 15px;">⏰&nbsp; {self.CONCERT_INFO["concert_time"]}</p>
                                                <p style="font-family: sans-serif;font-size: 14px;font-weight: normal;margin: 0;margin-bottom: 15px;">📍&nbsp; {self.CONCERT_INFO["concert_location"]} </p>
                                                <p style="font-family: sans-serif;font-size: 14px;font-weight: normal;margin: 0;margin-bottom: 15px;">📞&nbsp; Please contact {self.CONCERT_INFO["concert_contact"]} for any inquiries</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <!-- END MAIN CONTENT AREA -->
                        </table>
                        <!-- END CENTERED WHITE CONTAINER -->
                    </div>
                </td>
                <td style="font-family: sans-serif;font-size: 14px;vertical-align: top;">&nbsp;</td>
            </tr>
        </table>
        <div class="footer" style="clear: both;margin-top: 10px;text-align: center;width: 100%;">
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;min-width: 100%;width: 100%;">
                <tr>
                    <td class="content-block" style="font-family: sans-serif;font-size: 12px;vertical-align: top;padding-bottom: 10px;padding-top: 10px;color: #9a9ea6;text-align: center;">
                        <span class="apple-link" style="color: #9a9ea6;font-size: 12px;text-align: center;">Purchased Through Venmo ID: <b>@{self.user["venmo_id"]}</b></span>
                    </td>
                </tr>
            </table>
        </div>
        </body>
        """
