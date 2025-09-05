# NOTE: cannot install llm_guard

from strands import Agent
from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from langfuse import Langfuse, observe

vault = Vault()

def create_anonymize_scanner():
    """Creates a reusable anonymize scanner."""
    return Anonymize(vault, recognizer_conf=BERT_LARGE_NER_CONF, language="en")

def masking_function(data, **kwargs):
    """Langfuse masking function to recursively redact PII."""
    if isinstance(data, str):
        scanner = create_anonymize_scanner()
        sanitized_data, _, _ = scanner.scan(data)
        return sanitized_data
    elif isinstance(data, dict):
        return {k: masking_function(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [masking_function(item) for item in data]
    return data

langfuse = Langfuse(mask=masking_function)


class CustomerSupportAgent:
    def __init__(self):
        self.agent = Agent(
            system_prompt="You are a helpful customer service agent. Respond professionally to customer inquiries."
        )

    @observe
    def process_sanitized_message(self, sanitized_payload):
        """Processes a pre-sanitized payload and expects sanitized input."""
        sanitized_content = sanitized_payload.get("prompt", "empty input")

        conversation = f"Customer: {sanitized_content}"

        response = self.agent(conversation)
        return response


def process():
    support_agent = CustomerSupportAgent()
    scanner = create_anonymize_scanner()

    raw_payload = {
        "prompt": "Hi, I'm Jonny Test. My phone number is 123-456-7890 and my email is john@example.com. I need help with my order #123456789."
    }

    sanitized_prompt, _, _ = scanner.scan(raw_payload["prompt"])
    sanitized_payload = {"prompt": sanitized_prompt}

    response = support_agent.process_sanitized_message(sanitized_payload)

    print(f"Response: {response}")
    langfuse.flush()

    #Example input: prompt:
        # "Hi, I'm [REDACTED_PERSON_1]. My phone number is [REDACTED_PHONE_NUMBER_1] and my email is [REDACTED_EMAIL_ADDRESS_1]. I need help with my order #123456789."
    #Example output: 
        # #Hello! I'd be happy to help you with your order #123456789. 
        # To better assist you, could you please let me know what specific issue you're experiencing with this order? For example:
        # - Are you looking for a status update?
        # - Need to make changes to the order?
        # - Having delivery issues?
        # - Need to process a return or exchange?
        # 
        # Once I understand what you need help with, I'll be able to provide you with the most relevant assistance."

if __name__ == "__main__":
    process()