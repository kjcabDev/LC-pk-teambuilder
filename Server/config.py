import os

PORT = int(os.environ.get("PK_SVR_HOST", 8084))
HOST = os.environ.get("PK_SVR_PORT", '0.0.0.0')
DEBUG = os.environ.get("PK_SVR_DEBUG", "1") == "0"
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

# Agent Specific Variables
AGENT_MODEL = "claude-haiku-4-5-20251001"