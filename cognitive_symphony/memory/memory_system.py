"""
Memory System - Tri-Layer Gedächtnis-System
- Episodisches Gedächtnis: Erfolge und Fehler
- Semantisches Gedächtnis: Wissensdatenbank
- Prozedurales Gedächtnis: Workflows und Strategien
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import structlog
from collections import defaultdict

from cognitive_symphony.config import settings
from cognitive_symphony.models import AgentType, MemoryEntry, OrchestrationDecision, Task

logger = structlog.get_logger()


class MemorySystem:
    """
    Tri-Layer Gedächtnis-System für Cognitive Symphony

    - Episodic Memory: Erinnert Ereignisse und Erfahrungen
    - Semantic Memory: Speichert Fakten und Wissen
    - Procedural Memory: Lernt Fähigkeiten und Workflows
    """

    def __init__(self):
        """Initialisiert das Gedächtnis-System"""
        # In Produktion würden hier echte Datenbanken verwendet
        self.episodic_memory: List[MemoryEntry] = []
        self.semantic_memory: List[MemoryEntry] = []
        self.procedural_memory: List[MemoryEntry] = []

        # Indizes für schnellen Zugriff
        self.task_index: Dict[str, List[MemoryEntry]] = defaultdict(list)
        self.agent_performance_index: Dict[AgentType, Dict[str, Any]] = defaultdict(
            lambda: {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "avg_performance": 0.0,
            }
        )

        logger.info("memory_system_initialized")

    def store_episode(
        self,
        task: Task,
        subtasks: List[Task],
        decisions: List[OrchestrationDecision],
    ) -> None:
        """
        Speichert eine Episode (Task-Ausführung) im episodischen Gedächtnis

        Args:
            task: Die Hauptaufgabe
            subtasks: Alle Subtasks
            decisions: Alle Orchestrierungs-Entscheidungen
        """
        episode = MemoryEntry(
            type="episodic",
            content={
                "task": task.dict(),
                "subtasks": [s.dict() for s in subtasks],
                "decisions": [d.dict() for d in decisions],
                "outcome": task.status.value,
            },
            importance=self._calculate_importance(task, decisions),
            tags=["episode", task.status.value],
        )

        self.episodic_memory.append(episode)
        self.task_index[task.id].append(episode)

        # Update Agent Performance Index
        for decision in decisions:
            for agent_type in decision.selected_agents:
                perf = self.agent_performance_index[agent_type]
                perf["total_tasks"] += 1

                if decision.outcome == "success":
                    perf["successful_tasks"] += 1

                perf["avg_performance"] = (
                    perf["successful_tasks"] / perf["total_tasks"]
                    if perf["total_tasks"] > 0
                    else 0.0
                )

        logger.info(
            "episode_stored",
            task_id=task.id,
            episode_id=episode.id,
            importance=episode.importance,
        )

        # Cleanup alte Einträge
        self._cleanup_old_memories()

    def store_knowledge(
        self, knowledge: Dict[str, Any], tags: List[str], importance: float = 0.5
    ) -> None:
        """
        Speichert Wissen im semantischen Gedächtnis

        Args:
            knowledge: Das zu speichernde Wissen
            tags: Tags für Kategorisierung
            importance: Wichtigkeit (0.0-1.0)
        """
        memory_entry = MemoryEntry(
            type="semantic",
            content=knowledge,
            importance=importance,
            tags=tags,
        )

        self.semantic_memory.append(memory_entry)

        logger.info(
            "knowledge_stored",
            entry_id=memory_entry.id,
            tags=tags,
        )

    def store_workflow(self, workflow: Dict[str, Any], performance: float, tags: List[str]) -> None:
        """
        Speichert einen Workflow im prozeduralen Gedächtnis

        Args:
            workflow: Der Workflow (Agenten-Kombinationen, Strategien)
            performance: Performance-Score des Workflows
            tags: Tags für Kategorisierung
        """
        memory_entry = MemoryEntry(
            type="procedural",
            content=workflow,
            importance=performance,
            tags=tags,
            metadata={"performance": performance},
        )

        self.procedural_memory.append(memory_entry)

        logger.info(
            "workflow_stored",
            entry_id=memory_entry.id,
            performance=performance,
        )

    def recall_episodes(self, query: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        """
        Ruft relevante Episoden ab

        Args:
            query: Suchbegriff (optional)
            limit: Maximum anzahl Ergebnisse

        Returns:
            Liste von Memory-Einträgen
        """
        # Vereinfachte Suche - in Produktion würde man Vector-Search nutzen
        episodes = sorted(
            self.episodic_memory,
            key=lambda e: (e.importance, e.timestamp),
            reverse=True,
        )

        if query:
            # Einfacher String-Match
            episodes = [
                e
                for e in episodes
                if query.lower() in str(e.content).lower()
                or any(query.lower() in tag.lower() for tag in e.tags)
            ]

        return episodes[:limit]

    def recall_knowledge(self, tags: Optional[List[str]] = None) -> List[MemoryEntry]:
        """
        Ruft Wissen aus dem semantischen Gedächtnis ab

        Args:
            tags: Filter nach Tags

        Returns:
            Liste von Memory-Einträgen
        """
        knowledge = self.semantic_memory

        if tags:
            knowledge = [k for k in knowledge if any(tag in k.tags for tag in tags)]

        return sorted(knowledge, key=lambda k: k.importance, reverse=True)

    def recall_workflows(self, min_performance: float = 0.0, limit: int = 10) -> List[MemoryEntry]:
        """
        Ruft erfolgreiche Workflows ab

        Args:
            min_performance: Minimale Performance
            limit: Maximum Anzahl Ergebnisse

        Returns:
            Liste von Memory-Einträgen
        """
        workflows = [
            w
            for w in self.procedural_memory
            if w.metadata.get("performance", 0.0) >= min_performance
        ]

        return sorted(
            workflows,
            key=lambda w: w.metadata.get("performance", 0.0),
            reverse=True,
        )[:limit]

    def get_agent_performance_history(self) -> Dict[AgentType, Dict[str, float]]:
        """
        Gibt Performance-Historie aller Agenten zurück

        Returns:
            Dictionary mit Agent-Performance-Daten
        """
        return dict(self.agent_performance_index)

    def _calculate_importance(self, task: Task, decisions: List[OrchestrationDecision]) -> float:
        """
        Berechnet die Wichtigkeit einer Episode

        Faktoren:
        - Task-Priorität
        - Anzahl Entscheidungen
        - Durchschnittliche Confidence
        - Outcome
        """
        priority_weight = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.7,
            "critical": 1.0,
        }

        base_importance = priority_weight.get(task.priority.value, 0.5)

        # Mehr Entscheidungen = höhere Komplexität = wichtiger
        complexity_factor = min(len(decisions) * 0.1, 0.3)

        # Durchschnittliche Confidence
        avg_confidence = sum(d.confidence for d in decisions) / len(decisions) if decisions else 0.5

        # Outcome-Bonus
        outcome_factor = 0.2 if task.status.value == "completed" else 0.0

        importance = base_importance + complexity_factor + (avg_confidence * 0.2) + outcome_factor

        return min(importance, 1.0)

    def _cleanup_old_memories(self) -> None:
        """
        Entfernt alte, unwichtige Erinnerungen basierend auf Retention-Policy
        """
        cutoff_date = datetime.now() - timedelta(days=settings.memory_retention_days)

        # Episodisches Gedächtnis - behalte nur wichtige oder neue
        self.episodic_memory = [
            e for e in self.episodic_memory if e.timestamp > cutoff_date or e.importance > 0.7
        ]

        # Semantisches Gedächtnis - behalte häufig genutzte oder wichtige
        self.semantic_memory = [
            s for s in self.semantic_memory if s.access_count > 5 or s.importance > 0.6
        ]

        logger.info("memory_cleanup_completed")

    def get_metrics(self) -> Dict[str, Any]:
        """Gibt Memory-System-Metriken zurück"""
        return {
            "episodic_memory_size": len(self.episodic_memory),
            "semantic_memory_size": len(self.semantic_memory),
            "procedural_memory_size": len(self.procedural_memory),
            "total_tasks_tracked": len(self.task_index),
            "agents_tracked": len(self.agent_performance_index),
        }
