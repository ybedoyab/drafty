"""Huawei Cloud ModelArts LLM: direct integration with chat.completions API."""
import os
import requests
import json
from typing import List, Dict, Any, Optional
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult, Generation
from langchain_core.language_models.llms import LLM

class HuaweiModelArtsLLM(LLM):
    """Custom LLM for Huawei Cloud ModelArts"""
    
    model_name: str
    api_key: str
    base_url: str
    temperature: float
    max_tokens: int
    
    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: str,
        temperature: float = 0.1,
        max_tokens: int = 1024
    ):
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def invoke(self, input, config=None, **kwargs):
        if isinstance(input, str):
            return self._call(input, **kwargs)
        elif isinstance(input, list):
            return self._generate(input, **kwargs)
        else:
            raise ValueError("Input must be string or list of messages")
    
    def predict(self, text: str, **kwargs) -> str:
        return self._call(text, **kwargs)
    
    def predict_messages(self, messages: List[BaseMessage], **kwargs) -> BaseMessage:
        result = self._generate(messages, **kwargs)
        return AIMessage(content=result.generations[0][0].text)
    
    def generate_prompt(self, prompts: List[str], **kwargs) -> LLMResult:
        generations = []
        for prompt in prompts:
            response = self._call(prompt, **kwargs)
            generations.append([Generation(text=response)])
        return LLMResult(generations=generations)
    
    async def agenerate_prompt(self, prompts: List[str], **kwargs) -> LLMResult:
        return self.generate_prompt(prompts, **kwargs)
    
    async def apredict(self, text: str, **kwargs) -> str:
        return self.predict(text, **kwargs)
    
    async def apredict_messages(self, messages: List[BaseMessage], **kwargs) -> BaseMessage:
        return self.predict_messages(messages, **kwargs)
        
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        
        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.api_key
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            
            return content.strip()
            
        except Exception as e:
            raise Exception(f"Huawei Cloud ModelArts API call failed: {e}")
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        
        prompt_parts = []
        for message in messages:
            if isinstance(message, HumanMessage):
                prompt_parts.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                prompt_parts.append(f"Assistant: {message.content}")
            elif isinstance(message, SystemMessage):
                prompt_parts.append(f"System: {message.content}")
        
        prompt = "\n".join(prompt_parts)
        
        response_text = self._call(prompt, stop, run_manager, **kwargs)
        
        generation = Generation(text=response_text)
        
        return LLMResult(generations=[[generation]])
    
    @property
    def _llm_type(self) -> str:
        return "huawei_modelarts"

# Create instance using environment variables
huawei_llm = HuaweiModelArtsLLM(
    model_name=os.getenv("AI_DEEPSEEK_MODEL", os.getenv("AI_MODEL", "deepseek-r1-distil-qwen-32b_raziqt")),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("AI_DEEPSEEK_BASE_URL", "https://pangu.ap-southeast1.myhuaweicloud.com/api/v2/chat/completions"),
    temperature=0.1,
    max_tokens=1024
)
