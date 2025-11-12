"""
Research Agent - Spezialisiert auf Web-Recherche und Informationssammlung
"""

from typing import Any, List
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.agents.base_agent import BaseAgent
from cognitive_symphony.models import AgentCapability, AgentType, Task


class ResearchAgent(BaseAgent):
    """Agent für Web-Recherche und Wissensbasis-Erstellung"""

    def __init__(self, llm: Any):
        super().__init__(AgentType.RESEARCH, llm)

    def _initialize_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="Web Research",
                description="Durchsucht das Web nach relevanten Informationen",
                skill_level=0.9,
                success_rate=0.85,
            ),
            AgentCapability(
                name="Data Extraction",
                description="Extrahiert strukturierte Daten aus unstrukturierten Quellen",
                skill_level=0.85,
                success_rate=0.8,
            ),
            AgentCapability(
                name="Knowledge Base Creation",
                description="Erstellt strukturierte Wissensbasen",
                skill_level=0.8,
                success_rate=0.9,
            ),
        ]

    async def execute(self, task: Task) -> Any:
        """Führt Research-Aufgaben aus"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Research Agent, spezialisiert auf gründliche Recherche 
                    und Informationssammlung. Analysiere die Aufgabe und erstelle eine 
                    umfassende Recherche.
                    
                    Fähigkeiten:
                    - Web-Recherche und -Analyse
                    - Datenextraktion und -strukturierung
                    - Wissensbasis-Erstellung
                    - Quellenverifizierung
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
            "type": "research_result",
            "findings": response.content,
            "agent": self.agent_type.value,
            "sources": ["web_search", "knowledge_base"],  # Vereinfacht
        }
