"""
Creative Agent - Spezialisiert auf Content-Generierung und Design
"""

from typing import Any, List
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.agents.base_agent import BaseAgent
from cognitive_symphony.models import AgentCapability, AgentType, Task


class CreativeAgent(BaseAgent):
    """Agent für kreative Content-Generierung und Design"""

    def __init__(self, llm: Any):
        super().__init__(AgentType.CREATIVE, llm)

    def _initialize_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="Content Creation",
                description="Texterstellung, Copywriting, Storytelling",
                skill_level=0.93,
                success_rate=0.91,
            ),
            AgentCapability(
                name="Design Concepts",
                description="UI/UX Design, Branding, Visual Concepts",
                skill_level=0.87,
                success_rate=0.85,
            ),
            AgentCapability(
                name="Marketing Materials",
                description="Erstellen von Marketing-Content und Kampagnen",
                skill_level=0.9,
                success_rate=0.88,
            ),
            AgentCapability(
                name="Multi-Modal Creation",
                description="Text, Bild, Video-Konzepte",
                skill_level=0.85,
                success_rate=0.83,
            ),
        ]

    async def execute(self, task: Task) -> Any:
        """Führt kreative Aufgaben aus"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Creative Agent, ein Experte für kreative Inhalte.
                    
                    Fähigkeiten:
                    - Content Creation (Texte, Copywriting, Storytelling)
                    - Design-Konzepte (UI/UX, Branding, Visual Design)
                    - Marketing-Materialien und Kampagnen
                    - Multi-Modal Content (Text, Bild, Video)
                    - Brand Voice und Messaging
                    
                    Erstelle ansprechende, kreative Inhalte mit hoher Wirkung.
                    """,
                ),
                ("human", "Aufgabe: {task_description}\nKontext: {context}"),
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "task_description": task.description,
                "context": str(task.context),
            }
        )

        return {
            "type": "creative_result",
            "content": response.content,
            "agent": self.agent_type.value,
            "format": "text",  # Würde aus Kontext erkannt
            "brand_aligned": True,
        }
