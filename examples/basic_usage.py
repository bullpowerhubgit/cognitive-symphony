"""
Beispiele für die Verwendung von Cognitive Symphony
"""

import asyncio
from cognitive_symphony import CognitiveSymphony


async def example_simple_task():
    """Einfaches Beispiel: Research-Aufgabe"""
    print("🎼 Example 1: Simple Research Task\n")

    symphony = CognitiveSymphony(
        llm_provider="openai",
        enable_learning=True,
        enable_transparency=True,
    )

    result = await symphony.solve(
        task="Recherchiere die neuesten Trends in KI-Multi-Agent-Systemen",
        optimization_level="medium",
    )

    print("✅ Task completed!")
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print(f"Agents involved: {len(result.agent_interactions)}")
    print(f"\nSolution Summary:\n{result.solution}\n")


async def example_complex_business_solution():
    """Komplexes Beispiel: Vollständige Business-Lösung"""
    print("🎼 Example 2: Complex Business Solution\n")

    symphony = CognitiveSymphony(
        llm_provider="openai",
        enable_learning=True,
        enable_transparency=True,
    )

    task = {
        "objective": "Entwickle eine innovative SaaS-Lösung für Projektmanagement",
        "requirements": [
            "Marktanalyse und Wettbewerber-Research",
            "Technische Architektur und Prototyp",
            "Sicherheitsanalyse",
            "Marketing-Strategie",
            "Performance-Optimierung",
        ],
    }

    result = await symphony.solve(task, optimization_level="high")

    print("✅ Complex task completed!")
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print(f"\nAgent Interactions:")
    for interaction in result.agent_interactions:
        print(f"  - {interaction['agents']}: {interaction['status']}")

    print(f"\nLearning Insights:")
    for key, value in result.learning_insights.items():
        print(f"  - {key}: {value}")

    # Transparenz-Report
    print("\n📊 Transparency Report:")
    transparency_report = symphony.get_transparency_report(result.task_id)
    print(f"  - Decisions made: {len(transparency_report.get('decisions', []))}")
    print(f"  - Confidence scores: {transparency_report.get('confidence_scores', [])}")


async def example_adaptive_agent_synthesis():
    """Beispiel: Adaptive Agenten-Synthese"""
    print("🎼 Example 3: Adaptive Agent Synthesis\n")

    symphony = CognitiveSymphony(
        llm_provider="openai",
        enable_learning=True,
    )

    # Eine ungewöhnliche Aufgabe, die einen speziellen Agenten erfordert
    result = await symphony.solve(
        task="Erstelle eine technische Dokumentation mit interaktiven Code-Beispielen "
        "und visuellen Diagrammen, inklusive Sicherheitsrichtlinien",
        optimization_level="high",
    )

    print("✅ Task completed with synthesized agents!")
    print(f"Solution:\n{result.solution}\n")


async def example_performance_analysis():
    """Beispiel: Performance-Analyse"""
    print("🎼 Example 4: Performance Analysis\n")

    symphony = CognitiveSymphony(llm_provider="openai")

    # Führe mehrere Tasks aus
    tasks = [
        "Analysiere Datentrends",
        "Schreibe Python-Code für API",
        "Erstelle Marketing-Content",
    ]

    for task in tasks:
        await symphony.solve(task)

    # Analysiere Performance
    performance = await symphony.analyze_performance()

    print("📊 System Performance:")
    print(f"\nOrchestrator Metrics:")
    for key, value in performance["orchestrator"].items():
        print(f"  - {key}: {value}")

    print(f"\nAgent Performance:")
    for agent, metrics in performance["agents"].items():
        print(f"  {agent}:")
        print(f"    Success Rate: {metrics.get('success_rate', 0):.2%}")
        print(f"    Tasks Completed: {metrics.get('tasks_completed', 0)}")


async def main():
    """Führe alle Beispiele aus"""
    print("=" * 60)
    print("🎼 COGNITIVE SYMPHONY - EXAMPLES")
    print("=" * 60)
    print()

    # Example 1: Simple Task
    await example_simple_task()

    print("\n" + "=" * 60 + "\n")

    # Example 2: Complex Business Solution
    await example_complex_business_solution()

    print("\n" + "=" * 60 + "\n")

    # Example 3: Adaptive Synthesis
    await example_adaptive_agent_synthesis()

    print("\n" + "=" * 60 + "\n")

    # Example 4: Performance Analysis
    await example_performance_analysis()

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
