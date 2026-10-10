"""
Quigent Voice AI - Outbound Call Dispatch Example
Demonstrates triggering a sub-380ms real-time conversational voice call via Quigent API.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("QUIGENT_API_KEY")
BASE_URL = os.getenv("QUIGENT_API_BASE_URL", "https://api.quigent.com/v1")

if not API_KEY or API_KEY == "qgt_live_your_api_key_here":
    print("[ERROR] Please set your QUIGENT_API_KEY in the .env file.")
    sys.exit(1)


def dispatch_voice_call(
    to_number: str,
    agent_id: str = "enterprise_sales_qualifier",
    prospect_name: str = "Valued Customer",
    custom_variables: dict = None,
):
    """
    Dispatches an outbound AI call to a prospect's phone number.
    """
    endpoint = f"{BASE_URL}/calls/dispatch"

    payload = {
        "to_number": to_number,
        "caller_id": "+911409876543",  # Registered 140 / 160 series CLI
        "agent_id": agent_id,
        "prompt_variables": {
            "prospect_name": prospect_name,
            **(custom_variables or {}),
        },
        "telephony_config": {
            "carrier_route": "airtel_iq_primary",
            "max_duration_seconds": 600,
            "record_audio": True,
        },
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "quigent-python-quickstart/1.0",
    }

    print(f"[*] Dispatching AI voice agent to {to_number}...")
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code in (200, 201):
        data = response.json()
        print(f"[SUCCESS] Call queued successfully! Call ID: {data.get('call_id')}")
        return data
    else:
        print(f"[FAILED] Error {response.status_code}: {response.text}")
        return None


if __name__ == "__main__":
    # Example test dispatch (replace with real recipient phone number)
    test_number = "+919876543210"
    dispatch_voice_call(
        to_number=test_number,
        prospect_name="Rahul Sharma",
        custom_variables={
            "project_name": "Sobha Windsor",
            "micro_market": "Whitefield, Bengaluru",
            "budget": "1.5 Cr",
        },
    )
