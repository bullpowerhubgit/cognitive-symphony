"""
Self-Optimizer - Selbstoptimierungs-Engine
- A/B Testing verschiedener Strategien
- Reinforcement Learning
- Evolutionäre Algorithmen
- Predictive Analytics
"""

import random
from collections import defaultdict
from datetime import datetime
from typing import Any

import structlog

from cognitive_symphony.models import (
    AgentType,
    OptimizationResult,
    OrchestrationDecision,
    Task,
)

logger = structlog.get_logger()


class SelfOptimizer:
    """
    Selbstoptimierungs-Engine für kontinuierliche Systemverbesserung

    Nutzt:
    - A/B Testing für Strategievergleiche
    - Reinforcement Learning für Entscheidungsverbesserung
    - Evolutionäre Algorithmen für Strategieevolution
    - Predictive Analytics für Performance-Vorhersage
    """

    def __init__(self, enable_ab_testing: bool = True, enable_rl: bool = True):
        """
        Initialisiert die Self-Optimizer-Engine

        Args:
            enable_ab_testing: Aktiviert A/B Testing
            enable_rl: Aktiviert Reinforcement Learning
        """
        self.enable_ab_testing = enable_ab_testing
        self.enable_rl = enable_rl

        # A/B Testing
        self.ab_experiments: dict[str, dict[str, Any]] = {}
        self.strategy_variants: dict[str, list[list[AgentType]]] = defaultdict(list)

        # Reinforcement Learning
        self.q_table: dict[tuple, float] = {}  # State-Action Values
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.2  # Exploration rate

        # Evolutionäre Algorithmen
        self.strategy_population: list[dict[str, Any]] = []
        self.generation = 0

        # Performance Tracking
        self.optimization_history: list[OptimizationResult] = []

        logger.info(
            "self_optimizer_initialized",
            ab_testing=enable_ab_testing,
            reinforcement_learning=enable_rl,
        )

    async def optimize(
        self,
        task: Task,
        subtasks: list[Task],
        decisions: list[OrchestrationDecision],
    ) -> OptimizationResult | None:
        """
        Optimiert das System basierend auf der aktuellen Task-Ausführung

        Args:
            task: Die ausgeführte Hauptaufgabe
            subtasks: Alle Subtasks
            decisions: Alle Orchestrierungs-Entscheidungen

        Returns:
            OptimizationResult wenn Optimierung durchgeführt wurde
        """
        logger.info("starting_optimization", task_id=task.id)

        # 1. A/B Testing
        if self.enable_ab_testing:
            await self._run_ab_test(task, decisions)

        # 2. Reinforcement Learning Update
        if self.enable_rl:
            await self._update_q_values(task, decisions)

        # 3. Evolutionäre Optimierung (alle 10 Tasks)
        if len(self.optimization_history) % 10 == 0:
            result = await self._evolve_strategies(decisions)
            if result:
                self.optimization_history.append(result)
                return result

        # 4. Predictive Analytics
        await self._update_predictions(task, decisions)

        return None

    async def _run_ab_test(self, task: Task, decisions: list[OrchestrationDecision]) -> None:
        """
        Führt A/B Testing für verschiedene Strategien durch

        Vergleicht verschiedene Agenten-Kombinationen und trackt Performance
        """
        task_type = self._classify_task_type(task)

        # Erstelle Experiment wenn noch nicht existent
        if task_type not in self.ab_experiments:
            self.ab_experiments[task_type] = {
                "control_group": [],
                "variant_groups": defaultdict(list),
                "created_at": datetime.now(),
            }

        # Extrahiere verwendete Strategie
        strategy = tuple(sorted([a.value for d in decisions for a in d.selected_agents]))

        # Berechne Performance
        performance = self._calculate_performance(task, decisions)

        # Ordne zu Gruppe
        experiment = self.ab_experiments[task_type]
        if len(experiment["control_group"]) == 0:
            # Erste Strategie wird Control
            experiment["control_group"].append({"strategy": strategy, "performance": performance})
        else:
            # Variante
            experiment["variant_groups"][strategy].append(performance)

        logger.info(
            "ab_test_data_collected",
            task_type=task_type,
            strategy=strategy,
            performance=performance,
        )

        # Analysiere Ergebnisse wenn genug Daten
        if len(experiment["control_group"]) > 5 and len(experiment["variant_groups"]) > 0:
            await self._analyze_ab_results(task_type)

    async def _analyze_ab_results(self, task_type: str) -> None:
        """Analysiert A/B Test Ergebnisse und identifiziert bessere Strategien"""
        experiment = self.ab_experiments[task_type]

        control_performance = sum(r["performance"] for r in experiment["control_group"]) / len(
            experiment["control_group"]
        )

        logger.info(
            "ab_test_analysis",
            task_type=task_type,
            control_performance=control_performance,
        )

        # Finde beste Variante
        for strategy, performances in experiment["variant_groups"].items():
            if len(performances) > 3:
                avg_performance = sum(performances) / len(performances)

                if avg_performance > control_performance * 1.1:  # 10% Verbesserung
                    logger.info(
                        "ab_test_winner_found",
                        task_type=task_type,
                        strategy=strategy,
                        improvement=avg_performance - control_performance,
                    )

                    # Würde in Produktion die bessere Strategie als Standard setzen

    async def _update_q_values(self, task: Task, decisions: list[OrchestrationDecision]) -> None:
        """
        Update Q-Values für Reinforcement Learning

        Q-Learning Formula: Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        """
        for decision in decisions:
            # State: Task-Charakteristiken
            state = self._encode_state(task)

            # Action: Gewählte Agenten
            action = tuple(sorted([a.value for a in decision.selected_agents]))

            # Reward: Performance
            reward = decision.confidence if decision.outcome == "success" else -0.5

            # Current Q-Value
            current_q = self.q_table.get((state, action), 0.0)

            # Next state (vereinfacht - würde in Produktion komplexer sein)
            next_state = state  # Simplified

            # Max Q-Value für next state
            max_next_q = max(
                [self.q_table.get((next_state, a), 0.0) for a in self._get_possible_actions()],
                default=0.0,
            )

            # Q-Learning Update
            new_q = current_q + self.learning_rate * (
                reward + self.discount_factor * max_next_q - current_q
            )

            self.q_table[(state, action)] = new_q

            logger.debug(
                "q_value_updated",
                state=state,
                action=action,
                old_q=current_q,
                new_q=new_q,
            )

    def get_optimal_action(self, task: Task) -> list[AgentType]:
        """
        Gibt die optimale Aktion für einen Task basierend auf gelernten Q-Values zurück

        Args:
            task: Die Aufgabe

        Returns:
            Liste optimaler Agenten
        """
        state = self._encode_state(task)

        # Epsilon-Greedy Strategy
        if random.random() < self.epsilon:
            # Exploration: Zufällige Aktion
            return random.choice(self._get_possible_actions())
        else:
            # Exploitation: Beste bekannte Aktion
            best_action = max(
                self._get_possible_actions(),
                key=lambda a: self.q_table.get((state, a), 0.0),
            )

            return [AgentType(agent) for agent in best_action]

    async def _evolve_strategies(
        self, decisions: list[OrchestrationDecision]
    ) -> OptimizationResult | None:
        """
        Evolutionäre Algorithmen für Strategieverbesserung

        1. Selection: Wähle beste Strategien
        2. Crossover: Kombiniere Strategien
        3. Mutation: Zufällige Variationen
        """
        self.generation += 1

        # Initialisiere Population wenn leer
        if not self.strategy_population:
            self.strategy_population = [
                {
                    "agents": list(d.selected_agents),
                    "fitness": d.confidence,
                }
                for d in decisions
            ]
            return None

        # 1. Selection - behalte Top 50%
        self.strategy_population.sort(key=lambda x: x["fitness"], reverse=True)
        survivors = self.strategy_population[: len(self.strategy_population) // 2]

        # 2. Crossover - erstelle neue Strategien
        offspring = []
        for i in range(len(survivors)):
            parent1 = survivors[i]
            parent2 = survivors[(i + 1) % len(survivors)]

            # Kombiniere Agent-Listen
            child_agents = list(set(parent1["agents"] + parent2["agents"]))

            offspring.append(
                {
                    "agents": child_agents[:3],  # Limitiere auf 3 Agenten
                    "fitness": (parent1["fitness"] + parent2["fitness"]) / 2,
                }
            )

        # 3. Mutation - zufällige Änderungen
        for strategy in offspring:
            if random.random() < 0.2:  # 20% Mutationsrate
                # Füge zufälligen Agenten hinzu oder entferne einen
                all_agents = list(AgentType)
                if random.random() < 0.5 and len(strategy["agents"]) < 3:
                    strategy["agents"].append(random.choice(all_agents))
                elif len(strategy["agents"]) > 1:
                    strategy["agents"].pop()

        # Neue Population
        self.strategy_population = survivors + offspring

        # Beste Strategie
        best_strategy = self.strategy_population[0]

        result = OptimizationResult(
            strategy_name=f"evolved_gen_{self.generation}",
            performance_before=self.strategy_population[-1]["fitness"],
            performance_after=best_strategy["fitness"],
            improvement=best_strategy["fitness"] - self.strategy_population[-1]["fitness"],
            metadata={
                "generation": self.generation,
                "population_size": len(self.strategy_population),
                "best_agents": [a.value for a in best_strategy["agents"]],
            },
        )

        logger.info(
            "strategy_evolved",
            generation=self.generation,
            improvement=result.improvement,
        )

        return result

    async def _update_predictions(self, task: Task, decisions: list[OrchestrationDecision]) -> None:
        """
        Update Predictive Analytics Modelle

        In Produktion würde hier ein ML-Modell trainiert werden
        """
        # Vereinfacht - würde in Produktion komplexes ML-Modell sein
        logger.debug("predictions_updated", task_id=task.id)

    def _classify_task_type(self, task: Task) -> str:
        """Klassifiziert Task-Typ für A/B Testing"""
        description = task.description.lower()

        if any(keyword in description for keyword in ["code", "program", "develop"]):
            return "coding"
        elif any(keyword in description for keyword in ["research", "analyze", "find"]):
            return "research"
        elif any(keyword in description for keyword in ["create", "design", "write"]):
            return "creative"
        else:
            return "general"

    def _encode_state(self, task: Task) -> str:
        """Encodiert Task-State für Reinforcement Learning"""
        # Vereinfachtes State-Encoding
        return f"{self._classify_task_type(task)}_{task.priority.value}"

    def _get_possible_actions(self) -> list[tuple[str, ...]]:
        """Gibt mögliche Aktionen (Agenten-Kombinationen) zurück"""
        # Vereinfacht - in Produktion würden alle sinnvollen Kombinationen generiert
        return [
            (AgentType.RESEARCH.value,),
            (AgentType.CODE.value,),
            (AgentType.ANALYSIS.value,),
            (AgentType.RESEARCH.value, AgentType.ANALYSIS.value),
            (AgentType.CODE.value, AgentType.SECURITY.value),
        ]

    def _calculate_performance(self, task: Task, decisions: list[OrchestrationDecision]) -> float:
        """Berechnet Performance-Score für eine Task-Ausführung"""
        # Faktoren: Success, Confidence, Speed
        success_factor = 1.0 if task.status.value == "completed" else 0.3

        avg_confidence = sum(d.confidence for d in decisions) / len(decisions) if decisions else 0.5

        # Vereinfacht - würde auch Execution Time berücksichtigen
        return success_factor * avg_confidence

    def get_metrics(self) -> dict[str, Any]:
        """Gibt Optimizer-Metriken zurück"""
        return {
            "ab_experiments": len(self.ab_experiments),
            "q_table_size": len(self.q_table),
            "generation": self.generation,
            "strategy_population_size": len(self.strategy_population),
            "optimizations_performed": len(self.optimization_history),
            "avg_improvement": (
                sum(r.improvement for r in self.optimization_history)
                / len(self.optimization_history)
                if self.optimization_history
                else 0.0
            ),
        }
