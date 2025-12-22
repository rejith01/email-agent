from email_agent.graph import build_email_agent
from dotenv import load_dotenv

load_dotenv()

def main():
    app = build_email_agent()

    result = app.invoke(
        {
            "sender": "user@example.com",
            "subject": "System down",
            "body": "The service is unavailable. Please fix ASAP.",
        }
    )

    print("\nFINAL RESPONSE:")
    print(result["response"])

if __name__ == "__main__":
    main()