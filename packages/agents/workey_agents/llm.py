"""LLM provider abstraction - supports OpenAI, Anthropic, Gemini."""
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel


def get_llm(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> BaseChatModel:
    """Get a configured LLM instance based on provider settings."""
    provider = provider or os.getenv("LLM_PROVIDER", "openai")
    
    if provider == "openai":
        model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "anthropic":
        model = model or os.getenv("LLM_MODEL", "claude-3-5-haiku-20241022")
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Use 'openai' or 'anthropic'.")
