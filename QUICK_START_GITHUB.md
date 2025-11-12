# 🚀 Quick Start: GitHub Upload

Dieser Guide hilft Ihnen, **Cognitive Symphony** in 5 Minuten auf GitHub zu veröffentlichen.

---

## Voraussetzungen

- [x] Git installiert ([Download](https://git-scm.com/download/win))
- [x] GitHub Account vorhanden
- [x] Cognitive Symphony Projekt in `C:\cognitive-symphony`

---

## Schritt 1: Git Repository initialisieren

Öffnen Sie PowerShell/CMD und navigieren Sie zum Projekt:

```powershell
cd C:\cognitive-symphony

# Git initialisieren
git init

# Alle Dateien hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit: Cognitive Symphony v0.1.0 - Complete self-optimizing multi-agent system"
```

**Erwartete Ausgabe:**
```
[main (root-commit) abc1234] Initial commit: Cognitive Symphony v0.1.0...
 XX files changed, XXXX insertions(+)
 create mode 100644 README.md
 create mode 100644 cognitive_symphony/...
 ...
```

---

## Schritt 2: GitHub Repository erstellen

### Option A: Via GitHub Website (empfohlen)

1. Gehen Sie zu https://github.com/new
2. Füllen Sie aus:
   - **Repository name**: `cognitive-symphony`
   - **Description**: `🎼 Ein selbstoptimierendes Meta-Orchestrations-System für Multi-Agent-KI-Ökosysteme`
   - **Visibility**: Public (oder Private)
   - **Initialize**: ❌ NICHT anklicken (wir haben schon Dateien)
3. Klicken Sie "Create repository"

### Option B: Via GitHub CLI (fortgeschritten)

```powershell
# GitHub CLI installiert?
gh --version

# Repository erstellen
gh repo create cognitive-symphony --public --description "🎼 Ein selbstoptimierendes Meta-Orchestrations-System für Multi-Agent-KI-Ökosysteme"
```

---

## Schritt 3: Remote Repository verbinden

Ersetzen Sie `bullpull02` mit Ihrem GitHub-Username (falls anders):

```powershell
# Remote hinzufügen
git remote add origin https://github.com/bullpull02/cognitive-symphony.git

# Branch auf 'main' umbenennen (falls nötig)
git branch -M main

# Zum GitHub pushen
git push -u origin main
```

**Erwartete Ausgabe:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/bullpull02/cognitive-symphony.git
 * [new branch]      main -> main
```

---

## Schritt 4: Repository konfigurieren

### GitHub Repository Settings

1. Gehen Sie zu: `https://github.com/bullpull02/cognitive-symphony/settings`

2. **About-Sektion** (rechts oben):
   - Description: `🎼 Ein selbstoptimierendes Meta-Orchestrations-System für Multi-Agent-KI-Ökosysteme`
   - Topics: `artificial-intelligence`, `multi-agent-systems`, `llm`, `openai`, `langchain`, `python`, `meta-orchestration`, `self-optimization`

3. **Features aktivieren**:
   - Settings → Features
   - ✅ Issues
   - ✅ Discussions
   - ❌ Projects (optional)
   - ❌ Wiki (haben wir Docs)

4. **Branch Protection** (empfohlen):
   - Settings → Branches → Add rule
   - Branch name pattern: `main`
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass

---

## Schritt 5: GitHub Release erstellen

### Via GitHub Website

1. Gehen Sie zu: `https://github.com/bullpull02/cognitive-symphony/releases/new`
2. Füllen Sie aus:
   - **Tag**: `v0.1.0`
   - **Release title**: `🎼 Cognitive Symphony v0.1.0 - Initial Release`
   - **Description**: Kopieren Sie aus `CHANGELOG.md` (Version 0.1.0 Section)
3. Klicken Sie "Publish release"

### Via Command Line

```powershell
# Tag erstellen
git tag -a v0.1.0 -m "Release v0.1.0: Initial public release"

# Tag pushen
git push origin v0.1.0

# Dann via GitHub UI Release erstellen (siehe oben)
```

---

## Schritt 6: Verifizierung

Checken Sie:

- [ ] Repository ist sichtbar: `https://github.com/bullpull02/cognitive-symphony`
- [ ] README wird angezeigt (mit Badges)
- [ ] GitHub Actions läuft (Actions-Tab)
- [ ] Issues/Discussions aktiviert
- [ ] Release `v0.1.0` existiert

---

## 🎉 Fertig! Was nun?

### Erste Schritte nach dem Upload

1. **GitHub Actions prüfen**:
   - Gehen Sie zu: Actions-Tab
   - Sollte automatisch `tests.yml` Workflow laufen
   - Falls grün ✅: Alles gut!
   - Falls rot ❌: Logs checken (vermutlich fehlende Secrets)

2. **Secrets konfigurieren** (für CI/CD):
   - Settings → Secrets → Actions → New repository secret
   - Fügen Sie hinzu:
     - `OPENAI_API_KEY` (falls Tests LLMs brauchen)
     - `ANTHROPIC_API_KEY`

3. **Discussions starten**:
   - Discussions → New discussion
   - Titel: "🎼 Cognitive Symphony v0.1.0 ist live!"
   - Announcement posten (siehe `LAUNCH_CHECKLIST.md`)

4. **Social Media** (optional):
   - Twitter/X, LinkedIn, Reddit, etc.
   - Template siehe `LAUNCH_CHECKLIST.md`

---

## 📝 Zukünftige Updates

### Code-Änderungen committen

```powershell
# Änderungen prüfen
git status

# Dateien hinzufügen
git add .

# Commit
git commit -m "Beschreibung der Änderung"

# Push zu GitHub
git push
```

### Neue Release erstellen

```powershell
# Version in CHANGELOG.md aktualisieren
# Dann:

git add .
git commit -m "chore: bump version to 0.2.0"
git tag -a v0.2.0 -m "Release v0.2.0: [Beschreibung]"
git push
git push origin v0.2.0

# GitHub UI: Release für v0.2.0 erstellen
```

---

## 🆘 Troubleshooting

### "Permission denied (publickey)"

**Lösung**: HTTPS statt SSH nutzen oder SSH-Key einrichten.

```powershell
# Aktuelles Remote prüfen
git remote -v

# Falls ssh:// verwendet wird, zu HTTPS wechseln:
git remote set-url origin https://github.com/bullpull02/cognitive-symphony.git
```

### "Nothing to commit"

**Problem**: Keine Änderungen zum committen.

```powershell
# Status prüfen
git status

# Falls alles commitet: Nichts zu tun!
# Falls Dateien fehlen:
git add .
git commit -m "Add missing files"
```

### "Push rejected"

**Lösung**: Erst pullen, dann pushen.

```powershell
git pull origin main --rebase
git push origin main
```

### GitHub Actions schlägt fehl

**Ursache**: Vermutlich fehlende API-Keys in Secrets.

**Lösung**:
1. Settings → Secrets → Actions
2. `OPENAI_API_KEY` und `ANTHROPIC_API_KEY` hinzufügen
3. Oder: Tests so ändern, dass sie ohne echte API-Keys laufen (Mocks)

---

## 📚 Weitere Ressourcen

- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Guides](https://guides.github.com/)
- [GitHub Docs](https://docs.github.com/)

---

## 🔗 Wichtige Links

Nach dem Upload:

- **Repository**: `https://github.com/bullpull02/cognitive-symphony`
- **Releases**: `https://github.com/bullpull02/cognitive-symphony/releases`
- **Issues**: `https://github.com/bullpull02/cognitive-symphony/issues`
- **Discussions**: `https://github.com/bullpull02/cognitive-symphony/discussions`
- **Actions**: `https://github.com/bullpull02/cognitive-symphony/actions`

---

## ✅ Quick Checklist

Vor dem Upload:

- [ ] Alle Dateien gespeichert
- [ ] `.env` enthält KEINE echten API-Keys (nur `.env.example` committen!)
- [ ] Tests laufen lokal durch (`pytest`)

Nach dem Upload:

- [ ] README wird korrekt angezeigt
- [ ] Topics/Tags gesetzt
- [ ] Issues/Discussions aktiviert
- [ ] Release erstellt
- [ ] GitHub Actions läuft

---

## 🎊 Gratulation!

Ihr **Cognitive Symphony** Projekt ist jetzt auf GitHub! 🚀

**Nächste Schritte**: Siehe `LAUNCH_CHECKLIST.md`

---

**Viel Erfolg!** 🎼✨

*Bei Fragen: bullpull02@gmail.com*
