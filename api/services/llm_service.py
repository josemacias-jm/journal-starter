import json
from datetime import UTC, datetime

import boto3

brt = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

async def analyze_journal_entry(entry_id: str, entry_text: str) -> dict:
    """Analyze a journal entry using Amazon Bedrock."""
    system_message = "You are a sentiment analyzer for journal entries. Always respond with valid JSON only."
    prompt = f"""Analyze the journal entry and return a JSON object with these exact keys:
    - entry_id: {entry_id}
    - sentiment: 'positive' | 'negative' | 'neutral'
    - summary: a 2 sentence summary of the entry
    - topics: a list of 2-4 key topics mentioned in the entry

    Journal Entry:
    {entry_text}"""

    response = brt.converse(
        modelId=model_id,
        system=[{"text": system_message}],
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={
            "maxTokens": 512,
            "temperature": 0.5
        }
    )

    response_text = response["output"]["message"]["content"][0]["text"]
    result = json.loads(response_text)
    result["created_at"] = datetime.now(UTC).isoformat()
    return result
