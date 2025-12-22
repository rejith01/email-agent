from langgraph.graph import StateGraph, END

from email_agent.state import EmailState
from email_agent.graph_nodes import (
    classify_node,
    route_node,
    execute_node,
    reply_node,
    ignore_node,
    escalate_node,
    decide_next_node,
)


def build_email_agent():
    graph = StateGraph(EmailState)

    # Nodes
    graph.add_node("classify", classify_node)
    graph.add_node("route", route_node)
    graph.add_node("reply", reply_node)
    graph.add_node("ignore", ignore_node)
    graph.add_node("escalate", escalate_node)
    graph.add_node("execute", execute_node)

    # Entry
    graph.set_entry_point("classify")

    # Linear edge
    graph.add_edge("classify", "route")

    # Conditional branching
    graph.add_conditional_edges(
        "route",
        decide_next_node,
        {
            "reply": "reply",
            "ignore": "ignore",
            "escalate": "escalate",
        },
    )

    # All actions flow to execution
    graph.add_edge("reply", "execute")
    graph.add_edge("ignore", "execute")
    graph.add_edge("escalate", "execute")

    # Termination
    graph.add_edge("execute", END)

    return graph.compile()