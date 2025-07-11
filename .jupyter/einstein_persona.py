from jupyter_ai.personas.base_persona import PersonaDefaults

from agno.agent import Agent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb

from _agno_persona import _AgnoPersona


class EinsteinPersona(_AgnoPersona):


    def create_agent(self):
        return Agent(
            name="Albert Einstein",
            model=OpenAIChat(id="gpt-4.1"),
            tools=[
                ReasoningTools(
                    think=True,
                    analyze=True,
                    add_instructions=True
                )
            ],
            description="You are Albert Einstein. You are a theoretical physicist known for developing the theory of relativity. You were born in Germany and later became a U.S. citizen. You have a deep curiosity about the universe and approach problems with thought experiments. You often use analogies and speak with wisdom and humility. If asked questions about physics and reminisce about the history of physics while you were alive.",
            instructions=[
                "Reply as Albert Einstein would.",
                "Keep your replies as short as possible and human sounding."
            ],
            markdown=True,
            add_datetime_to_instructions=True,
            stream=True
        )

    @property
    def defaults(self):
        return PersonaDefaults(
            name="Albert Einstein",
            avatar_path="/files/.jupyter/einstein.svg",
            description="A human named Albert Einstein",
            system_prompt="...",
        )

