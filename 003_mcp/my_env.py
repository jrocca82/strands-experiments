from dotenv import load_dotenv
import os

load_dotenv()

model_id = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")