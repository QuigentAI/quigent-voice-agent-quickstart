"""
Quigent Voice AI - Function Calling & Tool Definition Example
Shows how to define structured tools that the AI voice agent can invoke during a live telephone call.
"""

# Example JSON schema for custom tools attached to an agent
SITE_VISIT_SCHEDULER_TOOL = {
    "type": "function",
    "function": {
        "name": "schedule_site_visit",
        "description": "Books a property site visit slot in the CRM calendar and sends a WhatsApp confirmation.",
        "parameters": {
            "type": "object",
            "properties": {
                "prospect_name": {
                    "type": "string",
                    "description": "Full name of the prospect.",
                },
                "project_name": {
                    "type": "string",
                    "description": "Name of the real estate project enquired about.",
                },
                "preferred_date": {
                    "type": "string",
                    "description": "Preferred date for the visit in YYYY-MM-DD format.",
                },
                "preferred_time_slot": {
                    "type": "string",
                    "enum": ["10:00 AM", "12:00 PM", "03:00 PM", "05:00 PM"],
                    "description": "Selected time slot.",
                },
                "send_whatsapp_location": {
                    "type": "boolean",
                    "description": "Whether to send the Google Maps location pin via WhatsApp.",
                },
            },
            "required": [
                "prospect_name",
                "project_name",
                "preferred_date",
                "preferred_time_slot",
            ],
        },
    },
}

CRM_RECORD_UPDATE_TOOL = {
    "type": "function",
    "function": {
        "name": "update_crm_lead_stage",
        "description": "Updates the lead qualification stage and notes in LeadSquared or Zoho CRM.",
        "parameters": {
            "type": "object",
            "properties": {
                "lead_id": {
                    "type": "string",
                    "description": "Unique identifier of the lead in CRM.",
                },
                "qualification_status": {
                    "type": "string",
                    "enum": ["HOT", "WARM", "COLD", "NOT_INTERESTED", "CALLBACK_REQUESTED"],
                },
                "budget_bracket": {
                    "type": "string",
                    "description": "Confirmed budget bracket (e.g., 1.5 Cr - 2.0 Cr).",
                },
                "possession_timeline": {
                    "type": "string",
                    "description": "Ready to move vs Under Construction.",
                },
            },
            "required": ["lead_id", "qualification_status"],
        },
    },
}


def register_agent_tools():
    """
    Returns list of tools to pass into the Quigent Agent configuration.
    """
    return [SITE_VISIT_SCHEDULER_TOOL, CRM_RECORD_UPDATE_TOOL]


if __name__ == "__main__":
    tools = register_agent_tools()
    print(f"[*] Defined {len(tools)} enterprise tools for Quigent Voice AI agents.")
