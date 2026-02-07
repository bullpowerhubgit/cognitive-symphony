"""
Base Agent - Basisklasse für alle spezialisierten Agenten
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import structlog

from cognitive_symphony.models import AgentCapability, AgentPerformance, AgentType, Task

logger = structlog.get_logger()


class BaseAgent(ABC):
    """Abstrakte Basisklasse für alle Agenten"""

    def __init__(self, agent_type: AgentType, llm: Any):
        """
        Initialisiert einen Agenten

        Args:
            agent_type: Typ des Agenten
            llm: Language Model Instance
        """
        self.agent_type = agent_type
        self.llm = llm
        self.agent_id = f"{agent_type.value}_{id(self)}"
        self.performance = AgentPerformance(
            agent_id=self.agent_id,
            agent_type=agent_type,
        )
        self.capabilities = self._initialize_capabilities()

    @abstractmethod
    def _initialize_capabilities(self) -> list[AgentCapability]:
        """Definiert die Fähigkeiten des Agenten"""
        pass

    @abstractmethod
    async def execute(self, task: Task) -> Any:
        """
        Führt eine Aufgabe aus

        Args:
            task: Die auszuführende Aufgabe

        Returns:
            Ergebnis der Aufgabe
        """
        pass

    async def execute_with_metrics(self, task: Task) -> Any:
        """
        Führt eine Aufgabe aus und trackt Performance-Metriken

        Args:
            task: Die auszuführende Aufgabe

        Returns:
            Ergebnis der Aufgabe
        """
        start_time = datetime.now()

        try:
            result = await self.execute(task)

            # Update Performance-Metriken
            execution_time = (datetime.now() - start_time).total_seconds()
            self.performance.tasks_completed += 1
            self.performance.last_active = datetime.now()

            # Update durchschnittliche Execution Time
            total_tasks = self.performance.tasks_completed + self.performance.tasks_failed
            self.performance.avg_execution_time = (
                self.performance.avg_execution_time * (total_tasks - 1) + execution_time
            ) / total_tasks

            # Update Success Rate
            self.performance.avg_success_rate = self.performance.tasks_completed / total_tasks

            logger.info(
                "agent_task_completed",
                agent_type=self.agent_type.value,
                task_id=task.id,
                execution_time=execution_time,
            )

            return result

        except Exception as e:
            self.performance.tasks_failed += 1

            logger.error(
                "agent_task_failed",
                agent_type=self.agent_type.value,
                task_id=task.id,
                error=str(e),
            )

            raise

    def get_performance_metrics(self) -> dict[str, Any]:
        """Gibt Performance-Metriken des Agenten zurück"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "tasks_completed": self.performance.tasks_completed,
            "tasks_failed": self.performance.tasks_failed,
            "success_rate": self.performance.avg_success_rate,
            "avg_execution_time": self.performance.avg_execution_time,
            "capabilities": [c.dict() for c in self.capabilities],
        }

    def share_knowledge(self, knowledge: dict[str, Any]) -> None:
        """
        Teilt Wissen mit anderen Agenten (Kollaboratives Lernen)

        Args:
            knowledge: Zu teilendes Wissen
        """
        logger.info(
            "sharing_knowledge",
            agent_type=self.agent_type.value,
            knowledge_keys=list(knowledge.keys()),
        )

        # In Produktion würde dies in eine zentrale Knowledge-Base geschrieben
