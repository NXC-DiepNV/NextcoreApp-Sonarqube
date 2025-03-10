import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class MailCore:
    def __init__(self, mail_server: str, mail_port: int, mail_user: str, mail_password: str):
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_password = mail_password

    def send_email(self, to_email, subject, body, attachment=None, type='plain'):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.mail_user
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, type))

            if attachment:
                with open(attachment, "rb") as f:
                    attach_file = MIMEApplication(
                        f.read(), _subtype="octet-stream")
                    attach_file.add_header(
                        'Content-Disposition', 'attachment', filename=attachment)
                    msg.attach(attach_file)

            with smtplib.SMTP_SSL(self.mail_server, self.mail_port) as server:
                # server.set_debuglevel(1)
                server.login(self.mail_user, self.mail_password)
                server.sendmail(self.mail_user, to_email, msg.as_string())
                print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Error sending email: {e}")
