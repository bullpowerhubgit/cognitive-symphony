"""
Gemeinsame Datenmodelle für Cognitive Symphony
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4


class AgentType(str, Enum):
    """Typen der spezialisierten Agenten"""

    RESEARCH = "research"
    CODE = "code"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    SECURITY = "security"
    OPTIMIZATION = "optimization"
    HUMAN_INTERFACE = "human_interface"
    CUSTOM = "custom"


class TaskStatus(str, Enum):
    """Status einer Aufgabe"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
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
    assigned_agent: Optional[AgentType] = None
    parent_task_id: Optional[str] = None
    subtasks: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


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
    capabilities: List[AgentCapability] = Field(default_factory=list)


class MemoryEntry(BaseModel):
    """Eintrag im Gedächtnis-System"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["episodic", "semantic", "procedural"]
    content: Any
    embedding: Optional[List[float]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: float = Field(ge=0.0, le=1.0, default=0.5)
    access_count: int = 0
    last_accessed: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OrchestrationDecision(BaseModel):
    """Dokumentiert eine Orchestrierungs-Entscheidung"""

    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    task_id: str
    selected_agents: List[AgentType]
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    alternative_strategies: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    outcome: Optional[str] = None  # success, failure, partial
    learning_feedback: Optional[str] = None


class OptimizationResult(BaseModel):
    """Ergebnis einer Optimierung"""

    optimization_id: str = Field(default_factory=lambda: str(uuid4()))
    strategy_name: str
    performance_before: float
    performance_after: float
    improvement: float
    timestamp: datetime = Field(default_factory=datetime.now)
    applied: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SymphonyResult(BaseModel):
    """Endergebnis einer Task-Lösung durch Cognitive Symphony"""

    task_id: str
    solution: Any
    status: TaskStatus
    agent_interactions: List[Dict[str, Any]] = Field(default_factory=list)
    orchestration_decisions: List[OrchestrationDecision] = Field(default_factory=list)
    learning_insights: Dict[str, Any] = Field(default_factory=dict)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    execution_time: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)
