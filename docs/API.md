# API Dokumentation - Cognitive Symphony

## Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Installation](#installation)
3. [Schnellstart](#schnellstart)
4. [Core API](#core-api)
5. [Agents API](#agents-api)
6. [Memory System API](#memory-system-api)
7. [Optimization API](#optimization-api)
8. [Transparency API](#transparency-api)

---

## Übersicht

Cognitive Symphony ist ein selbstoptimierendes Meta-Orchestrations-System für Multi-Agent-KI-Ökosysteme.

### Hauptkomponenten

- **CognitiveSymphony**: Haupt-Interface
- **MetaOrchestrator**: Zentrale Koordination
- **AgentFleet**: 7 spezialisierte Agenten
- **MemorySystem**: Tri-Layer Gedächtnis
- **SelfOptimizer**: Kontinuierliche Optimierung
- **AdaptiveAgentSynthesizer**: On-the-fly Agenten-Erstellung

---

## Installation

```bash
pip install -r requirements.txt
```

Konfiguration in `.env`:

```bash
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
DEFAULT_LLM_PROVIDER=openai
```

---

## Schnellstart

```python
from cognitive_symphony import CognitiveSymphony
import asyncio

async def main():
    # System initialisieren
    symphony = CognitiveSymphony(
        llm_provider="openai",
        enable_learning=True,
        enable_transparency=True
    )
    
    # Task lösen
    result = await symphony.solve(
        task="Entwickle eine Web-Anwendung mit Security-Analyse",
        optimization_level="high"
    )
    
    print(result.solution)

asyncio.run(main())
```

---

## Core API

### CognitiveSymphony

Haupt-Interface für das System.

#### Constructor

```python
CognitiveSymphony(
    llm_provider: str = "openai",  # "openai" oder "anthropic"
    enable_learning: bool = True,
    enable_transparency: bool = True
)
```

#### Methods

##### `solve()`

Löst eine komplexe Aufgabe.

```python
async def solve(
    task: Union[str, dict, Task],
    optimization_level: str = "medium",  # "low", "medium", "high"
    context: Optional[Dict[str, Any]] = None
) -> SymphonyResult
```

**Parameters:**
- `task`: Aufgabenbeschreibung (String, Dict oder Task-Objekt)
- `optimization_level`: Optimierungsstufe
- `context`: Zusätzlicher Kontext

**Returns:**
- `SymphonyResult`: Ergebnis mit Lösung, Metriken und Insights

**Example:**

```python
result = await symphony.solve(
    task={
        "objective": "Erstelle eine API",
        "requirements": ["FastAPI", "PostgreSQL", "Docker"]
    },
    optimization_level="high"
)
```

##### `analyze_performance()`

Analysiert System-Performance.

```python
async def analyze_performance() -> Dict[str, Any]
```

**Returns:**
- Performance-Metriken aller Komponenten

**Example:**

```python
performance = await symphony.analyze_performance()
print(performance["orchestrator"]["success_rate"])
```

##### `get_transparency_report()`

Generiert Transparenz-Report für eine Aufgabe.

```python
def get_transparency_report(task_id: str) -> Dict[str, Any]
```

---

### MetaOrchestrator

Zentrale Koordination und Metakognition.

#### Methods

##### `decompose_task()`

Zerlegt komplexe Aufgaben in Subtasks.

```python
async def decompose_task(task: Task) -> List[Task]
```

##### `select_optimal_agents()`

Wählt optimale Agenten für eine Aufgabe.

```python
async def select_optimal_agents(
    task: Task,
    agent_performance_history: Dict[AgentType, Dict[str, float]]
) -> Tuple[List[AgentType], OrchestrationDecision]
```

##### `learn_from_outcome()`

Lernt aus Ergebnissen.

```python
async def learn_from_outcome(
    decision: OrchestrationDecision,
    outcome: str,  # "success", "failure", "partial"
    performance: float  # 0.0 - 1.0
) -> None
```

---

## Agents API

### AgentFleet

Verwaltet alle spezialisierten Agenten.

#### Available Agents

- **ResearchAgent**: Web-Recherche, Wissensbasis
- **CodeAgent**: Programmierung, Testing
- **AnalysisAgent**: Datenanalyse, Mustererkennung
- **CreativeAgent**: Content, Design
- **SecurityAgent**: Sicherheitsprüfung
- **OptimizationAgent**: Performance-Optimierung
- **HumanInterfaceAgent**: Kommunikation

#### Methods

##### `execute_task()`

Führt Task mit ausgewählten Agenten aus.

```python
async def execute_task(
    task: Task,
    selected_agents: List[AgentType]
) -> Any
```

##### `get_agent_capabilities()`

Gibt alle Agenten-Fähigkeiten zurück.

```python
def get_agent_capabilities() -> Dict[str, List[Dict]]
```

**Example:**

```python
capabilities = agent_fleet.get_agent_capabilities()
print(capabilities["code"])
```

---

## Memory System API

### MemorySystem

Tri-Layer Gedächtnis-System.

#### Memory Types

1. **Episodic**: Ereignisse und Erfahrungen
2. **Semantic**: Fakten und Wissen
3. **Procedural**: Workflows und Fähigkeiten

#### Methods

##### `store_episode()`

Speichert Episode im episodischen Gedächtnis.

```python
def store_episode(
    task: Task,
    subtasks: List[Task],
    decisions: List[OrchestrationDecision]
) -> None
```

##### `store_knowledge()`

Speichert Wissen im semantischen Gedächtnis.

```python
def store_knowledge(
    knowledge: Dict[str, Any],
    tags: List[str],
    importance: float = 0.5
) -> None
```

##### `recall_episodes()`

Ruft relevante Episoden ab.

```python
def recall_episodes(
    query: Optional[str] = None,
    limit: int = 10
) -> List[MemoryEntry]
```

**Example:**

```python
# Speichere Wissen
memory.store_knowledge(
    knowledge={"best_practice": "Use async for I/O operations"},
    tags=["python", "performance"],
    importance=0.8
)

# Rufe ab
episodes = memory.recall_episodes(query="python performance")
```

---

## Optimization API

### SelfOptimizer

Kontinuierliche Selbstoptimierung.

#### Features

- A/B Testing
- Reinforcement Learning
- Evolutionäre Algorithmen
- Predictive Analytics

#### Methods

##### `optimize()`

Optimiert System basierend auf Task-Ausführung.

```python
async def optimize(
    task: Task,
    subtasks: List[Task],
    decisions: List[OrchestrationDecision]
) -> Optional[OptimizationResult]
```

##### `get_optimal_action()`

Gibt optimale Aktion basierend auf gelernten Werten.

```python
def get_optimal_action(task: Task) -> List[AgentType]
```

**Example:**

```python
optimizer = SelfOptimizer(enable_ab_testing=True, enable_rl=True)
optimal_agents = optimizer.get_optimal_action(task)
```

---

## Transparency API

### TransparencyTracker

Vollständige Transparenz aller Entscheidungen.

#### Methods

##### `log_decision()`

Loggt Orchestrierungs-Entscheidung.

```python
def log_decision(
    decision: OrchestrationDecision,
    context: Dict[str, Any]
) -> None
```

##### `generate_report()`

Generiert Transparenz-Report.

```python
def generate_report(task_id: str) -> Dict[str, Any]
```

**Example:**

```python
tracker = TransparencyTracker()
tracker.log_decision(decision, context={"user": "admin"})
report = tracker.generate_report(task_id)
```

### PerformanceMonitor

Echtzeit-Performance-Monitoring.

#### Methods

##### `record_metric()`

Zeichnet Metrik auf.

```python
def record_metric(metric_name: str, value: float) -> None
```

##### `get_statistics()`

Gibt Statistiken für Metrik zurück.

```python
def get_statistics(metric_name: str) -> Dict[str, float]
```

---

## Data Models

### Task

```python
class Task:
    id: str
    description: str
    priority: TaskPriority  # LOW, MEDIUM, HIGH, CRITICAL
    status: TaskStatus  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    assigned_agent: Optional[AgentType]
    context: Dict[str, Any]
    result: Optional[Any]
```

### SymphonyResult

```python
class SymphonyResult:
    task_id: str
    solution: Any
    status: TaskStatus
    agent_interactions: List[Dict[str, Any]]
    orchestration_decisions: List[OrchestrationDecision]
    learning_insights: Dict[str, Any]
    performance_metrics: Dict[str, float]
    execution_time: float
```

---

## Best Practices

### 1. Task-Beschreibungen

Seien Sie spezifisch:

```python
# ✅ Gut
task = "Entwickle eine FastAPI-Anwendung mit PostgreSQL-Datenbank, "
       "inklusive User-Authentifizierung und Swagger-Dokumentation"

# ❌ Schlecht
task = "Mache eine App"
```

### 2. Optimization Level

- **low**: Schnelle Ausführung, weniger Optimierung
- **medium**: Ausgewogenes Verhältnis (Standard)
- **high**: Maximum Optimierung, längere Ausführung

### 3. Learning aktivieren

```python
symphony = CognitiveSymphony(
    enable_learning=True,  # System lernt und verbessert sich
    enable_transparency=True  # Vollständige Nachvollziehbarkeit
)
```

### 4. Performance-Monitoring

```python
# Regelmäßig Performance analysieren
performance = await symphony.analyze_performance()

# Optimiere basierend auf Insights
if performance["orchestrator"]["success_rate"] < 0.8:
    # Passe Konfiguration an
    pass
```

---

## Error Handling

```python
from cognitive_symphony.models import TaskStatus

try:
    result = await symphony.solve(task)
    
    if result.status == TaskStatus.FAILED:
        # Handle failure
        for interaction in result.agent_interactions:
            if interaction["status"] == "failure":
                print(f"Failed: {interaction['error']}")
                
except Exception as e:
    logger.error(f"System error: {e}")
```

---

## Advanced Usage

### Custom Agent Synthesis

```python
from cognitive_symphony.synthesis import AdaptiveAgentSynthesizer

synthesizer = AdaptiveAgentSynthesizer(llm, agent_fleet)

# Erstelle speziellen Agenten
custom_agent = await synthesizer.synthesize_agent(
    task=task,
    required_capabilities=["research", "code", "security"]
)

result = await custom_agent.execute_with_metrics(task)
```

### Manual Memory Management

```python
# Speichere wichtige Erkenntnisse
memory.store_knowledge(
    knowledge={"lesson": "Always validate user input"},
    tags=["security", "best-practice"],
    importance=0.9
)

# Rufe für zukünftige Tasks ab
lessons = memory.recall_knowledge(tags=["security"])
```

---

## Configuration

Alle Einstellungen in `cognitive_symphony/config.py`:

```python
class Settings:
    # LLM
    default_llm_provider: str = "openai"
    
    # Performance
    max_concurrent_agents: int = 10
    task_timeout_seconds: int = 300
    
    # Memory
    memory_retention_days: int = 90
    
    # Optimization
    enable_ab_testing: bool = True
    enable_reinforcement_learning: bool = True
```

---

## Support & Resources

- **GitHub**: [cognitive-symphony](https://github.com/bullpull02/cognitive-symphony)
- **Email**: bullpull02@gmail.com
- **Issues**: [Report Issues](https://github.com/bullpull02/cognitive-symphony/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bullpull02/cognitive-symphony/discussions)

---

*Cognitive Symphony - Die Zukunft ist metakognitiv.* 🎼✨
