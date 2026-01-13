import resend
import os
from typing import Dict
from agents import Agent, function_tool


resend.api_key = os.getenv("RESEND_API_KEY")

@function_tool
def send_email(subject:str, html_body:str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body """
    
    # Initialize the API key
    resend.api_key = os.environ.get("RESEND_API_KEY")

    try:
        params = {
            "from": "onboarding@resend.dev",  # See note below about this address
            "to": "shyamksec@gmail.com",      # Your recipient
            "subject": subject,
            "html": html_body,
        }

        email = resend.Emails.send(params)
        
        return {
            "status": "success", 
            "id": email.get("id")
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }
    

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)