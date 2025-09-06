# tests/test_tools.py
from AI_Project.tools.news_tool import NewsTool

def test_news_fetch():
    n = NewsTool()
    out = n.fetch_headlines('top')
    assert out and isinstance(out, str)
