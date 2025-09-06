# AI Project — AI Personal Assistant (Agentic)

This project is a complete, ready-to-run Python agent built with LangChain and OpenAI (GPT-4)
that automates workflow tasks: calendar, email, and news retrieval.

## Quick start (full version - requires API keys)

1. Unzip AI_Project.zip and `cd` into the directory.
2. Create a virtualenv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the example env and fill your keys:
   ```bash
   cp .env.example .env
   # open .env and fill OPENAI_API_KEY, GOOGLE_SERVICE_ACCOUNT_FILE, SMTP credentials, NEWS_API_KEY (optional)
   ```
5. Place your Google service account JSON at the path you set in `.env` (or configure OAuth separately).
6. Run the agent:
   ```bash
   python app.py
   ```

## Example commands (type at the prompt)
- `daily_brief`  — fetches top news, today's calendar events, and (mock) unread emails.
- `summarize_inbox` — summarizes unread emails.
- `schedule_meeting;Team Sync;2025-09-10T14:00;60;teammate@example.com` — schedule meeting.
- `send_email|Project Update|boss@example.com|The task is complete` — send an email.

## Notes
- This "full" version uses Google Calendar (service account), SMTP for email, and NewsAPI (or RSS fallback).
- Do NOT commit real credentials to version control.
- If you prefer a quick-start mock version, run the mocked_demo branch (not included here).
