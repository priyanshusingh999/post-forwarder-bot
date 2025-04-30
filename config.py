import os

# Config Variables from environment or fallback
TOKEN = os.getenv('TOKEN') or ""
OWNER_ID = int(os.getenv('OWNER_ID') or )
FORCE_SUB_CHANNEL = os.getenv('FORCE_SUB_CHANNEL') or ""
