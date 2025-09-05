from dotenv import load_dotenv
import os

load_dotenv()

model_id = os.getenv("MODEL_ID", "anthropic.claude-3-5-sonnet-20240620")