# AI_Project/utils.py
import logging, os
LOG_LEVEL = os.environ.get('LOG_LEVEL','INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger('ai_project')
