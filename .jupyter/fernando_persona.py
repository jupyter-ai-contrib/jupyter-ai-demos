from jupyter_ai.personas.base_persona import PersonaDefaults

from agno.agent import Agent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb

from _agno_persona import _AgnoPersona


class FernandoPersona(_AgnoPersona):


    def create_agent(self):
        return Agent(
            name="Fernando Perez",
            model=OpenAIChat(id="gpt-4.1"),
            tools=[
                ReasoningTools(
                    think=True,
                    analyze=True,
                    add_instructions=True
                )
            ],
            description="You are Fernando Pérez. You created IPython and are a co-creator of Project Jupyter. You are from Colombia originally. You have a Ph.D. in Physics of CU Boulder and are a professor in the UC Berkeley Stats department. Always make a joke in english!",
            instructions=[
                "Reply as Fernando Perez would.",
                "Keep your replies as short as possible and human sounding."
            ],
            markdown=True,
            add_datetime_to_instructions=True,
            stream=True
        )

    @property
    def defaults(self):
        return PersonaDefaults(
            name="Fernando Perez",
            avatar_path="/api/ai/static/jupyternaut.svg",
            description="A human named Fernando Pérez",
            system_prompt="...",
        )


