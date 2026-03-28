from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class AIResponse(BaseModel):
    response: str = Field(description="Direct answer to the user's question")
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    category: str = Field(description="Category of the inquiry (e.g., billing, technical, general)")
    action: str = Field(description="Recommended action for the support rep")


default_json_parser: JsonOutputParser = JsonOutputParser(pydantic_object=AIResponse)

