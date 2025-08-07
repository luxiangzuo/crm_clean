import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件里的环境变量

# 模型提供方：openai / gemini
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini")  # 默认 gemini

# OpenAI 配置
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Gemini 配置
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")

ESPOTCRM_URL = os.getenv("ESPOTCRM_URL")
ESPOTCRM_USERNAME = os.getenv("ESPOTCRM_USERNAME")
ESPOTCRM_PASSWORD = os.getenv("ESPOTCRM_PASSWORD")
print("📦 Loaded CRM Config: ", ESPOTCRM_USERNAME, ESPOTCRM_PASSWORD, ESPOTCRM_URL)

