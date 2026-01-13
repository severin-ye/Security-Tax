"""LLM factory for creating language model instances"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_llm(
    provider: str = "openai",
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 2000,
    **kwargs
):
    """
    Create an LLM instance based on provider
    
    Args:
        provider: LLM provider (openai, deepseek, qwen, ollama)
        model: Model name
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        **kwargs: Additional provider-specific arguments
        
    Returns:
        LangChain LLM instance
    """
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )
    
    elif provider == "deepseek":
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            base_url="https://api.deepseek.com",
            **kwargs
        )
    
    elif provider == "qwen":
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )
    
    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        return ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url,
            **kwargs
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def create_llm_from_config(config: dict):
    """
    Create LLM from configuration dictionary
    
    Args:
        config: Configuration dict with keys: provider, model, temperature, etc.
        
    Returns:
        LangChain LLM instance
    """
    return create_llm(
        provider=config.get("provider", "openai"),
        model=config.get("model", "gpt-4"),
        temperature=config.get("temperature", 0.7),
        max_tokens=config.get("max_tokens", 2000),
    )
