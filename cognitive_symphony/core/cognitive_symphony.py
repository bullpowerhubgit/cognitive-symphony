"""
Cognitive Symphony - Haupt-Interface für das System

Diese Klasse orchestriert alle Komponenten und bietet das User-Interface
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
import structlog

from cognitive_symphony.config import settings
from cognitive_symphony.core.meta_orchestrator import MetaOrchestrator
from cognitive_symphony.agents.agent_fleet import AgentFleet
from cognitive_symphony.memory.memory_system import MemorySystem
from cognitive_symphony.optimization.self_optimizer import SelfOptimizer
from cognitive_symphony.models import (
    AgentType,
    SymphonyResult,
    Task,
    TaskPriority,
    TaskStatus,
)

logger = structlog.get_logger()


class CognitiveSymphony:
    """
    Haupt-Interface für Cognitive Symphony - das selbstoptimierende
    Multi-Agent-Ökosystem
    """

    def __init__(
        self,
        llm_provider: str = "openai",
        enable_learning: bool = True,
        enable_transparency: bool = True,
    ):
        """
        Initialisiert Cognitive Symphony

        Args:
            llm_provider: 'openai' oder 'anthropic'
            enable_learning: Aktiviert Self-Optimization
            enable_transparency: Aktiviert Transparenz-Layer
        """
        self.llm_provider = llm_provider
        self.enable_learning = enable_learning
        self.enable_transparency = enable_transparency

        # Initialisiere Komponenten
        self.meta_orchestrator = MetaOrchestrator(
            llm_provider=llm_provider,
            enable_learning=enable_learning,
        )

        self.agent_fleet = AgentFleet(llm_provider=llm_provider)

        self.memory_system = MemorySystem()

        self.self_optimizer = SelfOptimizer(
            enable_ab_testing=settings.enable_ab_testing,
            enable_rl=settings.enable_reinforcement_learning,
        )

        self.task_history: List[Task] = []

        logger.info(
            "cognitive_symphony_initialized",
            llm_provider=llm_provider,
            learning=enable_learning,
            transparency=enable_transparency,
        )

    async def solve(
        self,
        task: Any,
        optimization_level: str = "medium",
        context: Optional[Dict[str, Any]] = None,
    ) -> SymphonyResult:
        """
        Löst eine komplexe Aufgabe durch intelligente Orchestrierung

        Args:
            task: Die zu lösende Aufgabe (str, dict, oder Task-Objekt)
            optimization_level: 'low', 'medium', 'high'
            context: Zusätzlicher Kontext

        Returns:
            SymphonyResult mit Lösung und Metriken
        """
        start_time = datetime.now()

        # Konvertiere Task zu Task-Objekt
        if isinstance(task, str):
            task_obj = Task(description=task, context=context or {})
        elif isinstance(task, dict):
            task_obj = Task(
                description=task.get("objective", ""),
                context={**task, **(context or {})},
            )
        elif isinstance(task, Task):
            task_obj = task
        else:
            raise ValueError(f"Unsupported task type: {type(task)}")

        logger.info(
            "solving_task",
            task_id=task_obj.id,
            description=task_obj.description[:100],
        )

        # 1. Task-Dekomposition
        subtasks = await self.meta_orchestrator.decompose_task(task_obj)

        # 2. Agenten-Auswahl und Orchestrierung
        agent_interactions = []
        orchestration_decisions = []

        for subtask in subtasks:
            # Hole Performance-Historie aus Memory
            agent_performance = self.memory_system.get_agent_performance_history()

            # Wähle optimale Agenten
            selected_agents, decision = (
                await self.meta_orchestrator.select_optimal_agents(
                    subtask, agent_performance
                )
            )

            orchestration_decisions.append(decision)

            # Führe Subtask mit ausgewählten Agenten aus
            subtask.status = TaskStatus.IN_PROGRESS
            subtask.started_at = datetime.now()

            try:
                result = await self.agent_fleet.execute_task(subtask, selected_agents)

                subtask.status = TaskStatus.COMPLETED
                subtask.result = result
                subtask.completed_at = datetime.now()

                # Lerne aus Erfolg
                performance = 0.8  # Vereinfacht - würde in Produktion berechnet
                await self.meta_orchestrator.learn_from_outcome(
                    decision, "success", performance
                )

                agent_interactions.append(
                    {
                        "subtask_id": subtask.id,
                        "agents": [a.value for a in selected_agents],
                        "status": "success",
                        "result": result,
                    }
                )

            except Exception as e:
                subtask.status = TaskStatus.FAILED
                subtask.error = str(e)
                subtask.completed_at = datetime.now()

                # Lerne aus Fehler
                await self.meta_orchestrator.learn_from_outcome(
                    decision, "failure", 0.2
                )

                agent_interactions.append(
                    {
                        "subtask_id": subtask.id,
                        "agents": [a.value for a in selected_agents],
                        "status": "failure",
                        "error": str(e),
                    }
                )

                logger.error(
                    "subtask_failed",
                    subtask_id=subtask.id,
                    error=str(e),
                )

        # 3. Zusammenführen der Ergebnisse
        solution = self._combine_subtask_results(subtasks)

        # 4. Speichere in Memory
        self.memory_system.store_episode(task_obj, subtasks, orchestration_decisions)

        # 5. Self-Optimization
        if self.enable_learning:
            await self.self_optimizer.optimize(
                task_obj, subtasks, orchestration_decisions
            )

        # 6. Learning Insights generieren
        learning_insights = self.meta_orchestrator.get_performance_metrics()

        execution_time = (datetime.now() - start_time).total_seconds()

        result = SymphonyResult(
            task_id=task_obj.id,
            solution=solution,
            status=task_obj.status,
            agent_interactions=agent_interactions,
            orchestration_decisions=orchestration_decisions,
            learning_insights=learning_insights,
            performance_metrics={
                "execution_time": execution_time,
                "subtasks_completed": len(
                    [s for s in subtasks if s.status == TaskStatus.COMPLETED]
                ),
                "subtasks_failed": len(
                    [s for s in subtasks if s.status == TaskStatus.FAILED]
                ),
            },
            execution_time=execution_time,
        )

        logger.info(
            "task_solved",
            task_id=task_obj.id,
            execution_time=execution_time,
            status=task_obj.status.value,
        )

        return result

    def _combine_subtask_results(self, subtasks: List[Task]) -> Any:
        """
        Kombiniert die Ergebnisse aller Subtasks zu einer finalen Lösung
        """
        results = []

        for subtask in subtasks:
            if subtask.status == TaskStatus.COMPLETED and subtask.result:
                results.append(
                    {
                        "subtask": subtask.description,
                        "result": subtask.result,
                        "agent": subtask.assigned_agent.value
                        if subtask.assigned_agent
                        else "unknown",
                    }
                )

        return {
            "summary": "Task completed successfully",
            "subtask_results": results,
            "total_subtasks": len(subtasks),
            "completed": len([s for s in subtasks if s.status == TaskStatus.COMPLETED]),
            "failed": len([s for s in subtasks if s.status == TaskStatus.FAILED]),
        }

    async def analyze_performance(self) -> Dict[str, Any]:
        """
        Analysiert die Gesamt-Performance des Systems

        Returns:
            Performance-Metriken
        """
        orchestrator_metrics = self.meta_orchestrator.get_performance_metrics()
        agent_metrics = self.agent_fleet.get_performance_metrics()
        memory_metrics = self.memory_system.get_metrics()
        optimizer_metrics = self.self_optimizer.get_metrics()

        return {
            "orchestrator": orchestrator_metrics,
            "agents": agent_metrics,
            "memory": memory_metrics,
            "optimizer": optimizer_metrics,
            "timestamp": datetime.now().isoformat(),
        }

    def get_transparency_report(self, task_id: str) -> Dict[str, Any]:
        """
        Generiert einen Transparenz-Report für eine spezifische Aufgabe

        Args:
            task_id: ID der Aufgabe

        Returns:
            Detaillierter Transparenz-Report
        """
        if not self.enable_transparency:
            return {"message": "Transparency layer is disabled"}

        # Hole alle relevanten Daten aus Memory
        decisions = [
            d for d in self.meta_orchestrator.decision_history if d.task_id == task_id
        ]

        return {
            "task_id": task_id,
            "decisions": [d.dict() for d in decisions],
            "reasoning": [d.reasoning for d in decisions],
            "confidence_scores": [d.confidence for d in decisions],
            "alternative_strategies": [d.alternative_strategies for d in decisions],
        }
