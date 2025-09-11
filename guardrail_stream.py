import asyncio
import json
from strands import Agent
from strands.models import BedrockModel
from my_env import model_id

# PII redaction guardrail version 2
PII_GUARDRAIL_ID = "5pshecbsd1zj"
GUARDRAIL_VERSION = "2"

bedrock_model = BedrockModel(
    model_id=model_id,
    guardrail_id=PII_GUARDRAIL_ID,
    guardrail_version=GUARDRAIL_VERSION,
    guardrail_trace="enabled",
    guardrail_redact_output=True,               # mask unsafe tokens mid-stream
    guardrail_redact_output_message="[REDACTED]",
)

agent = Agent(
    system_prompt="You are a helpful assistant.",
    model=bedrock_model,
)

async def stream_with_guardrail(agent, prompt: str):
    full = ""
    async for event in agent.stream_async(prompt):
        if "data" in event:
            chunk = event["data"]
            full += chunk
            # Print each chunk immediately with a small delay
            print(chunk, end="", flush=True)
            await asyncio.sleep(0.05)  # flush incrementally for visibility
        if event.get("stop_reason") == "guardrail_intervened":
            print("\n--- Stream redacted due to guardrail ---")
    return full

# Long prompt with multiple PII occurrences spaced out
prompt = (
    "Write a customer support email draft: "
    "Hello team, please contact alice@example.com for issue A, "
    "bob@example.com for issue B, "
    "and charlie@example.com for issue C. "
    "Also include dave@example.com and eve@example.com for follow-up. "
    "Make sure all responses are courteous and professional, "
    # "and do not use profanity like fuck or cunt."
)

asyncio.run(stream_with_guardrail(agent, prompt))

# Inspect the guardrail trace
trace = getattr(agent.model, "last_guardrail_trace", None)
if trace:
    print("\nGuardrail trace:", json.dumps(trace, indent=2))

# Show conversation history
print("\nConversation history:", json.dumps(agent.messages, indent=2))
