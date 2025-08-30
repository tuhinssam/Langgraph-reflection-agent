from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.schema import AgentState, MAX_STEPS

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

def draft_node(state: AgentState) -> AgentState:
    # Imagine this is an LLM generating an initial draft
    prompt = f"Write a concise answer to this question:\n{state['user_prompt']}"
    response = llm.invoke([HumanMessage(content=prompt)])
    state["draft"] = response.content
    print(f"Initial Draft:\n {state['draft']}\n")
    print(f"=================================\n")
    state["count"] = 0
    return state

# ---- Reflect Node ----
def reflect_node(state: AgentState) -> AgentState:
    # Simulates self-critique (LLM reflection)
    prompt = f"""
    You are reviewing the following text for errors, clarity, and completeness:
    Draft: {state['draft']}
    Provide a short critique of issues, if any, or say 'Looks good.'
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    state["feedback"] = response.content
    print(f"\nFeedback: \n{state["feedback"]}\n")
    print(f"=================================\n")
    return state

# ---- Revise Node ----
def revise_node(state: AgentState) -> AgentState:
    # Apply reflection feedback
    prompt = f"""
    Revise the following draft based on the feedback:
    Draft: {state['draft']}
    Feedback: {state['feedback']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    state["draft"] = response.content
    state["final"] = response.content
    print(f"\nIteration: {state['count']}\n")
    print(f"\nUpdated after Feedback:\n{state["draft"]}\n")
    print(f"=================================\n")
    state["count"] += 1  # increment loop counter

    return state

# Conditional edges after reflect
def feedback_condition(state: AgentState) -> str:
    if state["feedback"] == "Looks good.":
        return "end"
    elif state.get("count", 0) >= MAX_STEPS:
        return "end"
    else:
        return "revise"
