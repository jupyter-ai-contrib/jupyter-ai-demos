from jupyter_ai.personas.base_persona import BasePersona, PersonaDefaults
from jupyterlab_chat.models import Message

from claude_code_sdk import (
    query, ClaudeCodeOptions,
    Message, SystemMessage, AssistantMessage, ResultMessage,
    TextBlock, ToolUseBlock
)

omit_input_args = ['content']

def input_dict_to_str(d: dict):
    args = []
    for k, v in d.items():
        if k not in omit_input_args:
            args.append(f"{k}={v}")
    return ', '.join(args)

def tool_to_str(block: ToolUseBlock):
    results = []
    if block.name == 'TodoWrite':
        todos = block.input.get('todos')
        for todo in todos:
            content = todo.get('content')
            if content:
                results.append(f"* {content}")
    else:
        results.append(f"🛠️ {block.name}({input_dict_to_str(block.input)})")
    return '\n'.join(results)


def claude_message_to_str(message):
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

    @property
    def defaults(self):
        return PersonaDefaults(
            name="Claude",
            avatar_path="/api/ai/static/jupyternaut.svg",
            description="Claude Code",
            system_prompt="...",
        )
    
    async def process_message(self, message: Message):
        try:
            async_gen = query(
                prompt=message.body,
                options=ClaudeCodeOptions(
                    max_turns=20,
                    cwd=self.get_chat_dir(),
                    permission_mode='bypassPermissions'
                )
            )
            async for response_message in async_gen:
                if isinstance(response_message, AssistantMessage):
                    msg_str = claude_message_to_str(response_message)
                    if msg_str is not None:
                        self.send_message(msg_str)
                else:
                    pass
                    # self.send_message(str(response_message))
        except Exception as e:
            print(f"Error in process_message: {e}")
            self.send_message(f"Sorry, I have had an internal error while working on that: {e}")
        finally:
            if 'async_gen' in locals():
                await async_gen.aclose()
