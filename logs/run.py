import logging

# 初始化日志配置
logging.basicConfig(
    filename="logs/run.log",         # 日志文件路径
    level=logging.INFO,              # 记录 info 级别以上的日志
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_result(email_id, status, model):
    msg = f"📧 Email {email_id} classified using {model}: {status}"
    print(msg)
    logging.info(msg)

def log_error(email_id, error_msg):
    msg = f"❌ Error on Email {email_id}: {error_msg}"
    print(msg)
    logging.error(msg)

def log_prompt(email_id, prompt):
    msg = f"📨 Prompt for Email {email_id}:\n{prompt}"
    print(msg)
    logging.info(msg)
