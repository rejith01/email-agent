from typing import TypedDict, Optional, Literal

class EmailState(TypedDict):
    # Original input
    sender: str
    subject: str
    body: str

    # Derived during execution
    category: Optional[Literal["request", "information", "urgent", "spam"]]
    action: Optional[Literal["reply", "ignore", "escalate"]]

    # Output
    response: Optional[str]