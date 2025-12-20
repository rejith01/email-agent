from langchain_core.prompts import PromptTemplate

EMAIL_REPLY_PROMPT = PromptTemplate(
    input_variables=["sender", "subject", "body"],
    template="""
You are an email assistant.

Sender: {sender}
Subject: {subject}

Email Body:
{body}

Task:
Write a short professional reply.
"""
)

