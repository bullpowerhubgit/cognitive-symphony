"""
Human Interface Agent - Spezialisiert auf Kommunikation mit Menschen
"""

from typing import Any, List
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.agents.base_agent import BaseAgent
from cognitive_symphony.models import AgentCapability, AgentType, Task


class HumanInterfaceAgent(BaseAgent):
    """Agent für Kommunikation und Feedback-Management"""

    def __init__(self, llm: Any):
        super().__init__(AgentType.HUMAN_INTERFACE, llm)

    def _initialize_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="Natural Communication",
                description="Natürliche, menschliche Kommunikation",
                skill_level=0.95,
                success_rate=0.92,
            ),
            AgentCapability(
                name="Feedback Collection",
                description="Sammlung und Verarbeitung von Feedback",
                skill_level=0.9,
                success_rate=0.88,
            ),
            AgentCapability(
                name="Explanation Generation",
                description="Verständliche Erklärungen komplexer Konzepte",
                skill_level=0.92,
                success_rate=0.91,
            ),
            AgentCapability(
                name="Conflict Resolution",
                description="Mediation und Konfliktlösung",
                skill_level=0.85,
                success_rate=0.83,
            ),
        ]

    async def execute(self, task: Task) -> Any:
        """Führt Kommunikationsaufgaben aus"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Human Interface Agent, spezialisiert auf Mensch-KI-Interaktion.
                    
                    Fähigkeiten:
                    - Natürliche, empathische Kommunikation
                    - Feedback-Sammlung und -Verarbeitung
                    - Verständliche Erklärungen komplexer Themen
                    - Konfliktlösung und Mediation
                    - User Experience Optimierung
                    
                    Kommuniziere klar, empathisch und zielgruppengerecht.
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
            "type": "communication_result",
            "message": response.content,
            "agent": self.agent_type.value,
            "tone": "professional",
            "clarity_score": 0.9,
        }
