# app.py - entrypoint for AI Project
import os
from dotenv import load_dotenv
load_dotenv()

from AI_Project.agent import AIProjectAgent

if __name__ == '__main__':
    agent = AIProjectAgent()
    print('AI Project agent started. Example commands: daily_brief, summarize_inbox, schedule_meeting')

    while True:
        try:
            cmd = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nShutting down...')
            break
        if not cmd:
            continue
        if cmd in {'exit','quit'}:
            print('Shutting down...')
            break
        try:
            result = agent.handle_command(cmd)
            print('\n-- RESULT --\n')
            print(result)
        except Exception as e:
            print('Error:', e)
