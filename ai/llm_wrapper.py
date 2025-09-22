"""
LLM Wrapper to bypass LiteLLM issues with Huawei Cloud ModelArts
"""
import os
import requests
import json
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
try:
    from ai.config import settings
except Exception:
    import ai.config.settings as settings

# Load environment variables from the main project .env file
from pathlib import Path
main_project_root = Path(__file__).parent.parent
env_file = main_project_root / ".env"
load_dotenv(env_file)

class HuaweiCloudLLM(ChatOpenAI):
    """Wrapper for Huawei ModelArts chat.completions using DeepSeek API key as Bearer token"""
    
    def __init__(self, **kwargs):
        # Huawei ModelArts endpoint provided by competition
        self._base_url = kwargs.get(
            "base_url",
            os.getenv(
                "AI_DEEPSEEK_BASE_URL",
                "https://pangu.ap-southeast-1.myhuaweicloud.com/api/v2/chat/completions",
            ),
        )
        self._deepseek_model = kwargs.get(
            "model",
            os.getenv("AI_DEEPSEEK_MODEL", os.getenv("AI_MODEL", "deepseek-r1-distil-qwen-32b_raziqt")),
        )
        # Store token locally to avoid relying on superclass attribute names
        self._token = kwargs.get("api_key", os.getenv("DEEPSEEK_API_KEY"))
        
        super().__init__(
            model="gpt-3.5-turbo",  # Use a known model name
            temperature=kwargs.get("temperature", 0.1),
            api_key=self._token,
            base_url=self._base_url,
            default_headers={
                "Authorization": f"Bearer {self._token}"
            }
        )
    
    @property
    def base_url(self):
        """Return the base URL"""
        return getattr(
            self,
            '_base_url',
            "https://pangu.ap-southeast-1.myhuaweicloud.com/api/v2/chat/completions",
        )
    
    @property
    def deepseek_model(self):
        """Return the DeepSeek model name"""
        return getattr(self, '_deepseek_model', "deepseek-r1-distil-qwen-32b_raziqt")
    
    @property
    def huawei_model(self):
        """Return the DeepSeek model name (for backward compatibility)"""
        return self.deepseek_model
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager = None,
        **kwargs: Any,
    ):
        """Override _generate to call Huawei ModelArts directly"""
        
        # Convert messages to the format expected by DeepSeek
        formatted_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                formatted_messages.append({"role": "assistant", "content": message.content})
            elif isinstance(message, SystemMessage):
                formatted_messages.append({"role": "system", "content": message.content})
        
        # Prepare payload for Huawei ModelArts
        payload = {
            "model": self.deepseek_model,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "max_tokens": kwargs.get("max_tokens", settings.DEFAULT_MAX_TOKENS)
        }
        
        # Prepare headers (ALWAYS Authorization: Bearer)
        token = getattr(self, "_token", None) or os.getenv("DEEPSEEK_API_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        
        try:
            # Make direct API call with retries/backoff
            import time
            read_timeout = settings.HUAWEI_API_READ_TIMEOUT_SECONDS
            connect_timeout = settings.HUAWEI_API_CONNECT_TIMEOUT_SECONDS
            timeouts = (connect_timeout, read_timeout)
            backoffs = settings.HUAWEI_REQUEST_BACKOFFS
            last_error: Exception | None = None
            for attempt in range(len(backoffs) + 1):
                try:
                    response = requests.post(
                        self.base_url,
                        headers=headers,
                        json=payload,
                        timeout=timeouts,
                    )
                    if response.status_code >= 400:
                        raise Exception(f"HTTP {response.status_code}: {response.text[:800]}")
                    response_data = response.json()
                    content = response_data['choices'][0]['message']['content']
                    from langchain_core.outputs import LLMResult, Generation
                    generation = Generation(text=content)
                    return LLMResult(generations=[[generation]])
                except requests.exceptions.Timeout as te:
                    last_error = te
                    if attempt < len(backoffs):
                        time.sleep(backoffs[attempt])
                        continue
                    raise
                except Exception as e:
                    # Non-timeout errors propagate immediately
                    raise
            
        except Exception as e:
            raise Exception(f"Huawei ModelArts API call failed: {e}")

# Create instance
huawei_llm_wrapper = HuaweiCloudLLM(
    model=os.getenv("AI_DEEPSEEK_MODEL", os.getenv("AI_MODEL", "deepseek-r1-distil-qwen-32b_raziqt")),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv(
        "AI_DEEPSEEK_BASE_URL",
        "https://pangu.ap-southeast-1.myhuaweicloud.com/api/v2/chat/completions",
    ),
    temperature=0.1,
)
