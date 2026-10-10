"""
Quigent Voice AI - Webhook Listener Server (FastAPI)
Listens for real-time call lifecycle events, CRM updates, and triggers automated WhatsApp follow-ups.
"""

import os
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Quigent Webhook Server",
    description="Enterprise webhook endpoint for receiving Quigent Voice AI events",
    version="1.0.0",
)

WEBHOOK_SECRET = os.getenv("QUIGENT_WEBHOOK_SECRET", "")


class TranscriptItem(BaseModel):
    role: str
    text: str


class CallEndedPayload(BaseModel):
    event: str
    call_id: str
    direction: str
    from_number: str
    to_number: str
    duration_seconds: int
    status: str
    qualification: Optional[Dict[str, Any]] = None
    transcript: Optional[List[TranscriptItem]] = None
    audio_recording_url: Optional[str] = None


@app.post("/api/quigent/webhook")
async def handle_quigent_webhook(
    request: Request,
    x_quigent_signature: Optional[str] = Header(None),
):
    """
    Primary webhook endpoint to process live Quigent events.
    """
    raw_body = await request.json()
    event_type = raw_body.get("event")

    print(f"\n[EVENT RECEIVED] Type: {event_type} | Call ID: {raw_body.get('call_id')}")

    if event_type == "call.started":
        # Handle call initialization (e.g. log in CRM)
        print(f"[*] Call started with recipient: {raw_body.get('to_number')}")
        return {"status": "ok"}

    elif event_type == "call.function_call":
        # Handle live in-call tool execution
        tool_name = raw_body.get("tool_name")
        args = raw_body.get("arguments", {})
        print(f"[*] Live tool execution: {tool_name}({args})")
        # Example response back to the voice agent
        return {"status": "success", "result": "Slot confirmed for Saturday 11:00 AM"}

    elif event_type == "call.ended":
        # Process completed conversation
        qualification = raw_body.get("qualification", {})
        to_number = raw_body.get("to_number")
        duration = raw_body.get("duration_seconds")
        audio_url = raw_body.get("audio_recording_url")

        print(f"[COMPLETED] Duration: {duration}s | Qualified: {qualification.get('qualified')}")
        print(f"[RECORDING] Audio URL: {audio_url}")

        # Trigger Omnichannel Follow-up (e.g., WhatsApp brochure)
        if qualification.get("qualified"):
            trigger_whatsapp_followup(to_number, qualification)

        # Sync with Enterprise CRM (e.g. LeadSquared / Zoho)
        sync_to_crm(raw_body)

        return {"status": "processed"}

    return {"status": "ignored"}


def trigger_whatsapp_followup(phone_number: str, qualification_data: dict):
    """
    Mock function to send instant WhatsApp collateral to a qualified prospect.
    """
    print(f"[*] Triggering WhatsApp brochure to {phone_number}...")
    # In production, call WhatsApp Business API (e.g., via Gupshup, Twilio, or Meta Cloud API)


def sync_to_crm(call_data: dict):
    """
    Mock function to sync call transcripts and outcomes to LeadSquared or Zoho CRM.
    """
    print(f"[*] Syncing call {call_data.get('call_id')} to Enterprise CRM...")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"[*] Starting Quigent Webhook Listener on http://0.0.0.0:{port}")
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=port, reload=True)
