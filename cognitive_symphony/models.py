"""
Gemeinsame Datenmodelle für Cognitive Symphony
"""

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentType(StrEnum):
    """Typen der spezialisierten Agenten"""

    RESEARCH = "research"
    CODE = "code"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    SECURITY = "security"
    OPTIMIZATION = "optimization"
    HUMAN_INTERFACE = "human_interface"
    CUSTOM = "custom"


class TaskStatus(StrEnum):
    """Status einer Aufgabe"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(StrEnum):
    """Priorität einer Aufgabe"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    """Repräsentiert eine Aufgabe im System"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: AgentType | None = None
    parent_task_id: str | None = None
    subtasks: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    result: Any | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentCapability(BaseModel):
    """Beschreibt eine Fähigkeit eines Agenten"""

    name: str
    description: str
    skill_level: float = Field(ge=0.0, le=1.0)  # 0.0 = novice, 1.0 = expert
    success_rate: float = Field(ge=0.0, le=1.0)
    avg_execution_time: float = 0.0  # in Sekunden


class AgentPerformance(BaseModel):
    """Performance-Metriken eines Agenten"""

    agent_id: str
    agent_type: AgentType
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_success_rate: float = 0.0
    avg_execution_time: float = 0.0
    last_active: datetime = Field(default_factory=datetime.now)
    capabilities: list[AgentCapability] = Field(default_factory=list)


class MemoryEntry(BaseModel):
    """Eintrag im Gedächtnis-System"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["episodic", "semantic", "procedural"]
    content: Any
    embedding: list[float] | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: float = Field(ge=0.0, le=1.0, default=0.5)
    access_count: int = 0
    last_accessed: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OrchestrationDecision(BaseModel):
    """Dokumentiert eine Orchestrierungs-Entscheidung"""

    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    task_id: str
    selected_agents: list[AgentType]
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    alternative_strategies: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    outcome: str | None = None  # success, failure, partial
    learning_feedback: str | None = None


class OptimizationResult(BaseModel):
    """Ergebnis einer Optimierung"""

    optimization_id: str = Field(default_factory=lambda: str(uuid4()))
    strategy_name: str
    performance_before: float
    performance_after: float
    improvement: float
    timestamp: datetime = Field(default_factory=datetime.now)
    applied: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class SymphonyResult(BaseModel):
    """Endergebnis einer Task-Lösung durch Cognitive Symphony"""

    task_id: str
    solution: Any
    status: TaskStatus
    agent_interactions: list[dict[str, Any]] = Field(default_factory=list)
    orchestration_decisions: list[OrchestrationDecision] = Field(default_factory=list)
    learning_insights: dict[str, Any] = Field(default_factory=dict)
    performance_metrics: dict[str, float] = Field(default_factory=dict)
    execution_time: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)
