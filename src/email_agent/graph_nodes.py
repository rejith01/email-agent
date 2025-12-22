from email_agent.state import EmailState
from email_agent.prompts import EMAIL_CLASSIFICATION_PROMPT
from email_agent.llm import get_llm
from email_agent.router import route_email
from email_agent.executor import execute_action

import logging

logger = logging.getLogger("email_agent")
logging.basicConfig(level=logging.INFO)


VALID_CATEGORIES = {"request", "information", "urgent", "spam"}
VALID_ACTIONS = {"reply", "ignore", "escalate"}


def classify_node(state: EmailState) -> EmailState:
    logger.info(
        "Classifying email",
        extra={"sender": state["sender"], "subject": state["subject"]},
    )

    llm = get_llm()
    prompt = EMAIL_CLASSIFICATION_PROMPT.format(
        subject=state["subject"],
        body=state["body"],
    )

    result = llm.invoke(prompt)
    category = result.content.strip().lower()

    logger.info("Classification result", extra={"category": category})

    state["category"] = category
    return state


def route_node(state: EmailState) -> EmailState:
    category = state.get("category")

    logger.info(
        "Routing email",
        extra={"category": category},
    )

    if category not in VALID_CATEGORIES:
        logger.error(
            "Invalid category from classifier",
            extra={"category": category},
        )
        raise ValueError(f"Invalid category produced by classifier: {category}")

    if category == "urgent":
        action = "escalate"
    elif category == "spam":
        action = "ignore"
    else:
        action = "reply"

    if action not in VALID_ACTIONS:
        logger.error(
            "Invalid action derived",
            extra={"action": action},
        )
        raise ValueError(f"Invalid action derived: {action}")

    logger.info(
        "Routing decision",
        extra={"action": action},
    )

    state["action"] = action
    return state


def execute_node(state: EmailState) -> EmailState:
    logger.info(
        "Executing action",
        extra={"action": state["action"]},
    )

    result = execute_action(
        action=state["action"],
        sender=state["sender"],
        subject=state["subject"],
        body=state["body"],
    )

    logger.info(
        "Action executed",
        extra={
            "action": state["action"],
            "response_length": len(result.get("response", "") or ""),
        },
    )

    state["response"] = result["response"]
    return state


def reply_node(state: EmailState) -> EmailState:
    return state


def ignore_node(state: EmailState) -> EmailState:
    logger.info(
        "Email ignored",
        extra={"category": state.get("category")},
    )

    state["response"] = None
    return state



def escalate_node(state: EmailState) -> EmailState:
    logger.warning(
        "Email escalated to human operator",
        extra={
            "sender": state.get("sender"),
            "subject": state.get("subject"),
        },
    )

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