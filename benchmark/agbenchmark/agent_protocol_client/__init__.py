# coding: utf-8

import importlib

spec = """
Agent Communication Protocol

Specification of the API protocol for communication with an agent.

The version of the OpenAPI document: v0.2
"""

__all__ = [
    "AgentApi",
    "ApiClient",
    "ApiResponse",
    "Configuration",
    "Artifact",
    "Step",
    "StepAllOf",
    "StepRequestBody",
    "Task",
    "TaskAllOf",
    "TaskRequestBody",
]

for name in __all__:
    module = importlib.import_module(f"agbenchmark.agent_protocol_client.api.{name[:1].lower()}{name[1:]}")
    globals()[name] = getattr(module, name)

__version__ = "1.0.0"
__spec__ = spec
