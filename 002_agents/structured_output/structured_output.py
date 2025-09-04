from pydantic import BaseModel, Field
from typing import Optional, List
from strands import Agent
from my_env import model_id

class WeatherForecast(BaseModel):
    """Complete weather forecast information."""
    location: str = Field(description="The location for this forecast")
    current_time: str = Field(description="Current time in HH:MM format")
    current_weather: str = Field(description="Current weather conditions")
    temperature: Optional[float] = Field(default=None, description="Temperature in Celsius")
    forecast_days: List[str] = Field(default_factory=list, description="Multi-day forecast")
    
agent = Agent(model=model_id)

result = agent.structured_output(WeatherForecast, "What's the weather like in Brisbane today?")

print(result)

