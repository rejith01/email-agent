from langchain_openai import ChatOpenAI

def get_llm(model: str = "gpt-4o"):
    return ChatOpenAI(model=model)

