import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bottle import request

##############################
def send_reset_email(email, key):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    domain = request.urlparts.scheme + "://" + request.urlparts.netloc
    reset_link = f"{domain}/reset-password/{key}"
    msg = MIMEText(f"Click the link to reset your password: {reset_link}")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = from_email
    msg["To"] = email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())

##############################
def send_block_email(email):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    msg = MIMEText(f"You are deleted bro")
    msg["Subject"] = "Account Blocked"
    msg["From"] = from_email
    msg["To"] = email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())


##############################
def send_unblock_email(email):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    msg = MIMEText(f"You are no longer deleted bro")
    msg["Subject"] = "account un-blocked"
    msg["From"] = from_email
    msg["To"] = email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
##############################
def send_block_property_email(email):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    msg = MIMEText(f"your property has been blocked")
    msg["Subject"] = "Proerty blocked"
    msg["From"] = from_email
    msg["To"] = email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())

##############################
def send_unblock_property_email(email):
    from_email = 'joeybidenisbased@gmail.com'
    from_password = 'tdvi euik qgsa bzdf'

    msg = MIMEText(f"your property is no longer blocked")
    msg["Subject"] = "Property un-blocked"
    msg["From"] = from_email
    msg["To"] = email

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())

##############################