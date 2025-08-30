from typing import TypedDict

MAX_STEPS = 3
class AgentState(TypedDict):
    draft: str
    feedback: str
    final: str
    count: int  # track number of loops
    user_prompt: str