from jupyter_ai.personas.base_persona import BasePersona, PersonaDefaults
from jupyterlab_chat.models import Message

from agno.agent import Agent
from agno.models.message import Message as AgnoMessage


async def transform_iterator(source_iterator):
    async for item in source_iterator:
        if item is not None:
            yield item.content.replace('$',r'\\$')


class _AgnoPersona(BasePersona):
    """
    The debug persona, the main persona provided by Jupyter AI.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = self.create_agent()

    @property
    def defaults(self):
        return PersonaDefaults(
            name="AgnoPersona",
            avatar_path="/api/ai/static/jupyternaut.svg",
            description="A Generic Agno Persona",
            system_prompt="...",
        )
 
    def create_agent(self) -> Agent:
        raise NotImplementedError("Please implement create_agent()")

    def get_role(self, ychat_message):
        if ychat_message.sender in self.parent.personas:
            return 'assistant'
        else:
            return 'user'

    async def process_message(self, message: Message):
        history = self.ychat.get_messages()[-4:]
        messages = [AgnoMessage(content=h.body, name=h.sender, role=self.get_role(h)) for h in history]
        stream = await self.agent.arun(
            message.body,
            user_id=message.sender,
            session_id=self.ychat.get_id(),
            messages=messages
        )
        await self.stream_message(transform_iterator(stream))

