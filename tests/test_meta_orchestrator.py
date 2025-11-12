"""
Tests für den MetaOrchestrator
"""

import pytest
from cognitive_symphony.core.meta_orchestrator import MetaOrchestrator
from cognitive_symphony.models import Task, TaskPriority, AgentType


@pytest.fixture
def orchestrator():
    """Fixture für MetaOrchestrator"""
    return MetaOrchestrator(llm_provider="openai", enable_learning=True)


@pytest.mark.asyncio
async def test_task_decomposition(orchestrator):
    """Test Task-Dekomposition"""
    task = Task(
        description="Entwickle eine Web-Anwendung mit Backend und Frontend",
        priority=TaskPriority.HIGH,
    )

    subtasks = await orchestrator.decompose_task(task)

    assert len(subtasks) > 0
    assert all(isinstance(t, Task) for t in subtasks)


@pytest.mark.asyncio
async def test_agent_selection(orchestrator):
    """Test Agenten-Auswahl"""
    task = Task(
        description="Schreibe Python-Code für eine API",
        priority=TaskPriority.MEDIUM,
    )

    agent_performance = {}
    selected_agents, decision = await orchestrator.select_optimal_agents(
        task, agent_performance
    )

    assert len(selected_agents) > 0
    assert all(isinstance(a, AgentType) for a in selected_agents)
    assert decision.confidence > 0.0


def test_performance_metrics(orchestrator):
    """Test Performance-Metriken"""
    metrics = orchestrator.get_performance_metrics()

    assert "total_decisions" in metrics
    assert "success_rate" in metrics
