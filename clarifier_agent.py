from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are a helpful research assistant. Given a user's research query, generate exactly 4 clarifying questions that will help improve the quality of web searches and the final research report.

Your questions should:
- Be short and specific (one sentence each)
- Help narrow down the scope, timeframe, geography, or specific aspects of the topic
- Avoid yes/no questions when possible
- Focus on details that would make web searches more targeted and effective

Always return exactly 4 questions, no more, no less."""

class ClarifyingQuestions(BaseModel):
    questions: list[str] = Field(
        description="Exactly 4 clarifying questions to ask the user about their research query"
    )

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)
