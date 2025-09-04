from pydantic import BaseModel
from strands import Agent
from my_env import model_id
from pathlib import Path

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    
script_dir = Path(__file__).resolve().parent
file_path = script_dir / "resume.pdf"


with open(file_path, "rb") as fp:
    document_bytes = fp.read()

agent = Agent(model=model_id)
result = agent.structured_output(
    PersonInfo,
    [
        {"text": "Please process this resume."},
        {
            "document": {
                "format": "pdf",
                "name": "application",
                "source": {
                    "bytes": document_bytes,
                },
            },
        },
    ]
)

print(result)