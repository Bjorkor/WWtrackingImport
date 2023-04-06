import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import os
from dotenv import load_dotenv


context = ssl.create_default_context()
load_dotenv()
# Replace the following placeholders with your own values
from_email = "sales@hdlusa.com"
from_password = os.getenv('EMAIL_CRED')
to_email = "tbarker@hdlusa.com"
print(from_email)
print(from_password)
# Create the message
subject = "testerino"
body = "this is a test"

msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

# Add attachment
attachment_path = "order_invoice.pdf"  # Replace with the path to your attachment
attachment_filename = "order_invoice.pdf"  # Replace with the filename of your attachment

with open(attachment_path, "rb") as attachment_file:
    attachment = MIMEApplication(attachment_file.read(), _subtype="octet-stream")
    attachment.add_header("Content-Disposition", "attachment", filename=attachment_filename)
    msg.attach(attachment)

# Send the email
try:
    with smtplib.SMTP_SSL("mail.runspot.net", 465, context=context) as server:
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg)
        print("Email sent successfully")
except Exception as e:
    print("Error: Unable to send email")
    print(e)
