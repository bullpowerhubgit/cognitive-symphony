# Deployment Guide - Cognitive Symphony

## 🚀 Deployment-Optionen

### 1. Lokale Installation

#### Voraussetzungen
- Python 3.11 oder höher
- Git
- API Keys (OpenAI und/oder Anthropic)

#### Schritte

```bash
# Repository klonen
git clone https://github.com/bullpull02/cognitive-symphony.git
cd cognitive-symphony

# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeiten Sie .env und fügen Sie Ihre API-Keys hinzu
```

#### Verwendung

```python
from cognitive_symphony import CognitiveSymphony
import asyncio

async def main():
    symphony = CognitiveSymphony(
        llm_provider="openai",
        enable_learning=True,
        enable_transparency=True
    )
    
    result = await symphony.solve("Ihre Aufgabe hier")
    print(result.solution)

asyncio.run(main())
```

---

### 2. Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application Code
COPY cognitive_symphony/ ./cognitive_symphony/
COPY .env.example .env

# Expose ports (falls Web-Interface)
EXPOSE 8000

# Start
CMD ["python", "-m", "cognitive_symphony"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  cognitive-symphony:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_HOST=redis
      - NEO4J_URI=bolt://neo4j:7687
    depends_on:
      - redis
      - neo4j
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  neo4j:
    image: neo4j:5
    environment:
      - NEO4J_AUTH=neo4j/your_password
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data

volumes:
  redis_data:
  neo4j_data:
```

---

### 3. Cloud Deployment (AWS)

#### EC2 Deployment

```bash
# SSH in EC2 Instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Setup
sudo apt update
sudo apt install python3.11 python3.11-venv git -y

# Clone & Install
git clone https://github.com/bullpull02/cognitive-symphony.git
cd cognitive-symphony
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add your API keys

# Run with systemd
sudo nano /etc/systemd/system/cognitive-symphony.service
```

**Service File:**

```ini
[Unit]
Description=Cognitive Symphony
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cognitive-symphony
Environment="PATH=/home/ubuntu/cognitive-symphony/venv/bin"
ExecStart=/home/ubuntu/cognitive-symphony/venv/bin/python -m cognitive_symphony
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable & Start
sudo systemctl enable cognitive-symphony
sudo systemctl start cognitive-symphony
sudo systemctl status cognitive-symphony
```

---

### 4. Kubernetes Deployment

#### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cognitive-symphony
  labels:
    app: cognitive-symphony
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cognitive-symphony
  template:
    metadata:
      labels:
        app: cognitive-symphony
    spec:
      containers:
      - name: cognitive-symphony
        image: bullpull02/cognitive-symphony:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: cognitive-symphony-service
spec:
  selector:
    app: cognitive-symphony
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Apply

```bash
# Create secrets
kubectl create secret generic api-keys \
  --from-literal=openai-key=YOUR_KEY \
  --from-literal=anthropic-key=YOUR_KEY

# Deploy
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods
kubectl get services
```

---

## 🔧 Konfiguration

### Umgebungsvariablen

```bash
# LLM Provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_PROVIDER=openai

# Databases
REDIS_HOST=localhost
REDIS_PORT=6379
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=your_password

# Vector DB (optional)
PINECONE_API_KEY=...
WEAVIATE_URL=http://localhost:8080

# Performance
MAX_CONCURRENT_AGENTS=10
TASK_TIMEOUT_SECONDS=300

# Optimization
ENABLE_AB_TESTING=true
ENABLE_REINFORCEMENT_LEARNING=true
```

---

## 📊 Monitoring & Logging

### Prometheus Metrics

```python
from prometheus_client import start_http_server, Counter, Histogram

# Start metrics server
start_http_server(9090)

# Metrics werden automatisch exportiert
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()
logger.info("task_completed", task_id=task.id, duration=duration)
```

---

## 🔒 Sicherheit

### Best Practices

1. **API Keys**
   - Nie im Code speichern
   - Immer Umgebungsvariablen oder Secrets Manager nutzen

2. **Network Security**
   - Firewall-Regeln konfigurieren
   - HTTPS/TLS verwenden

3. **Access Control**
   - IAM Rollen (AWS)
   - RBAC (Kubernetes)

---

## 🧪 Testing vor Deployment

```bash
# Unit Tests
pytest tests/ -v

# Coverage
pytest --cov=cognitive_symphony tests/

# Integration Tests
pytest tests/integration/ -v

# Load Tests
locust -f tests/load/locustfile.py
```

---

## 📈 Skalierung

### Horizontale Skalierung

```bash
# Kubernetes
kubectl scale deployment cognitive-symphony --replicas=10

# Docker Compose
docker-compose up --scale cognitive-symphony=5
```

### Performance-Optimierung

1. **Caching**: Redis für häufige Queries
2. **Load Balancing**: Nginx/HAProxy
3. **Database Optimization**: Indizes, Connection Pooling
4. **Async Processing**: Celery für Background Tasks

---

## 🔄 Updates & Wartung

### Rolling Updates (Kubernetes)

```bash
kubectl set image deployment/cognitive-symphony \
  cognitive-symphony=bullpull02/cognitive-symphony:v0.2.0

kubectl rollout status deployment/cognitive-symphony
```

### Backup

```bash
# Redis Backup
redis-cli BGSAVE

# Neo4j Backup
neo4j-admin backup --backup-dir=/backups
```

---

## 🆘 Troubleshooting

### Häufige Probleme

**Problem**: API Rate Limits
```bash
# Lösung: Rate Limiting implementieren
from ratelimit import limits, sleep_and_retry
```

**Problem**: Memory Issues
```bash
# Lösung: Ressourcen erhöhen oder Batch-Größe reduzieren
MAX_CONCURRENT_AGENTS=5
```

**Problem**: Slow Performance
```bash
# Lösung: Profiling
python -m cProfile -o profile.stats your_script.py
```

---

## 📞 Support

Bei Problemen:
- GitHub Issues: https://github.com/bullpull02/cognitive-symphony/issues
- Email: bullpull02@gmail.com

---

**Cognitive Symphony** - Bereit für Production! 🎼✨
