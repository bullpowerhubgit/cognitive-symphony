"""
Code Agent - Spezialisiert auf Programmierung, Testing und Debugging
"""

from typing import Any, List
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.agents.base_agent import BaseAgent
from cognitive_symphony.models import AgentCapability, AgentType, Task


class CodeAgent(BaseAgent):
    """Agent für Code-Entwicklung, Testing und Debugging"""

    def __init__(self, llm: Any):
        super().__init__(AgentType.CODE, llm)

    def _initialize_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="Multi-Language Programming",
                description="Programmierung in Python, JavaScript, TypeScript, Go, Rust, etc.",
                skill_level=0.95,
                success_rate=0.9,
            ),
            AgentCapability(
                name="Testing & Debugging",
                description="Unit-Tests, Integration-Tests, Debugging",
                skill_level=0.9,
                success_rate=0.85,
            ),
            AgentCapability(
                name="Code Review",
                description="Code-Analyse und Optimierungsvorschläge",
                skill_level=0.88,
                success_rate=0.92,
            ),
            AgentCapability(
                name="Architecture Design",
                description="Software-Architektur und Design Patterns",
                skill_level=0.85,
                success_rate=0.87,
            ),
        ]

    async def execute(self, task: Task) -> Any:
        """Führt Code-Aufgaben aus"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Code Agent, ein Experte in Software-Entwicklung.
                    
                    Fähigkeiten:
                    - Multi-Language Programming (Python, JS, TS, Go, Rust, etc.)
                    - Testing & Debugging (Unit, Integration, E2E)
                    - Code Review und Optimierung
                    - Architektur-Design
                    - Best Practices und Design Patterns
                    
                    Erstelle hochwertigen, gut dokumentierten Code mit Tests.
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
            "type": "code_result",
            "code": response.content,
            "agent": self.agent_type.value,
            "language": "python",  # Würde aus Kontext erkannt
            "tests_included": True,
        }
