import os
from typing import Literal, Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")

# ========== OpenAI ==========
from openai import OpenAI
_openai_client: Optional[OpenAI] = None

def _get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY 未设置")
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client

def call_openai(prompt: str) -> str:
    client = _get_openai_client()
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        print(f"❌ OpenAI 调用失败: {e}")
        return ""


# ========== Gemini ==========
_genai_model = None
def _get_gemini_model():
    global _genai_model
    if _genai_model is None:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            _genai_model = genai.GenerativeModel("models/gemini-1.5-pro")
        except ImportError:
            raise ImportError("请先 pip install google-generativeai")
    return _genai_model

def call_gemini(prompt: str) -> str:
    try:
        model = _get_gemini_model()
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        print(f"❌ Gemini 调用失败: {e}")
        return ""


# ========== 工厂入口 ==========
def call_model(prompt: str,
               model_name: Literal["openai", "gemini"] | None = None,
               print_prompt: bool = False) -> str:
    """
    model_name=None ➜ 读取环境变量 LLM_PROVIDER，默认为 "openai"
    print_prompt=True ➜ 控制台打印 prompt 内容，方便调试
    """
    model_name = (model_name or os.getenv("LLM_PROVIDER", "openai")).lower()  # type: ignore
    if print_prompt:
        print(f"\n📝 [Prompt to {model_name}]:\n{prompt}\n")

    if model_name == "openai":
        return call_openai(prompt)
    elif model_name == "gemini":
        return call_gemini(prompt)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def get_current_model() -> str:
    """返回当前使用的模型名，供日志记录调用"""
    return os.getenv("LLM_PROVIDER", "openai").lower()
