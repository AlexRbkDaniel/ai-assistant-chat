import logging
import threading

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from config import DEFAULT_MODEL_ID, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
from shared.ai_response import default_json_parser

load_dotenv()

logger = logging.getLogger(__name__)

default_prompt_template = PromptTemplate(
    template='''{system_prompt}\n\n{format_instructions}\n\n{user_prompt}''',
    input_variables=['system_prompt', 'user_prompt'],
    partial_variables={'format_instructions': default_json_parser.get_format_instructions()}
)

_model_cache: dict[str, ChatOpenAI] = {}
_cache_lock = threading.Lock()

def load_model(
    model_id: str = DEFAULT_MODEL_ID,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS
) -> ChatOpenAI:
    cache_key = f"{model_id}_{temperature}_{max_tokens}"

    with _cache_lock:
        if cache_key in _model_cache:
            logger.debug("Returning cached model: %s", model_id)
            return _model_cache[cache_key]

        logger.info("Loading model: %s (temperature=%.2f, max_tokens=%d)", model_id, temperature, max_tokens)
        model_instance = ChatOpenAI(
            model=model_id,
            temperature=temperature,
            max_tokens=max_tokens
        )
        _model_cache[cache_key] = model_instance
        logger.info("Model loaded and cached: %s", model_id)
        return model_instance


def get_ai_response(
    model: ChatOpenAI,
    system_prompt: str,
    user_prompt: str,
    template: PromptTemplate = default_prompt_template
) -> dict:
    logger.debug("Invoking AI chain for prompt: %.80s...", user_prompt)
    chain = template | model | default_json_parser
    result = chain.invoke({'system_prompt': system_prompt, 'user_prompt': user_prompt})
    logger.debug("AI chain completed successfully")
    return result

