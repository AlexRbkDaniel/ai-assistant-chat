"""
Utility scripts for manually testing the AI connection.
Run from the project root:
    python -m scripts.sanity_check
"""
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

from shared.openai_wrapper import load_model, get_ai_response


def test_connection():
    model = load_model()
    from langchain_core.prompts import PromptTemplate
    prompt_template = PromptTemplate.from_template("Only reply with the answer. {question}")
    text = prompt_template.format(question="What is the capital of France?")
    print("Response:", model.invoke(text).content)


def sanity_check():
    llm = load_model()
    system_prompt = "You are a helpful football assistant, specialized on Premier League and LaLiga football."
    user_prompt = "Who won the 1998 World Cup?"
    response = get_ai_response(llm, system_prompt, user_prompt)
    print("AI response:", response)


if __name__ == "__main__":
    sanity_check()

