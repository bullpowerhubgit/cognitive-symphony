"""
Transparency Layer - Vollständige Transparenz aller System-Entscheidungen

Trackt und visualisiert:
- Alle Orchestrierungs-Entscheidungen
- Agent-Interaktionen
- Performance-Metriken
- Learning-Prozesse
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import structlog

from cognitive_symphony.models import OrchestrationDecision, Task

logger = structlog.get_logger()


class TransparencyTracker:
    """
    Trackt alle System-Entscheidungen für vollständige Transparenz

    Ermöglicht:
    - Nachvollziehbarkeit aller Entscheidungen
    - Audit-Trail
    - Debugging
    - Human-in-the-Loop Feedback
    """

    def __init__(self, log_dir: str = "./logs/transparency"):
        """
        Initialisiert den Transparency Tracker

        Args:
            log_dir: Verzeichnis für Transparenz-Logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.decision_log: List[Dict[str, Any]] = []
        self.interaction_log: List[Dict[str, Any]] = []

        logger.info("transparency_tracker_initialized", log_dir=str(self.log_dir))

    def log_decision(self, decision: OrchestrationDecision, context: Dict[str, Any]) -> None:
        """
        Loggt eine Orchestrierungs-Entscheidung

        Args:
            decision: Die getroffene Entscheidung
            context: Zusätzlicher Kontext
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "decision_id": decision.decision_id,
            "task_id": decision.task_id,
            "selected_agents": [a.value for a in decision.selected_agents],
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "alternative_strategies": decision.alternative_strategies,
            "context": context,
        }

        self.decision_log.append(entry)

        # Persistiere in Datei
        self._persist_log("decisions", entry)

        logger.info(
            "decision_logged",
            decision_id=decision.decision_id,
            agents=[a.value for a in decision.selected_agents],
        )

    def log_interaction(
        self,
        task_id: str,
        agent_type: str,
        action: str,
        result: Any,
        metadata: Dict[str, Any],
    ) -> None:
        """
        Loggt eine Agent-Interaktion

        Args:
            task_id: Task-ID
            agent_type: Typ des Agenten
            action: Durchgeführte Aktion
            result: Ergebnis
            metadata: Zusätzliche Metadaten
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "agent_type": agent_type,
            "action": action,
            "result": str(result)[:500],  # Limitiere Größe
            "metadata": metadata,
        }

        self.interaction_log.append(entry)
        self._persist_log("interactions", entry)

        logger.debug("interaction_logged", task_id=task_id, agent=agent_type)

    def generate_report(self, task_id: str) -> Dict[str, Any]:
        """
        Generiert einen Transparenz-Report für eine Aufgabe

        Args:
            task_id: Task-ID

        Returns:
            Detaillierter Transparenz-Report
        """
        # Filtere relevante Entscheidungen
        decisions = [d for d in self.decision_log if d["task_id"] == task_id]

        # Filtere relevante Interaktionen
        interactions = [i for i in self.interaction_log if i["task_id"] == task_id]

        report = {
            "task_id": task_id,
            "generated_at": datetime.now().isoformat(),
            "decision_count": len(decisions),
            "interaction_count": len(interactions),
            "decisions": decisions,
            "interactions": interactions,
            "timeline": self._create_timeline(decisions, interactions),
        }

        # Speichere Report
        report_path = (
            self.log_dir / f"report_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info("transparency_report_generated", task_id=task_id, path=str(report_path))

        return report

    def _create_timeline(
        self, decisions: List[Dict], interactions: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Erstellt eine chronologische Timeline aller Events"""
        timeline = []

        for decision in decisions:
            timeline.append(
                {
                    "timestamp": decision["timestamp"],
                    "type": "decision",
                    "data": decision,
                }
            )

        for interaction in interactions:
            timeline.append(
                {
                    "timestamp": interaction["timestamp"],
                    "type": "interaction",
                    "data": interaction,
                }
            )

        # Sortiere chronologisch
        timeline.sort(key=lambda x: x["timestamp"])

        return timeline

    def _persist_log(self, log_type: str, entry: Dict[str, Any]) -> None:
        """Persistiert Log-Einträge in Dateien"""
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"{log_type}_{date_str}.jsonl"

        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_metrics(self) -> Dict[str, Any]:
        """Gibt Transparenz-Metriken zurück"""
        return {
            "total_decisions_logged": len(self.decision_log),
            "total_interactions_logged": len(self.interaction_log),
            "log_directory": str(self.log_dir),
        }


class PerformanceMonitor:
    """
    Monitort System-Performance in Echtzeit

    Trackt:
    - Execution Times
    - Success Rates
    - Resource Usage
    - Agent Performance
    """

    def __init__(self):
        """Initialisiert den Performance Monitor"""
        self.metrics: Dict[str, List[float]] = {
            "task_execution_time": [],
            "success_rate": [],
            "agent_utilization": [],
        }

        logger.info("performance_monitor_initialized")

    def record_metric(self, metric_name: str, value: float) -> None:
        """
        Zeichnet eine Performance-Metrik auf

        Args:
            metric_name: Name der Metrik
            value: Wert
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []

        self.metrics[metric_name].append(value)

        logger.debug("metric_recorded", metric=metric_name, value=value)

    def get_statistics(self, metric_name: str) -> Dict[str, float]:
        """
        Gibt Statistiken für eine Metrik zurück

        Args:
            metric_name: Name der Metrik

        Returns:
            Statistiken (avg, min, max, etc.)
        """
        values = self.metrics.get(metric_name, [])

        if not values:
            return {}

        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1],
        }

    def get_all_metrics(self) -> Dict[str, Dict[str, float]]:
        """Gibt alle Performance-Metriken zurück"""
        return {
            metric_name: self.get_statistics(metric_name) for metric_name in self.metrics.keys()
        }
