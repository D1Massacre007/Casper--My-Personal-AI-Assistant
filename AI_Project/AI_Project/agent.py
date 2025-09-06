import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path)

from langchain_openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)

class GoogleCalendarTool:
    def get_today_events(self):
        return ["Dummy Event 1 10:00 AM", "Dummy Event 2 3:00 PM"]
    def create_event(self, title, date_time, duration, attendees):
        return f"Event '{title}' scheduled for {date_time} with attendees {attendees}, Sir."

class EmailTool:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
    def send_email(self, to, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            return f"Email sent to {to} with subject '{subject}', Sir."
        except Exception as e:
            return f"Failed to send email: {e}, Sir."
    def get_unread_emails(self):
        return ["Dummy email from boss", "Dummy email from HR"]
    def summarize_emails(self):
        return "You have 2 unread emails: Dummy email from boss, Dummy email from HR, Sir."

class NewsTool:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.endpoint = "https://newsapi.org/v2/top-headlines"
        self.country = "us"
    def get_latest_news(self):
        if not self.api_key or self.api_key == "REPLACE_ME":
            return ["News API key not configured, Sir."]
        try:
            params = {"apiKey": self.api_key, "country": self.country, "pageSize": 5}
            response = requests.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
            return news_list if news_list else ["No news found, Sir."]
        except Exception as e:
            return [f"Failed to fetch news: {e}, Sir."]

calendar_tool = GoogleCalendarTool()
email_tool = EmailTool()
news_tool = NewsTool()

def greet_user():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    print(f"\n🤖 Greetings, Sir! I am Casper, your humble AI assistant. {greeting}, Sir! I am at your service.\n")

def run_agent():
    logging.info("🤖 AI Project Agent Started!")
    greet_user()
    while True:
        print("\nSir, please choose a command or enter the number corresponding to your request:")
        print("1. daily_brief  → Receive today’s events, news & emails")
        print("2. summarize_inbox → Summarize unread emails")
        print("3. schedule_meeting → Schedule a meeting")
        print("4. send_email → Send an email")
        print("5. exit → Stop the assistant")

        cmd_input = input("\nEnter command, Sir: ").strip().lower().replace(".", "")
        cmd_map = {
            "1":"daily_brief",
            "2":"summarize_inbox",
            "3":"schedule_meeting",
            "4":"send_email",
            "5":"exit",
            "daily brief":"daily_brief",
            "summarize inbox":"summarize_inbox",
            "schedule meeting":"schedule_meeting",
            "send email":"send_email",
            "exit":"exit"
        }
        cmd = cmd_map.get(cmd_input, cmd_input)

        if cmd == "daily_brief":
            events = calendar_tool.get_today_events()
            emails = email_tool.get_unread_emails()
            news = news_tool.get_latest_news()
            print("\n=== DAILY BRIEF ===")
            print(f"\n📅 Events: {events}")
            print(f"\n📧 Emails: {emails}")
            print(f"\n📰 News: {news}")
            input("\nCasper: I trust this summary serves you well, Sir. Press Enter to continue...")
        elif cmd == "summarize_inbox":
            print("\n=== INBOX SUMMARY ===")
            print(email_tool.summarize_emails())
            input("\nCasper: Your inbox has been summarized, Sir. Press Enter to continue...")
        elif cmd == "schedule_meeting":
            title = input("Enter meeting title, Sir: ")
            date_time = input("Enter meeting date & time (YYYY-MM-DD HH:MM), Sir: ")
            duration = input("Enter duration in minutes, Sir: ")
            attendees = input("Enter attendee emails (comma separated), Sir: ").split(",")
            print("\n📅", calendar_tool.create_event(title, date_time, duration, attendees))
            input("\nCasper: The meeting has been successfully scheduled, Sir. Press Enter to continue...")
        elif cmd == "send_email":
            to = input("Recipient email, Sir: ")
            subject = input("Subject, Sir: ")
            body = input("Body, Sir: ")
            result = email_tool.send_email(to, subject, body)
            print("\n📧", result)
            input("\nCasper: Email dispatched successfully, Sir. Press Enter to continue...")
        elif cmd == "exit":
            logging.info("Shutting down AI Project Agent...")
            print("\nCasper: Farewell, Sir! I remain at your service whenever you require assistance. 👋")
            break
        else:
            input("⚠️ Apologies, Sir. I did not comprehend that command. Kindly press Enter and try again!")

if __name__ == "__main__":
    run_agent()
