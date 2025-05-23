import json
from email_sender.send_email import EmailSender
from website_clocker.clock_hours import WebsiteClocker
from common.date_operations import load_and_format_template

def load_credentials(path='credentials-test.json'):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    send_email()

    # # Initialize the website clocker
    # website_clocker = WebsiteClocker()
    # # Clock hours by visiting the specified website
    # website_clocker.clock_hours()

def send_email():
    # Load credentials and recipients
    credentials = load_credentials()

    html_message = load_and_format_template(
        'email_templates/tripple_crown_weekly_stat.html',
        'Tripple Crown Team'
    )

    sender = EmailSender(credentials["username"], credentials["password"])
    sender.send_email(
        to_email=credentials["to"],
        subject="Status Update on Asset Tracker",
        html_message=html_message,
        cc_emails=credentials.get("cc", []),
        bcc_emails=credentials.get("bcc", [])
    )

if __name__ == "__main__":
    main()
