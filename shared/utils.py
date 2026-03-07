"""
Shared utilities for the AI Agents course notebooks.
Import with: import sys; sys.path.insert(0, '..'); from shared.utils import *
"""

import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def print_tool_call(tool_call):
    """Pretty-print a tool call from the OpenAI response."""
    print(f"  Tool: {tool_call.function.name}")
    args = json.loads(tool_call.function.arguments)
    print(f"  Args: {json.dumps(args, indent=4)}")


def print_messages(messages):
    """Print a message list in a readable format."""
    for m in messages:
        role = m.get("role", "?").upper()
        content = m.get("content") or ""
        if len(content) > 300:
            content = content[:300] + "..."
        print(f"[{role}] {content}")
