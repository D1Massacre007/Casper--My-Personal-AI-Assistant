# AI_Project/prompts.py
def build_prompt_chain(task_name: str) -> str:
    if task_name == 'daily_brief':
        return (
            'You are AI Project assistant. Provide a concise daily brief: '
            '1) Top news headlines, 2) Today\'s calendar events, '
            '3) Any unread important emails (short summary). Use tools by calling them with clear commands.'
        )
    if task_name == 'summarize_inbox':
        return 'Summarize unread emails in the inbox in 5 bullet points with actionable items.'
    return task_name
