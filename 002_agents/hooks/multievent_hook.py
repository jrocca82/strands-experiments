from strands.hooks import HookProvider, HookRegistry, BeforeInvocationEvent, AfterInvocationEvent
from strands.agent import Agent
from my_env import model_id

# Other hooks for reference -- experimental
# from strands.experimental.hooks import AfterModelInvocationEvent, AfterToolInvocationEvent, BeforeModelInvocationEvent, BeforeToolInvocationEvent

class LoggingHook(HookProvider):
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.log_start)
        registry.add_callback(AfterInvocationEvent, self.log_end)

    def log_start(self, event: BeforeInvocationEvent) -> None:
        print(f"Request started for agent: {event.agent.name}")

    def log_end(self, event: AfterInvocationEvent) -> None:
        print(f"\nRequest completed for agent: {event.agent.name}")

# Passed in via the hooks parameter
agent = Agent(hooks=[LoggingHook()], model=model_id)

agent("Hello!")