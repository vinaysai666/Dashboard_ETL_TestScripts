import sys

sys.dont_write_bytecode = True

import smtplib
import os
from email.message import EmailMessage

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_SENDER = "vinays@newstreettech.com"
EMAIL_PASSWORD = "Snvvsssv@2001"  
EMAIL_RECEIVER = "padalapraneeth@newstreettech.com"

# File to Attach
file_path = "C:\\Users\\Vinay\\Desktop\\Fast-api\\Test_Execution_Report.xlsx" 

def email_generation():
   
        msg = EmailMessage()
        msg["Subject"] = "Automated Email with Attachment"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content("Please find the attached file.")

        # Attach File


        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        # Send Email
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

