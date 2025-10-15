from ai.chat_service import AIChatService, ServiceConfig
from utils.dotenv import SILICONFLOW_CONFIG

base_service = AIChatService(
    ServiceConfig(
        name="siliconflow-qwen3-8B",
        api_key=SILICONFLOW_CONFIG.api_key,
        base_url=SILICONFLOW_CONFIG.base_url,
        model="Qwen/Qwen3-8B",
    )
)
