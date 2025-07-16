from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .gmail_utility import authenticate_gmail, create_message, create_draft

# from agentops import record_tool

import os


class GmailToolInput(BaseModel):
    body: str


# @record_tool("This is used for gmail draft emails.")
class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str) -> str:
        try:
            service = authenticate_gmail()

            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            subject = "Memecoin Report"
            message_text = body

            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            draft = create_draft(service, "me", message)
            if draft is None:
                return "Error: Failed to create draft email."
            return f"Email sent successfully! Draft id: {draft['id']}"

        except Exception as e:
            return f"Error sending email: {e}"
