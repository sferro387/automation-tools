class EmailSender:
    def __init__(self, username, password):
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587  # TLS port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, html_message, cc_emails=None, bcc_emails=None):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import COMMASPACE

        cc_emails = cc_emails or []
        bcc_emails = bcc_emails or []

        # Create the HTML email message
        msg = MIMEText(html_message, 'html')
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email
        if cc_emails:
            msg['Cc'] = COMMASPACE.join(cc_emails)

        # Combine all recipients: TO + CC + BCC
        all_recipients = [to_email] + cc_emails + bcc_emails

        # Send the email
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, all_recipients, msg.as_string())
