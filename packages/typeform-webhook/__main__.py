#!/usr/bin/env python
import os
import sys
import json
import asyncio

# Add the virtual environment site-packages and shared directory to the Python path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.extend([
    os.path.join(dir_path, "virtualenv/lib/python3.11/site-packages"),
    os.path.join(dir_path, "../shared")  # Adjusted path to shared directory
])

from db_operations import get_db_pool, store_user_response, store_analysis_results
from analysis import get_anthropic_client, run_analysis

async def process_webhook(args):
    db_pool = None
    try:
        db_pool = await get_db_pool()
        anthropic_client = get_anthropic_client()
        
        # Parse incoming request body from Typeform
        data = json.loads(args.get('__ow_body', '{}'))
        
        form_response = data.get('form_response', {})
        form_response_id = form_response.get('token')
        answers = form_response.get('answers', [])
        hidden_fields = form_response.get('hidden', {})
        
        email = hidden_fields.get('email', '')
        name = hidden_fields.get('name', '')
        raw_responses = {a['field']['ref']: a.get('text', a.get('choice', {}).get('label', '')) for a in answers}
        
        # Store response in DB
        async with db_pool.acquire() as conn:
            await store_user_response(conn, form_response_id, email, name, raw_responses)
        
        # Process with Claude
        analysis = await run_analysis(anthropic_client, raw_responses)
        
        # Store analysis results
        async with db_pool.acquire() as conn:
            await store_analysis_results(conn, form_response_id, analysis)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "message": "Webhook processed successfully"})
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }
    finally:
        if db_pool:
            await db_pool.close()

# DigitalOcean Functions entry point
def main(args):
    return asyncio.run(process_webhook(args))
