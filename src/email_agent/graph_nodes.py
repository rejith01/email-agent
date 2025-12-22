from email_agent.state import EmailState
from email_agent.prompts import EMAIL_CLASSIFICATION_PROMPT
from email_agent.llm import get_llm
from email_agent.router import route_email
from email_agent.executor import execute_action

VALID_CATEGORIES = {"request", "information", "urgent", "spam"}
VALID_ACTIONS = {"reply", "ignore", "escalate"}


def classify_node(state: EmailState) -> EmailState:
    llm = get_llm()
    prompt = EMAIL_CLASSIFICATION_PROMPT.format(
        subject=state["subject"],
        body=state["body"]
    )
    response = llm.invoke(prompt)
    state["category"] = response.content.strip().lower()
    return state

def route_node(state: EmailState) -> EmailState:
    action = route_email(state["category"])
    state["action"] = action
    return state

def execute_node(state: EmailState) -> EmailState:
    result = execute_action(
        action=state["action"],
        sender=state["sender"],
        subject=state["subject"],
        body=state["body"],
    )

    state["response"] = result["response"]
    return state

def reply_node(state: EmailState) -> EmailState:
    return state


def ignore_node(state: EmailState) -> EmailState:
    state["response"] = None
    return state


def escalate_node(state: EmailState) -> EmailState:
    state["response"] = "Escalated to human operator."
    return state

def decide_next_node(state: EmailState) -> str:
    action = state["action"]

    if action == "reply":
        return "reply"
    if action == "ignore":
        return "ignore"
    if action == "escalate":
        return "escalate"

    return "ignore"