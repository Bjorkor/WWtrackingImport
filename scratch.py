import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()
# Replace the following placeholders with your own values
from_email = "sales@hdlusa.com"
from_password = os.getenv('EMAIL_CRED')
to_email = "tbarker@hdlusa.com"

# Create the message
subject = "testerino"
body = "this is a test"

msg = MIMEMultipart()
port = 465

msg['To'] = to_email
msg['Subject'] = subject
msg['From'] = from_email

msg.attach(MIMEText(body, "plain"))

# Attachment
attachment_path = "order_invoice.pdf"  # Provide the path to your attachment
attachment_name = os.path.basename(attachment_path)
with open(attachment_path, "rb") as attachment_file:
    attachment_data = attachment_file.read()

attachment = MIMEBase("application", "octet-stream")
attachment.set_payload(attachment_data)
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", f"attachment; filename={attachment_name}")
msg.attach(attachment)

with smtplib.SMTP_SSL("mail.runspot.net", port) as server:
    server.login(from_email, from_password)
    server.send_message(msg)

print("Email sent successfully")
