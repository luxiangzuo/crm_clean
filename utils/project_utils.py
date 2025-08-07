# project_utils.py
"""
通用工具模块：日志打印、模型状态提示、输出格式化等辅助函数
"""
import datetime
import config
from dotenv import load_dotenv
import os

load_dotenv()  # 加载.env环境变量

def get_current_model():
    provider = config.MODEL_PROVIDER.lower()
    if provider == "openai":
        return f"OpenAI - {config.OPENAI_MODEL}"
    elif provider == "gemini":
        return f"Gemini - {config.GEMINI_MODEL}"
    else:
        return "Unknown Provider"

def print_model_status():
    model_name = get_current_model()
    print(f"\n📡 Currently using model: {model_name}\n")

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_result(email_id, status, model):
    time_str = timestamp()
    print(f"[{time_str}] ✉️ Email {email_id} classified using {model}: {status}")
