
### 📦 `utils/` 文件夹说明

这个目录是 **项目的通用工具模块集**，封装了不同功能的可复用函数与结构体。每个文件职责明确，互不耦合，便于后续维护与拓展。

---

### 🧠 模块一览

|文件名|作用简介|
|---|---|
|`model_loader.py`|通用模型调用工厂，支持 Gemini / OpenAI 的智能调用|
|`embedding_loader.py`|嵌入模型加载器，支持 FAISS 召回所需的向量模型切换|
|`project_utils.py`|工具函数合集，如日志打印、模型状态判断、当前模型获取等|
|`models.py`|使用 Pydantic 定义的数据结构（例如：EmailData）|
|`__init__.py`|设置导出接口，支持 `from utils import ...` 简洁引用|

---

### 🧩 模块功能详解

#### `model_loader.py`

封装调用语言模型的逻辑（如 `call_model(prompt)`），可根据环境变量或传参自动切换 OpenAI / Gemini。包含懒加载、防止未设置 API 报错等机制，避免模型初始化冲突。

#### `embedding_loader.py`

支持加载 OpenAI / Gemini 嵌入模型（用于文本向量化）。通过 `load_embedding_model(provider)` 自动选择模型，适配 FAISS 等向量检索库。

#### `project_utils.py`

提供：

- `print_model_status()`：输出当前模型状态（带颜色提示）
    
- `log_result()`：保存日志文件
    
- `get_current_model()`：返回当前使用的 LLM 提供商
    

#### `models.py`

使用 `pydantic.BaseModel` 定义结构化数据。例如：

```python
class EmailData(BaseModel):
    sender: str
    subject: str
    content: str
```

便于校验输入字段、生成 IDE 智能提示、结构清晰。

---

### 🚀 示例：如何使用

```python
from utils import call_model, load_embedding_model, EmailData

prompt = "请用英语回复这封邮件"
model_output = call_model(prompt)

embedding_model = load_embedding_model()
```

---

### 🧩 后续建议

- 增加 `logger.py` 专门处理日志格式与存储路径
    
- 增加 `config_loader.py` 动态读取配置（如 .env、JSON、YAML）
    
- `models.py` 中可拆分不同结构到子模块，如 `email_models.py`, `crm_models.py` 等
 
