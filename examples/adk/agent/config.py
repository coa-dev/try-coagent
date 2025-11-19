import os

from google.adk.models.lite_llm import LiteLlm

llm_model = os.environ.get("LLM_MODEL")
llm_api_key = os.environ.get("LLM_API_KEY")
llm_api_base = os.environ.get("LLM_API_BASE")

def get_llm_model() -> str:
    if llm_model is None:
        raise ValueError("LLM_MODEL must be set in the environment variables.")
    return llm_model

def get_llm_api_key() -> str:
    if llm_api_key is None:
        raise ValueError("LLM_API_KEY must be set in the environment variables.")
    return llm_api_key

def get_llm_api_base() -> str | None:
    return llm_api_base

def get_litellm_model() -> LiteLlm:
    return LiteLlm(
        model=get_llm_model(),
        api_key=get_llm_api_key(),
        api_base=get_llm_api_base(),
        custom_llm_provider="gemini"
    )
