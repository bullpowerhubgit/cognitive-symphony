# 🎼 Cognitive Symphony - Starter Guide

Willkommen bei **Cognitive Symphony**! Dieses Guide führt Sie durch die ersten Schritte.

## 📋 Inhaltsverzeichnis

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Erste Schritte](#erste-schritte)
4. [Konzepte verstehen](#konzepte-verstehen)
5. [Beispiele](#beispiele)
6. [Nächste Schritte](#nächste-schritte)

---

## Installation

### Voraussetzungen

- **Python 3.11+**
- **API Keys**: OpenAI oder Anthropic
- **Optional**: Redis, Neo4j (für Production)

### Schritt 1: Repository klonen

```bash
git clone https://github.com/bullpull02/cognitive-symphony.git
cd cognitive-symphony
```

### Schritt 2: Virtual Environment

```bash
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Schritt 3: Dependencies installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: Konfiguration

```bash
# Kopiere .env Template
cp .env.example .env

# Bearbeite .env und füge deine API Keys hinzu
```

In `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
DEFAULT_LLM_PROVIDER=openai
ENABLE_LEARNING=true
```

---

## Quick Start

### Ihr erstes Programm

Erstellen Sie `my_first_symphony.py`:

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
    
    # Einfache Aufgabe lösen
    result = await symphony.solve(
        task="Erkläre mir Quantencomputing in einfachen Worten"
    )
    
    print("🎼 Lösung:")
    print(result.solution)
    print(f"\n⏱️  Zeit: {result.execution_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

**Ausführen:**

```bash
python my_first_symphony.py
```

---

## Erste Schritte

### Beispiel 1: Research Task

```python
result = await symphony.solve(
    task="Recherchiere die Top 5 KI-Trends 2025"
)
```

### Beispiel 2: Code Generation

```python
result = await symphony.solve(
    task="Schreibe eine Python-Funktion für Binary Search mit Tests"
)
```

### Beispiel 3: Komplexe Business-Aufgabe

```python
task = {
    "objective": "Entwickle eine Strategie für ein neues SaaS-Produkt",
    "requirements": [
        "Marktanalyse",
        "Technische Machbarkeit",
        "Sicherheitsaspekte",
        "Marketing-Plan"
    ]
}

result = await symphony.solve(task, optimization_level="high")
```

---

## Konzepte verstehen

### 🧠 Meta-Orchestrator

Der "Dirigent" des Systems - koordiniert alle Agenten und lernt kontinuierlich.

```python
# Automatische Task-Zerlegung
# Der Orchestrator zerlegt komplexe Aufgaben intelligent
```

### 🤖 Spezialisierte Agenten

7 Agenten mit unterschiedlichen Fähigkeiten:

| Agent | Spezialisierung |
|-------|----------------|
| 🔍 Research | Web-Recherche, Wissensbasis |
| 💻 Code | Programmierung, Testing |
| 📊 Analysis | Datenanalyse, Patterns |
| 🎨 Creative | Content, Design |
| 🔒 Security | Sicherheitsprüfung |
| ⚡ Optimization | Performance-Tuning |
| 👤 Human Interface | Kommunikation |

### 🧠 Tri-Layer Memory

```python
# Das System erinnert sich an:
# 1. Episodisches Gedächtnis: Was ist passiert?
# 2. Semantisches Gedächtnis: Was weiß ich?
# 3. Prozedurales Gedächtnis: Wie mache ich das?
```

### 📈 Self-Optimization

Das System wird automatisch besser:

```python
# A/B Testing: Testet verschiedene Strategien
# Reinforcement Learning: Lernt aus Erfolgen/Fehlern
# Evolution: Entwickelt neue Lösungsansätze
```

---

## Beispiele

### Performance-Analyse

```python
# Mehrere Tasks ausführen
for task in ["Task 1", "Task 2", "Task 3"]:
    await symphony.solve(task)

# Performance analysieren
performance = await symphony.analyze_performance()

print(f"Erfolgsrate: {performance['orchestrator']['success_rate']:.1%}")
print(f"Durchschnitt Entscheidungen: {performance['orchestrator']['total_decisions']}")
```

### Transparenz-Report

```python
result = await symphony.solve("Ihre Aufgabe")

# Vollständige Transparenz
report = symphony.get_transparency_report(result.task_id)

print("Entscheidungen:", len(report['decisions']))
print("Begründungen:", report['reasoning'])
```

### Custom Context

```python
result = await symphony.solve(
    task="Optimiere diese API",
    context={
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "current_latency": "500ms",
        "target_latency": "100ms"
    }
)
```

---

## Nächste Schritte

### 📚 Dokumentation

- [API Reference](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Architecture Overview](./docs/ARCHITECTURE.md)

### 🎯 Erweiterte Features

1. **Adaptive Agent Synthesis**
   ```python
   from cognitive_symphony.synthesis import AdaptiveAgentSynthesizer
   
   # Erstelle spezialisierte Agenten on-the-fly
   synthesizer = AdaptiveAgentSynthesizer(llm, agent_fleet)
   custom_agent = await synthesizer.auto_synthesize_for_task(task)
   ```

2. **Memory Management**
   ```python
   # Speichere wichtige Erkenntnisse
   symphony.memory_system.store_knowledge(
       knowledge={"best_practice": "Always validate input"},
       tags=["security", "coding"],
       importance=0.9
   )
   ```

3. **Custom Optimization**
   ```python
   # Hole optimale Strategie
   optimal_agents = symphony.self_optimizer.get_optimal_action(task)
   ```

### 🤝 Community

- **GitHub**: [Issues](https://github.com/bullpull02/cognitive-symphony/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bullpull02/cognitive-symphony/discussions)
- **Email**: bullpull02@gmail.com

### 🎓 Best Practices

1. **Spezifische Tasks**: Je detaillierter, desto besser
2. **Context nutzen**: Geben Sie relevante Informationen
3. **Learning aktivieren**: System lernt kontinuierlich
4. **Transparenz**: Nutzen Sie Reports für Insights

---

## Troubleshooting

### Problem: API Rate Limit

```python
# Lösung: Timeout erhöhen
from cognitive_symphony.config import settings
settings.task_timeout_seconds = 600
```

### Problem: Langsame Performance

```python
# Lösung: Optimization Level anpassen
result = await symphony.solve(task, optimization_level="low")
```

### Problem: Memory Issues

```python
# Lösung: Memory Retention reduzieren
settings.memory_retention_days = 30
```

---

## 🎉 Viel Erfolg!

Sie sind jetzt bereit, Cognitive Symphony zu nutzen!

**Tipp**: Starten Sie mit einfachen Tasks und steigern Sie die Komplexität.

Bei Fragen:
- 📖 Siehe [API Dokumentation](./docs/API.md)
- 💬 Öffnen Sie ein [GitHub Issue](https://github.com/bullpull02/cognitive-symphony/issues)
- 📧 Email: bullpull02@gmail.com

---

**Cognitive Symphony** - Orchestrieren Sie Ihre KI-Zukunft! 🎼✨
