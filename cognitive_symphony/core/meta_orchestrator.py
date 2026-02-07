"""
Meta-Orchestrator - Das orchestrierende Gehirn von Cognitive Symphony

Der Meta-Orchestrator ist verantwortlich für:
- Intelligente Task-Dekomposition
- Dynamische Agenten-Auswahl
- Selbst-Optimierung durch Reinforcement Learning
- Adaptive Team-Neubildung
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import structlog
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.config import settings
from cognitive_symphony.models import (
    AgentType,
    OrchestrationDecision,
    Task,
    TaskPriority,
    TaskStatus,
)

logger = structlog.get_logger()


class MetaOrchestrator:
    """
    Der zentrale Meta-Orchestrator koordiniert alle Agenten und optimiert
    kontinuierlich seine Strategien durch Metakognition.
    """

    def __init__(
        self,
        llm_provider: str = "openai",
        enable_learning: bool = True,
    ):
        """
        Initialisiert den Meta-Orchestrator

        Args:
            llm_provider: 'openai' oder 'anthropic'
            enable_learning: Aktiviert Reinforcement Learning
        """
        self.llm_provider = llm_provider
        self.enable_learning = enable_learning
        self.llm = self._initialize_llm()
        self.decision_history: List[OrchestrationDecision] = []
        self.strategy_performance: Dict[str, float] = {}

        logger.info(
            "meta_orchestrator_initialized",
            llm_provider=llm_provider,
            learning_enabled=enable_learning,
        )

    def _initialize_llm(self) -> Any:
        """Initialisiert das Language Model basierend auf dem Provider"""
        if self.llm_provider == "openai":
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7,
                api_key=settings.openai_api_key,
            )
        elif self.llm_provider == "anthropic":
            return ChatAnthropic(
                model="claude-3-5-sonnet-20240620",
                temperature=0.7,
                api_key=settings.anthropic_api_key,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    async def decompose_task(self, task: Task) -> List[Task]:
        """
        Zerlegt eine komplexe Aufgabe in Teilaufgaben

        Args:
            task: Die zu zerlegende Aufgabe

        Returns:
            Liste von Teilaufgaben
        """
        logger.info("decomposing_task", task_id=task.id, description=task.description)

        # Prompt für Task-Dekomposition
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Meta-Orchestrator, der komplexe Aufgaben intelligent in 
                    Teilaufgaben zerlegt. Analysiere die Aufgabe und erstelle eine optimale 
                    Zerlegung in logische, ausführbare Schritte.
                    
                    Verfügbare Agent-Typen:
                    - RESEARCH: Web-Recherche, Informationssammlung
                    - CODE: Programmierung, Testing, Debugging
                    - ANALYSIS: Datenanalyse, Mustererkennung
                    - CREATIVE: Content-Generierung, Design
                    - SECURITY: Sicherheitsprüfung, Threat-Detection
                    - OPTIMIZATION: Performance-Optimierung, Kostenreduktion
                    - HUMAN_INTERFACE: Kommunikation mit Menschen
                    
                    Erstelle eine strukturierte Zerlegung mit:
                    1. Beschreibung der Teilaufgabe
                    2. Empfohlener Agent-Typ
                    3. Priorität (LOW, MEDIUM, HIGH, CRITICAL)
                    4. Abhängigkeiten zu anderen Teilaufgaben
                    """,
                ),
                (
                    "human",
                    "Aufgabe: {task_description}\nKontext: {context}",
                ),
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "task_description": task.description,
                "context": str(task.context),
            }
        )

        # Parse LLM Response und erstelle Teilaufgaben
        subtasks = self._parse_subtasks_from_response(response.content, task.id)

        logger.info(
            "task_decomposed",
            task_id=task.id,
            subtask_count=len(subtasks),
        )

        return subtasks

    def _parse_subtasks_from_response(self, response: str, parent_task_id: str) -> List[Task]:
        """
        Parst die LLM-Antwort und erstellt Task-Objekte

        Diese Methode würde in einer produktiven Umgebung strukturiertes Output-Parsing
        verwenden (z.B. mit Pydantic). Hier eine vereinfachte Version.
        """
        subtasks = []

        # Vereinfachtes Parsing - in Produktion würde man strukturiertes Output-Format nutzen
        lines = response.split("\n")
        current_subtask = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Erkennen von Task-Beschreibungen (vereinfacht)
            if any(keyword in line.lower() for keyword in ["aufgabe", "schritt", "task", "step"]):
                if current_subtask:
                    subtasks.append(current_subtask)

                current_subtask = Task(
                    description=line,
                    parent_task_id=parent_task_id,
                    priority=TaskPriority.MEDIUM,
                )

            # Agent-Typ erkennen
            elif current_subtask:
                for agent_type in AgentType:
                    if agent_type.value.lower() in line.lower():
                        current_subtask.assigned_agent = agent_type
                        break

        if current_subtask:
            subtasks.append(current_subtask)

        # Fallback: Wenn Parsing fehlschlägt, erstelle eine einfache Teilaufgabe
        if not subtasks:
            subtasks.append(
                Task(
                    description=response[:200],  # Erste 200 Zeichen
                    parent_task_id=parent_task_id,
                    priority=TaskPriority.MEDIUM,
                )
            )

        return subtasks

    async def select_optimal_agents(
        self,
        task: Task,
        agent_performance_history: Dict[AgentType, Dict[str, float]],
    ) -> Tuple[List[AgentType], OrchestrationDecision]:
        """
        Wählt die optimalen Agenten für eine Aufgabe basierend auf:
        - Task-Anforderungen
        - Historischer Agent-Performance
        - Aktuellem System-Zustand

        Args:
            task: Die auszuführende Aufgabe
            agent_performance_history: Performance-Daten der Agenten

        Returns:
            Tuple von (ausgewählte Agenten, Entscheidungsdokumentation)
        """
        logger.info("selecting_optimal_agents", task_id=task.id)

        # Wenn Agent bereits zugewiesen, verwende diesen
        if task.assigned_agent:
            decision = OrchestrationDecision(
                task_id=task.id,
                selected_agents=[task.assigned_agent],
                reasoning="Pre-assigned agent from task decomposition",
                confidence=0.8,
            )
            return [task.assigned_agent], decision

        # Analysiere Task und wähle Agenten
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Meta-Orchestrator mit Metakognition. Analysiere die Aufgabe 
                    und wähle die optimalen Agenten aus. Berücksichtige:
                    
                    1. Task-Anforderungen
                    2. Agent-Performance-Historie
                    3. Potenzielle Synergien zwischen Agenten
                    4. Ressourcen-Effizienz
                    
                    Verfügbare Agenten: {available_agents}
                    Performance-Historie: {performance_history}
                    
                    Antworte mit:
                    - Liste der ausgewählten Agenten
                    - Begründung für jede Auswahl
                    - Confidence-Score (0.0-1.0)
                    - Alternative Strategien
                    """,
                ),
                (
                    "human",
                    "Aufgabe: {task_description}\nPriorität: {priority}\nKontext: {context}",
                ),
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "task_description": task.description,
                "priority": task.priority.value,
                "context": str(task.context),
                "available_agents": [agent.value for agent in AgentType],
                "performance_history": str(agent_performance_history),
            }
        )

        # Parse Response
        selected_agents, reasoning, confidence = self._parse_agent_selection(response.content)

        decision = OrchestrationDecision(
            task_id=task.id,
            selected_agents=selected_agents,
            reasoning=reasoning,
            confidence=confidence,
        )

        self.decision_history.append(decision)

        logger.info(
            "agents_selected",
            task_id=task.id,
            agents=[a.value for a in selected_agents],
            confidence=confidence,
        )

        return selected_agents, decision

    def _parse_agent_selection(self, response: str) -> Tuple[List[AgentType], str, float]:
        """Parst die Agent-Auswahl aus der LLM-Antwort"""
        selected_agents = []
        reasoning = response
        confidence = 0.7  # Default

        # Erkenne Agent-Typen im Response
        for agent_type in AgentType:
            if agent_type.value.lower() in response.lower():
                selected_agents.append(agent_type)

        # Fallback: Wenn keine Agenten erkannt, nutze generischen Agenten
        if not selected_agents:
            selected_agents = [AgentType.RESEARCH]

        # Versuche Confidence zu extrahieren
        confidence_keywords = ["confidence", "vertrauen", "sicherheit"]
        for line in response.split("\n"):
            if any(keyword in line.lower() for keyword in confidence_keywords):
                # Suche nach Zahlen zwischen 0 und 1
                import re

                numbers = re.findall(r"0\.\d+", line)
                if numbers:
                    confidence = float(numbers[0])
                    break

        return selected_agents, reasoning, confidence

    async def learn_from_outcome(
        self, decision: OrchestrationDecision, outcome: str, performance: float
    ) -> None:
        """
        Lernt aus dem Ergebnis einer Orchestrierungs-Entscheidung

        Args:
            decision: Die getroffene Entscheidung
            outcome: 'success', 'failure', oder 'partial'
            performance: Performance-Score (0.0-1.0)
        """
        if not self.enable_learning:
            return

        decision.outcome = outcome
        decision.learning_feedback = f"Performance: {performance}"

        # Update Strategy-Performance
        strategy_key = "_".join([agent.value for agent in decision.selected_agents])

        if strategy_key not in self.strategy_performance:
            self.strategy_performance[strategy_key] = performance
        else:
            # Exponential moving average
            alpha = 0.3
            self.strategy_performance[strategy_key] = (
                alpha * performance + (1 - alpha) * self.strategy_performance[strategy_key]
            )

        logger.info(
            "learned_from_outcome",
            decision_id=decision.decision_id,
            outcome=outcome,
            performance=performance,
            strategy=strategy_key,
        )

        # Metakognitiver Reflexionsprozess
        if len(self.decision_history) % 10 == 0:  # Alle 10 Entscheidungen
            await self._metacognitive_reflection()

    async def _metacognitive_reflection(self) -> None:
        """
        Metakognitiver Reflexionsprozess - das System denkt über sein eigenes Denken nach
        und identifiziert Verbesserungsmöglichkeiten
        """
        logger.info("starting_metacognitive_reflection")

        recent_decisions = self.decision_history[-10:]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein Meta-Orchestrator mit Metakognition. Analysiere deine 
                    letzten Entscheidungen und identifiziere Muster, Verbesserungsmöglichkeiten 
                    und neue Strategien.
                    
                    Fragen zur Reflexion:
                    1. Welche Agenten-Kombinationen waren am erfolgreichsten?
                    2. Welche Fehler wurden wiederholt gemacht?
                    3. Gibt es ungenutzte Synergien zwischen Agenten?
                    4. Wie können zukünftige Entscheidungen optimiert werden?
                    """,
                ),
                (
                    "human",
                    "Letzte Entscheidungen: {decisions}\nStrategy Performance: {performance}",
                ),
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "decisions": str([d.dict() for d in recent_decisions]),
                "performance": str(self.strategy_performance),
            }
        )

        logger.info("metacognitive_reflection_completed", insights=response.content[:200])

        # In Produktion würden die Insights gespeichert und angewendet

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Gibt Performance-Metriken des Orchestrators zurück"""
        total_decisions = len(self.decision_history)
        successful_decisions = sum(1 for d in self.decision_history if d.outcome == "success")

        return {
            "total_decisions": total_decisions,
            "successful_decisions": successful_decisions,
            "success_rate": (
                successful_decisions / total_decisions if total_decisions > 0 else 0.0
            ),
            "strategy_performance": self.strategy_performance,
            "avg_confidence": (
                sum(d.confidence for d in self.decision_history) / total_decisions
                if total_decisions > 0
                else 0.0
            ),
        }
