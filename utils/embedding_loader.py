#utils/embedding_loader.py
# 使用 langchain-openai 提供的 OpenAIEmbeddings（已替换旧版本）

import os
from dotenv import load_dotenv
from pydantic import SecretStr


load_dotenv()

def load_embedding_model(provider: str | None = None):
    """
    provider 可选:
      - "openai"   ➜ 使用 text-embedding-ada-002
      - "gemini"   ➜ 使用 models/embedding-001
    若 provider=None 则自动读取环境变量 EMBEDDING_PROVIDER，默认为 "openai"
    """
    provider = (provider or os.getenv("EMBEDDING_PROVIDER", "openai")).lower()

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")


   

    else:
        raise ValueError(f"❌ Unsupported embedding provider: {provider}")
