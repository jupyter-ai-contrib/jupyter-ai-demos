from typing import Dict, Any, List, Optional, AsyncIterator

from jupyter_ai.personas.base_persona import BasePersona, PersonaDefaults
from jupyterlab_chat.models import Message

from claude_code_sdk import (
    query, ClaudeCodeOptions,
    Message, SystemMessage, AssistantMessage, ResultMessage,
    TextBlock, ToolUseBlock
)


OMIT_INPUT_ARGS = ['content']

TOOL_PARAM_MAPPING = {
    'Task': 'description',
    'Bash': 'command',
    'Glob': 'pattern',
    'Grep': 'pattern',
    'LS': 'path',
    'Read': 'file_path',
    'Edit': 'file_path',
    'MultiEdit': 'file_path',
    'Write': 'file_path',
    'NotebookRead': 'notebook_path',
    'NotebookWrite': 'notebook_path',
    'WebFetch': 'url',
    'WebSearch': 'query',
}


def input_dict_to_str(d: Dict[str, Any]) -> str:
    """Convert input dictionary to string representation, omitting specified args."""
    args = []
    for k, v in d.items():
        if k not in OMIT_INPUT_ARGS:
            args.append(f"{k}={v}")
    return ', '.join(args)


def tool_to_str(block: ToolUseBlock) -> str:
    """Convert a ToolUseBlock to its string representation."""
    results = []
    
    if block.name == 'TodoWrite':
        todos = block.input.get('todos', [])
        results.append('TodoWrite()')
        for todo in todos:
            content = todo.get('content')
            if content:
                results.append(f"* {content}")
    elif block.name in TOOL_PARAM_MAPPING:
        param_key = TOOL_PARAM_MAPPING[block.name]
        param_value = block.input.get(param_key, '')
        results.append(f"🛠️ {block.name}({param_value})")
    else:
        results.append(f"🛠️ {block.name}({input_dict_to_str(block.input)})")
    
    return '\n'.join(results)


def claude_message_to_str(message) -> Optional[str]:
    """Convert a Claude Message to a string by extracting text content."""
    text_parts = []
    for block in message.content:
        if isinstance(block, TextBlock):
            text_parts.append(block.text)
        elif isinstance(block, ToolUseBlock):
            text_parts.append(tool_to_str(block))
        else:
            text_parts.append(str(block))
    return '\n'.join(text_parts) if text_parts else None


class ClaudeCodePersona(BasePersona):
    """Claude Code persona for Jupyter AI integration."""

    @property
    def defaults(self) -> PersonaDefaults:
        """Return default configuration for the Claude Code persona."""
        return PersonaDefaults(
            name="Claude",
            avatar_path="/files/.jupyter/claude.svg",
            description="Claude Code",
            system_prompt="...",
        )
    
    async def _process_response_message(self, message_iterator) -> AsyncIterator[str]:
        """Process response messages from Claude Code SDK."""
        async for response_message in message_iterator:
            self.log.info(str(response_message))
            if isinstance(response_message, AssistantMessage):
                msg_str = claude_message_to_str(response_message)
                if msg_str is not None:
                    yield msg_str + '\n\n'
    
    async def process_message(self, message: Message) -> None:
        """Process incoming message and stream Claude Code response."""
        async_gen = None
        try:
            async_gen = query(
                prompt=message.body,
                options=ClaudeCodeOptions(
                    max_turns=20,
                    cwd=self.get_chat_dir(),
                    permission_mode='bypassPermissions'
                )
            )
            await self.stream_message(self._process_response_message(async_gen))
        except Exception as e:
            self.log.error(f"Error in process_message: {e}")
            await self.send_message(f"Sorry, I have had an internal error while working on that: {e}")
        finally:
            if async_gen is not None:
                await async_gen.aclose()
