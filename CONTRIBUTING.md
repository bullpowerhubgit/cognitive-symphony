# Contributing to Cognitive Symphony

Vielen Dank für Ihr Interesse an Cognitive Symphony! 🎼

## Wie Sie beitragen können

### 1. Code-Beiträge

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

### 2. Bug Reports

Bitte erstellen Sie ein Issue mit:
- Beschreibung des Problems
- Schritte zur Reproduktion
- Erwartetes vs. tatsächliches Verhalten
- System-Informationen

### 3. Feature Requests

Wir freuen uns über Vorschläge! Beschreiben Sie:
- Das Problem, das gelöst werden soll
- Ihre vorgeschlagene Lösung
- Alternativen, die Sie in Betracht gezogen haben

## Entwicklungs-Guidelines

### Code-Style

Wir verwenden:
- **Black** für Code-Formatierung
- **Ruff** für Linting
- **MyPy** für Type-Checking

```bash
# Vor dem Commit
black cognitive_symphony/
ruff check cognitive_symphony/
mypy cognitive_symphony/
```

### Testing

```bash
pytest tests/
pytest --cov=cognitive_symphony tests/
```

### Commit-Nachrichten

Folgen Sie dem Format:
```
type(scope): description

[optional body]

[optional footer]
```

Typen: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Code of Conduct

- Respektvoller Umgang
- Konstruktive Kritik
- Inklusives Verhalten

## Lizenz

Mit Ihrem Beitrag stimmen Sie zu, dass Ihre Arbeit unter der MIT-Lizenz lizenziert wird.
