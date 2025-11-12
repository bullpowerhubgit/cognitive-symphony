"""
Adaptive Agent Synthesizer - Dynamische Agenten-Erstellung on-the-fly

Erstellt neue spezialisierte Agenten durch:
- Kombination bestehender Agenten-Fähigkeiten
- Zusammenstellung verfügbarer APIs
- Lernen aus erfolgreichen Patterns
"""

from typing import Any, Dict, List
import structlog
from langchain.prompts import ChatPromptTemplate

from cognitive_symphony.agents.base_agent import BaseAgent
from cognitive_symphony.models import AgentCapability, AgentType, Task

logger = structlog.get_logger()


class SynthesizedAgent(BaseAgent):
    """Ein dynamisch erstellter Agent mit kombinierten Fähigkeiten"""

    def __init__(
        self,
        llm: Any,
        name: str,
        description: str,
        capabilities: List[AgentCapability],
        base_agents: List[AgentType],
    ):
        """
        Initialisiert einen synthetisierten Agenten

        Args:
            llm: Language Model
            name: Name des neuen Agenten
            description: Beschreibung der Fähigkeiten
            capabilities: Liste der Fähigkeiten
            base_agents: Basis-Agenten, aus denen synthetisiert wurde
        """
        # Verwende CUSTOM als Typ für synthetisierte Agenten
        super().__init__(AgentType.CUSTOM, llm)

        self.custom_name = name
        self.description = description
        self.base_agents = base_agents
        self.capabilities = capabilities

        logger.info(
            "synthesized_agent_created",
            name=name,
            base_agents=[a.value for a in base_agents],
        )

    def _initialize_capabilities(self) -> List[AgentCapability]:
        """Capabilities werden im Constructor gesetzt"""
        return []

    async def execute(self, task: Task) -> Any:
        """Führt Aufgaben mit kombinierten Fähigkeiten aus"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein spezialisierter Agent mit folgenden Eigenschaften:
                    
                    Name: {agent_name}
                    Beschreibung: {description}
                    
                    Du kombinierst die Fähigkeiten von: {base_agents}
                    
                    Deine Capabilities:
                    {capabilities}
                    
                    Nutze diese kombinierten Fähigkeiten optimal für die Aufgabe.
                    """,
                ),
                ("human", "Aufgabe: {task_description}\nKontext: {context}"),
            ]
        )

        capabilities_str = "\n".join(
            [
                f"- {c.name}: {c.description} (Skill Level: {c.skill_level})"
                for c in self.capabilities
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "agent_name": self.custom_name,
                "description": self.description,
                "base_agents": ", ".join([a.value for a in self.base_agents]),
                "capabilities": capabilities_str,
                "task_description": task.description,
                "context": str(task.context),
            }
        )

        return {
            "type": "synthesized_result",
            "result": response.content,
            "agent": self.custom_name,
            "base_agents": [a.value for a in self.base_agents],
        }


class AdaptiveAgentSynthesizer:
    """
    Synthesizer für dynamische Agenten-Erstellung

    Erstellt on-the-fly neue Agenten durch:
    - Analyse der Task-Anforderungen
    - Kombination passender Basis-Agenten
    - Synthese neuer Capability-Sets
    """

    def __init__(self, llm: Any, agent_fleet: Any):
        """
        Initialisiert den Synthesizer

        Args:
            llm: Language Model
            agent_fleet: Referenz zur Agent-Fleet
        """
        self.llm = llm
        self.agent_fleet = agent_fleet
        self.synthesized_agents: Dict[str, SynthesizedAgent] = {}

        logger.info("adaptive_synthesizer_initialized")

    async def synthesize_agent(
        self, task: Task, required_capabilities: List[str]
    ) -> SynthesizedAgent:
        """
        Synthetisiert einen neuen Agenten basierend auf Task-Anforderungen

        Args:
            task: Die Aufgabe, für die der Agent benötigt wird
            required_capabilities: Liste benötigter Fähigkeiten

        Returns:
            Neu synthetisierter Agent
        """
        logger.info(
            "synthesizing_agent",
            task_id=task.id,
            required_capabilities=required_capabilities,
        )

        # 1. Analysiere welche Basis-Agenten die benötigten Capabilities haben
        suitable_agents = await self._find_suitable_base_agents(required_capabilities)

        # 2. Generiere Namen und Beschreibung
        agent_spec = await self._generate_agent_specification(
            task, required_capabilities, suitable_agents
        )

        # 3. Kombiniere Capabilities
        combined_capabilities = self._combine_capabilities(suitable_agents)

        # 4. Erstelle synthetisierten Agenten
        synthesized_agent = SynthesizedAgent(
            llm=self.llm,
            name=agent_spec["name"],
            description=agent_spec["description"],
            capabilities=combined_capabilities,
            base_agents=suitable_agents,
        )

        # Cache für Wiederverwendung
        self.synthesized_agents[agent_spec["name"]] = synthesized_agent

        logger.info(
            "agent_synthesized",
            name=agent_spec["name"],
            base_agents=[a.value for a in suitable_agents],
        )

        return synthesized_agent

    async def _find_suitable_base_agents(
        self, required_capabilities: List[str]
    ) -> List[AgentType]:
        """
        Findet Basis-Agenten, die die benötigten Capabilities haben

        Args:
            required_capabilities: Benötigte Fähigkeiten

        Returns:
            Liste passender Agent-Typen
        """
        suitable_agents = []

        # Hole alle Agent-Capabilities
        all_capabilities = self.agent_fleet.get_agent_capabilities()

        for agent_type_str, capabilities in all_capabilities.items():
            agent_type = AgentType(agent_type_str)

            # Check ob Agent relevante Capabilities hat
            for capability in capabilities:
                if any(
                    req.lower() in capability["name"].lower()
                    or req.lower() in capability["description"].lower()
                    for req in required_capabilities
                ):
                    if agent_type not in suitable_agents:
                        suitable_agents.append(agent_type)
                    break

        # Fallback: Wenn keine passenden gefunden, nutze generische
        if not suitable_agents:
            suitable_agents = [AgentType.RESEARCH, AgentType.ANALYSIS]

        return suitable_agents[:3]  # Limitiere auf max 3 Basis-Agenten

    async def _generate_agent_specification(
        self,
        task: Task,
        required_capabilities: List[str],
        base_agents: List[AgentType],
    ) -> Dict[str, str]:
        """
        Generiert Name und Beschreibung für den neuen Agenten

        Args:
            task: Die Aufgabe
            required_capabilities: Benötigte Fähigkeiten
            base_agents: Basis-Agenten

        Returns:
            Dict mit 'name' und 'description'
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Du bist ein KI-Architekt, der neue spezialisierte Agenten entwirft.
                    
                    Erstelle einen Namen und eine Beschreibung für einen neuen Agenten, der:
                    - Die folgenden Capabilities benötigt: {capabilities}
                    - Auf diesen Basis-Agenten aufbaut: {base_agents}
                    - Diese Aufgabe erfüllen soll: {task}
                    
                    Der Name sollte:
                    - Prägnant und beschreibend sein
                    - Die Hauptfunktion widerspiegeln
                    - Im Format "XyzAgent" sein
                    
                    Die Beschreibung sollte:
                    - Klar die Fähigkeiten beschreiben
                    - Die Synergie der Basis-Agenten hervorheben
                    - 2-3 Sätze lang sein
                    """,
                ),
                (
                    "human",
                    "Erstelle die Spezifikation für den neuen Agenten.",
                ),
            ]
        )

        chain = prompt | self.llm
        response = await chain.ainvoke(
            {
                "capabilities": ", ".join(required_capabilities),
                "base_agents": ", ".join([a.value for a in base_agents]),
                "task": task.description,
            }
        )

        # Parse Response (vereinfacht)
        content = response.content
        lines = content.split("\n")

        name = "CustomSynthesizedAgent"
        description = content[:200]

        # Versuche Name zu extrahieren
        for line in lines:
            if "name:" in line.lower() or "agent" in line.lower():
                name = line.split(":")[-1].strip()
                if name:
                    break

        return {"name": name, "description": description}

    def _combine_capabilities(
        self, base_agents: List[AgentType]
    ) -> List[AgentCapability]:
        """
        Kombiniert Capabilities mehrerer Basis-Agenten

        Args:
            base_agents: Basis-Agenten

        Returns:
            Kombinierte Capabilities
        """
        combined = []

        for agent_type in base_agents:
            agent = self.agent_fleet.get_agent(agent_type)
            if agent and hasattr(agent, "capabilities"):
                for capability in agent.capabilities:
                    # Reduziere Skill-Level leicht, da synthetisiert
                    adjusted_capability = AgentCapability(
                        name=capability.name,
                        description=capability.description,
                        skill_level=capability.skill_level * 0.9,
                        success_rate=capability.success_rate * 0.85,
                    )
                    combined.append(adjusted_capability)

        return combined

    async def auto_synthesize_for_task(self, task: Task) -> SynthesizedAgent:
        """
        Analysiert eine Aufgabe und synthetisiert automatisch den optimalen Agenten

        Args:
            task: Die Aufgabe

        Returns:
            Synthetisierter Agent
        """
        # Analysiere Task und extrahiere benötigte Capabilities
        required_capabilities = await self._extract_required_capabilities(task)

        # Synthesize Agent
        return await self.synthesize_agent(task, required_capabilities)

    async def _extract_required_capabilities(self, task: Task) -> List[str]:
        """
        Extrahiert benötigte Capabilities aus einer Task-Beschreibung

        Args:
            task: Die Aufgabe

        Returns:
            Liste benötigter Capabilities
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analysiere die folgende Aufgabe und identifiziere die benötigten 
                    Fähigkeiten (Capabilities).
                    
                    Liste nur die Kernfähigkeiten auf, z.B.:
                    - Research
                    - Data Analysis
                    - Code Generation
                    - Security Analysis
                    - Content Creation
                    - Optimization
                    
                    Antworte mit einer kommagetrennten Liste.
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

        # Parse capabilities
        capabilities = [
            cap.strip() for cap in response.content.split(",") if cap.strip()
        ]

        return capabilities[:5]  # Max 5 Capabilities

    def get_synthesized_agents(self) -> Dict[str, SynthesizedAgent]:
        """Gibt alle synthetisierten Agenten zurück"""
        return self.synthesized_agents
