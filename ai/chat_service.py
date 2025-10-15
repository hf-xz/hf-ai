# ai/chat_service.py
from fastapi import HTTPException
from openai import APIError, AsyncOpenAI, AuthenticationError, RateLimitError
from pydantic import BaseModel

from utils.log import base_logger


class ServiceConfig(BaseModel):
    name: str
    api_key: str
    base_url: str
    model: str
    system_prompt: str = ""
    temperature: float = 0.7
    top_p: float = 0.9


class AIChatService:
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=30.0,  # 添加超时，避免卡死
        )
        self.logger = base_logger.getChild(config.name)

    async def chat(self, prompt: str) -> str:
        self.logger.info(
            f"Request: {prompt[:60] + '...' if len(prompt) > 60 else prompt}"
        )

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
            )
            result = response.choices[0].message.content or ""
            self.logger.info(f"Success, response length: {len(result)}")
            return result

        except AuthenticationError:
            self.logger.error(f"Invalid API key")
            raise HTTPException(status_code=401, detail="Invalid SiliconFlow API key")

        except RateLimitError:
            self.logger.error(f"Rate limit exceeded")
            raise HTTPException(
                status_code=429, detail="Too many requests, please try later"
            )

        except APIError as e:
            self.logger.error(f"API error: {e}")
            raise HTTPException(status_code=502, detail="AI service unavailable")

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
