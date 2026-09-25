import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class Evidence(BaseModel):
    text: str = Field(
        description="Evidence explicitly present in the user's input."
    )
    supports: str = Field(
        description="Requirement or factor supported by this evidence."
    )


class ReasoningLink(BaseModel):
    from_: str = Field(
        alias="from",
        description="Starting evidence or requirement."
    )
    to: str = Field(
        description="Decision or intermediate requirement."
    )
    reason: str = Field(
        description="Short explanation of the relationship."
    )


class DecisionTraceResult(BaseModel):
    decision: str
    evidence: list[Evidence]
    assumptions: list[str]
    reasoning_links: list[ReasoningLink]
    gaps: list[str]


SYSTEM_INSTRUCTION = """
You are DecisionTrace, an AI decision analysis system.

Analyze ONLY the information provided by the user.

Identify:

1. The primary decision.
2. Evidence explicitly present in the input.
3. Assumptions that appear necessary but are not explicitly stated.
4. Reasoning connections between evidence, requirements, and the decision.
5. Potential missing evidence.

Rules:

- Never invent evidence.
- Evidence must be grounded in the user's input.
- Clearly distinguish assumptions from evidence.
- Do not treat assumptions as verified facts.
- Do not claim that a gap invalidates the decision.
- Use neutral wording for potential gaps.
- If multiple decisions exist, represent them clearly.
"""


def analyze_decision(text: str) -> DecisionTraceResult:

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=[
            {
                "type": "text",
                "text": SYSTEM_INSTRUCTION
            },
            {
                "type": "text",
                "text": text
            }
        ],
        response_format=[
            {
                "type": "text",
                "mime_type": "application/json",
                "schema": DecisionTraceResult.model_json_schema(),
            }
        ],
    )

    return DecisionTraceResult.model_validate_json(
        interaction.output_text
    )   