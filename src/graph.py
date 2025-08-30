from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.nodes import draft_node, reflect_node, revise_node, feedback_condition
from src.schema import AgentState

graph = StateGraph(AgentState)

graph.add_node("draft", draft_node)
graph.add_node("reflect", reflect_node)
graph.add_node("revise", revise_node)

# Flow: START -> draft -> reflect
graph.add_edge(START, "draft")
graph.add_edge("draft", "reflect")

graph.add_conditional_edges(
    "reflect", feedback_condition, {"revise": "revise", "end": END}
)

# After revise, always loop back to reflect
graph.add_edge("revise", "reflect")

reflection_app = graph.compile()