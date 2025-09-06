# AI_Project/tools/email_tool.py
import os
import smtplib
from email.message import EmailMessage

class EmailTool:
    def __init__(self):
        self.host = os.environ.get('SMTP_HOST')
        self.port = int(os.environ.get('SMTP_PORT', 587))
        self.user = os.environ.get('SMTP_USER')
        self.password = os.environ.get('SMTP_PASSWORD')
        if not all([self.host, self.user, self.password]):
            print('Warning: SMTP not fully configured; email sending will fail until configured.')

    def send_email(self, payload: str):
        """Expected payload format (pipe-separated): subject|to1,to2|body"""
        parts = payload.split('|')
        if len(parts) < 3:
            return 'Usage: subject|to1,to2|body'
        subject, tos, body = parts[0], parts[1], parts[2]
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = tos
        msg.set_content(body)

        with smtplib.SMTP(self.host, self.port) as s:
            s.starttls()
            s.login(self.user, self.password)
            s.send_message(msg)
        return f'Email sent to {tos}'

    def run(self, query: str):
        return self.send_email(query)
