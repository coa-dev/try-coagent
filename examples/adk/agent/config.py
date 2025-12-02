import os

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.google_llm import Gemini

llm_model = os.environ.get("LLM_MODEL")
llm_api_key = os.environ.get("LLM_API_KEY")
llm_api_base = os.environ.get("LLM_API_BASE")
gemini_model = os.environ.get("GEMINI_MODEL")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

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
    )

def get_gemini_model_name() -> str:
    if gemini_model is None:
        raise ValueError("GEMINI_MODEL must be set in the environment variables.")
    return gemini_model


def get_gemini_api_key() -> str:
    if gemini_api_key is None:
        raise ValueError("GEMINI_API_KEY must be set in the environment variables.")
    return gemini_api_key

def get_gemini_model() -> Gemini:
    return Gemini(
        model=get_gemini_model_name(),
        api_key=get_gemini_api_key(),
    )