"""
Shared utilities for the AI Agents course notebooks.
Import with: import sys; sys.path.insert(0, '..'); from shared.utils import *
"""

import os
import json
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionMessageToolCallUnion

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def print_tool_call(tool_call: ChatCompletionMessageToolCallUnion):
    """Pretty-print a tool call from the OpenAI response."""
    args = json.loads(tool_call.function.arguments)
    print(f"  Function tool: {tool_call.function.name} Args: {json.dumps(args, indent=4)}")


def print_messages(messages: List[ChatCompletionMessage | ChatCompletionMessageParam]):
    print("Full conversation (what the model 'sees' on each call):")
    print()
    for i, m in enumerate(messages):
        role = m["role"].upper()
        if m["content"] is not None:
            content = m["content"]
        elif m["tool_calls"] is not None:
            tool_call: ChatCompletionMessageToolCallUnion = m["tool_call"]
            args = json.loads(tool_call.function.arguments)
            content = f"Function tool: {tool_call.function.name} Args: {json.dumps(args, indent=4)}"
        else:
            content = "Unexpected"
        content = str(content)
        if len(content) > 200:
            content = content[:200] + "..."
        print(f"{i}. [{role}] {content}")


def to_param(m: ChatCompletionMessage) -> ChatCompletionMessageParam:
    """
    Normalizes model responses into model params to be combined uniformly in conversation lists
    
    We drop fields that only appear in responses, never used by the model in requests:
    - id
    - refusal
    - reasoning
    - audio
    - function_call (legacy)
    - tool_calls metadata details - if converted field by field for full consistency with Param
    - annotations (for some models)
    - model-specific metadata    
 """
    return {
        "role": m.role,
        "content": m.content,
        "tool_calls": m.tool_calls # type: ignore
    }

