from bottle import request
import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "joeybidenisbased@gmail.com"
SMTP_PASSWORD = "tdvi euik qgsa bzdf"

def send_reset_email(user_email, user_pk):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    domain = request.urlparts.scheme + "://" + request.urlparts.netloc
    reset_link = f"{domain}/reset-password/{user_pk}"
    msg = MIMEText(f"Click the link to reset your password: {reset_link}")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = from_email
    msg["To"] = user_email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())