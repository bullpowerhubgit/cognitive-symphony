"""
Tests für Agenten
"""

import pytest
from cognitive_symphony.agents.code_agent import CodeAgent
from cognitive_symphony.agents.research_agent import ResearchAgent
from cognitive_symphony.models import Task
from langchain_openai import ChatOpenAI


@pytest.fixture
def llm():
    """LLM Fixture"""
    return ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)


@pytest.mark.asyncio
async def test_code_agent_execution(llm):
    """Test CodeAgent Ausführung"""
    agent = CodeAgent(llm)
    task = Task(description="Schreibe eine Python-Funktion für Fibonacci")

    result = await agent.execute_with_metrics(task)

    assert result is not None
    assert agent.performance.tasks_completed == 1


@pytest.mark.asyncio
async def test_research_agent_execution(llm):
    """Test ResearchAgent Ausführung"""
    agent = ResearchAgent(llm)
    task = Task(description="Recherchiere KI-Trends 2025")

    result = await agent.execute_with_metrics(task)

    assert result is not None
    assert "type" in result
    assert result["type"] == "research_result"


def test_agent_capabilities(llm):
    """Test Agenten-Capabilities"""
    agent = CodeAgent(llm)

    assert len(agent.capabilities) > 0
    assert all(cap.skill_level > 0 for cap in agent.capabilities)
