"""
Test-Konfiguration und Fixtures
"""

import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup Test-Umgebung"""
    # Mock API Keys für Tests
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["ANTHROPIC_API_KEY"] = "test-key"


@pytest.fixture
def sample_task():
    """Sample Task für Tests"""
    from cognitive_symphony.models import Task, TaskPriority

    return Task(
        description="Test Task",
        priority=TaskPriority.MEDIUM,
        context={"test": True},
    )
