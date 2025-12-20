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

EMAIL_CLASSIFICATION_PROMPT = PromptTemplate(
    input_variables=["subject", "body"],
    template="""
You are an email classification assistant.

Email Subject:
{subject}

Email Body:
{body}

Task:
Classify this email into ONE of the following categories:
- request
- information
- urgent
- spam

Return ONLY the category name.
"""
)

