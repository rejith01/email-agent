from email_agent.prompts import EMAIL_REPLY_PROMPT
from email_agent.llm import get_llm


def execute_action(
    action: str,
    sender: str,
    subject: str,
    body: str,
):
    """
    Execute the action decided by the router.
    """
    llm = get_llm()

    if action == "reply":
        prompt = EMAIL_REPLY_PROMPT.format(
            sender=sender,
            subject=subject,
            body=body,
        )
        response = llm.invoke(prompt)
        return {
            "action": "reply",
            "response": response.content,
        }

    elif action == "acknowledge":
        return {
            "action": "acknowledge",
            "response": "Thank you for the information. We have noted this.",
        }

    elif action == "escalate":
        return {
            "action": "escalate",
            "response": "This email requires urgent human attention.",
        }

    elif action == "ignore":
        return {
            "action": "ignore",
            "response": None,
        }

    else:
        return {
            "action": "unknown",
            "response": None,
        }
