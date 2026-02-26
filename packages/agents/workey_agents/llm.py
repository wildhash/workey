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
    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).strip().lower()

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
    elif provider == "gemini":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as e:
            raise ImportError(
                "Gemini support requires installing 'langchain-google-genai'."
            ) from e

        model = model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Gemini provider selected but neither GOOGLE_API_KEY nor GEMINI_API_KEY is set."
            )
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=api_key,
        )
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. Use 'openai', 'anthropic', or 'gemini'."
        )
