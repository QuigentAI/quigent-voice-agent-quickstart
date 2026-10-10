/**
 * Quigent Voice AI - Webhook Server (Express.js)
 * Listens for live call transcripts, tool execution requests, and triggers downstream automations.
 */

import express, { Request, Response } from 'express';
import * as dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 8000;

app.post('/api/quigent/webhook', (req: Request, res: Response) => {
  const { event, call_id, to_number, duration_seconds, qualification, audio_recording_url } = req.body;

  console.log(`\n[EVENT RECEIVED] Type: ${event} | Call ID: ${call_id}`);

  switch (event) {
    case 'call.started':
      console.log(`[*] Call initiated with recipient: ${to_number}`);
      return res.status(200).json({ status: 'ok' });

    case 'call.function_call': {
      const { tool_name, arguments: toolArgs } = req.body;
      console.log(`[*] Live function execution: ${tool_name}`, toolArgs);
      return res.status(200).json({ status: 'success', result: 'Site visit locked for Saturday 11 AM' });
    }

    case 'call.ended':
      console.log(`[COMPLETED] Duration: ${duration_seconds}s | Qualified: ${qualification?.qualified}`);
      console.log(`[RECORDING] Audio URL: ${audio_recording_url}`);

      // Omnichannel action: Send WhatsApp brochure if qualified
      if (qualification?.qualified) {
        console.log(`[*] Dispatching WhatsApp brochure to ${to_number}...`);
      }

      return res.status(200).json({ status: 'processed' });

    default:
      return res.status(200).json({ status: 'ignored' });
  }
});

app.listen(PORT, () => {
  console.log(`[*] Quigent Webhook Server running on http://localhost:${PORT}`);
});
