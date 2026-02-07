"""
Agent Fleet - Verwaltet alle spezialisierten Agenten
"""

from typing import Any, Dict, List
import structlog
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from cognitive_symphony.config import settings
from cognitive_symphony.models import AgentType, Task
from cognitive_symphony.agents.research_agent import ResearchAgent
from cognitive_symphony.agents.code_agent import CodeAgent
from cognitive_symphony.agents.analysis_agent import AnalysisAgent
from cognitive_symphony.agents.creative_agent import CreativeAgent
from cognitive_symphony.agents.security_agent import SecurityAgent
from cognitive_symphony.agents.optimization_agent import OptimizationAgent
from cognitive_symphony.agents.human_interface_agent import HumanInterfaceAgent

logger = structlog.get_logger()


class AgentFleet:
    """Verwaltet und koordiniert die Flotte spezialisierter Agenten"""

    def __init__(self, llm_provider: str = "openai"):
        """
        Initialisiert die Agent-Flotte

        Args:
            llm_provider: 'openai' oder 'anthropic'
        """
        self.llm_provider = llm_provider
        self.llm = self._initialize_llm()
        self.agents: Dict[AgentType, Any] = self._initialize_agents()

        logger.info(
            "agent_fleet_initialized",
            agent_count=len(self.agents),
            llm_provider=llm_provider,
        )

    def _initialize_llm(self) -> Any:
        """Initialisiert das Language Model"""
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

    def _initialize_agents(self) -> Dict[AgentType, Any]:
        """Initialisiert alle spezialisierten Agenten"""
        return {
            AgentType.RESEARCH: ResearchAgent(self.llm),
            AgentType.CODE: CodeAgent(self.llm),
            AgentType.ANALYSIS: AnalysisAgent(self.llm),
            AgentType.CREATIVE: CreativeAgent(self.llm),
            AgentType.SECURITY: SecurityAgent(self.llm),
            AgentType.OPTIMIZATION: OptimizationAgent(self.llm),
            AgentType.HUMAN_INTERFACE: HumanInterfaceAgent(self.llm),
        }

    async def execute_task(self, task: Task, selected_agents: List[AgentType]) -> Any:
        """
        Führt eine Aufgabe mit den ausgewählten Agenten aus

        Args:
            task: Die auszuführende Aufgabe
            selected_agents: Liste der einzusetzenden Agenten

        Returns:
            Kombiniertes Ergebnis aller Agenten
        """
        logger.info(
            "executing_task",
            task_id=task.id,
            agents=[a.value for a in selected_agents],
        )

        results = []

        for agent_type in selected_agents:
            if agent_type in self.agents:
                agent = self.agents[agent_type]
                try:
                    result = await agent.execute_with_metrics(task)
                    results.append(result)

                    # Kollaboratives Lernen - Agent teilt Wissen
                    if len(selected_agents) > 1:
                        knowledge = {
                            "task_id": task.id,
                            "findings": result,
                            "agent_type": agent_type.value,
                        }
                        agent.share_knowledge(knowledge)

                except Exception as e:
                    logger.error(
                        "agent_execution_failed",
                        agent_type=agent_type.value,
                        error=str(e),
                    )
                    results.append(
                        {
                            "error": str(e),
                            "agent": agent_type.value,
                        }
                    )

        # Kombiniere Ergebnisse
        if len(results) == 1:
            return results[0]
        else:
            return {
                "combined_results": results,
                "agent_count": len(selected_agents),
                "collaboration": True,
            }

    def get_agent(self, agent_type: AgentType) -> Any:
        """Gibt einen spezifischen Agenten zurück"""
        return self.agents.get(agent_type)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Gibt Performance-Metriken aller Agenten zurück"""
        metrics = {}
        for agent_type, agent in self.agents.items():
            metrics[agent_type.value] = agent.get_performance_metrics()

        return metrics

    def get_agent_capabilities(self) -> Dict[str, List[Dict]]:
        """Gibt alle Fähigkeiten aller Agenten zurück"""
        capabilities = {}
        for agent_type, agent in self.agents.items():
            capabilities[agent_type.value] = [c.dict() for c in agent.capabilities]

        return capabilities
