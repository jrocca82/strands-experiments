from typing import Any
from strands import Agent
from strands.hooks import HookProvider, HookRegistry
from strands.experimental.hooks import BeforeToolInvocationEvent, AfterToolInvocationEvent
from strands_tools import calculator
from my_env import model_id

class ConstantToolArguments(HookProvider):
    """Use constant argument values for specific parameters of a tool."""

    def __init__(self, fixed_tool_arguments: dict[str, dict[str, Any]]):
        """
        Initialize fixed parameter values for tools.

        Args:
            fixed_tool_arguments: A dictionary mapping tool names to dictionaries of 
                parameter names and their fixed values. These values will override any 
                values provided by the agent when the tool is invoked.
        """
        self._tools_to_fix = fixed_tool_arguments

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self._fix_tool_arguments)

    def _fix_tool_arguments(self, event: BeforeToolInvocationEvent):
        print(f"[HOOK] BeforeToolInvocationEvent fired for tool: {event.tool_use['name']}")
        print(f"[HOOK] Original tool input: {event.tool_use['input']}")

        if parameters_to_fix := self._tools_to_fix.get(event.tool_use["name"]):
            print(f"[HOOK] Applying fixed parameters: {parameters_to_fix}")
            tool_input: dict[str, Any] = event.tool_use["input"]
            tool_input.update(parameters_to_fix)
            print(f"[HOOK] Updated tool input: {tool_input}")
        else:
            print(f"[HOOK] No fixed parameters configured for tool: {event.tool_use['name']}")
            
class ToolInterceptor(HookProvider):
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self.intercept_tool)

    def intercept_tool(self, event: BeforeToolInvocationEvent) -> None:
        if event.tool_use.name == "sensitive_tool":
            # Replace with a safer alternative
            event.selected_tool = self.safe_alternative_tool
            event.tool_use["name"] = "safe_tool"
            
# class ResultProcessor(HookProvider):
#     def register_hooks(self, registry: HookRegistry) -> None:
#         registry.add_callback(AfterToolInvocationEvent, self.process_result)

#     def process_result(self, event: AfterToolInvocationEvent) -> None:
#         if event.tool_use.name == "calculator":
#             # Add formatting to calculator results
#             original_content = event.result["content"][0]["text"]
#             event.result["content"][0]["text"] = f"Result: {original_content}"
            
fix_parameters = ConstantToolArguments({
    "calculator": {
        "precision": 1,
    }
})

agent = Agent(tools=[calculator], hooks=[fix_parameters], model=model_id)
result = agent("What is 2.5 / 3?")