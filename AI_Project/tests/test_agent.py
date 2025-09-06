# tests/test_agent.py
from AI_Project.agent import AIProjectAgent
import os

def test_agent_init():
    # Don't fail if OPENAI_API_KEY missing; just instantiate
    a = AIProjectAgent()
    assert hasattr(a, 'handle_command')
