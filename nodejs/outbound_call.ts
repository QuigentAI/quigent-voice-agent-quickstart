/**
 * Quigent Voice AI - Outbound Call Dispatch Example (TypeScript)
 * Initiates an outbound conversational call with sub-380ms response speed.
 */

import * as dotenv from 'dotenv';
dotenv.config();

const API_KEY = process.env.QUIGENT_API_KEY;
const BASE_URL = process.env.QUIGENT_API_BASE_URL || 'https://api.quigent.com/v1';

if (!API_KEY || API_KEY === 'qgt_live_your_api_key_here') {
  console.error('[ERROR] Please set QUIGENT_API_KEY in your .env file.');
  process.exit(1);
}

interface DispatchOptions {
  toNumber: string;
  callerId?: string;
  agentId?: string;
  prospectName?: string;
  variables?: Record<string, string>;
}

async function dispatchVoiceCall(options: DispatchOptions) {
  const endpoint = `${BASE_URL}/calls/dispatch`;

  const payload = {
    to_number: options.toNumber,
    caller_id: options.callerId || '+911409876543',
    agent_id: options.agentId || 'enterprise_sales_qualifier',
    prompt_variables: {
      prospect_name: options.prospectName || 'Valued Customer',
      ...options.variables,
    },
    telephony_config: {
      carrier_route: 'airtel_iq_primary',
      record_audio: true,
    },
  };

  console.log(`[*] Dispatching Quigent Voice Agent to ${options.toNumber}...`);

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'User-Agent': 'quigent-node-quickstart/1.0',
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`[FAILED] API responded with status ${res.status}: ${errorText}`);
      return;
    }

    const data = await res.json();
    console.log(`[SUCCESS] Call queued successfully!`, data);
  } catch (err) {
    console.error(`[ERROR] Network error dispatching call:`, err);
  }
}

// Execute sample dispatch
dispatchVoiceCall({
  toNumber: '+919876543210',
  prospectName: 'Rahul Sharma',
  variables: {
    project_name: 'Sobha Windsor',
    budget: '1.5 Cr',
    micro_market: 'Whitefield, Bengaluru',
  },
});
