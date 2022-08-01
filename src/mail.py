import smtplib
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

# this class contains the configuration for accessing the mail server
class EMailProperties:
    def __init__(self):
        self.authenticate = None
        self.smtp_server = None
        self.port = None
        self.sender = None
        self.recipient = None
        self.password = None

# sends an email via smtp with an attachment
# this is tested to work with the kit smarthost server
# using a different host might require small adjustments
def send_email(properties, subject, text, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = properties.sender
    msg["To"] = properties.recipient
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    attachment = MIMEBase('application', "octet-stream")
    header = 'Content-Disposition', 'attachment; filename="%s"' % attachment_path
    try:
        with open(attachment_path, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_to_attach
        print(msg)
        return

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(properties.smtp_server, properties.port) as server:
            server.starttls(context=context)
            if properties.authenticate:
                server.login(properties.sender, properties.password)
            server.sendmail(properties.sender, properties.recipient, msg.as_string())
    except Exception as e:
        print(e)
