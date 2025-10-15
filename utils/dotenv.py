import os

from dotenv import load_dotenv
from pydantic import BaseModel


class API_ENV_CONFIG(BaseModel):
    api_key: str
    base_url: str


# 加载 .env 文件
load_dotenv()

SILICONFLOW_CONFIG = API_ENV_CONFIG(
    api_key=os.getenv("SILICONFLOW_API_KEY", ""),
    base_url=os.getenv("SILICONFLOW_BASE_URL", ""),
)
