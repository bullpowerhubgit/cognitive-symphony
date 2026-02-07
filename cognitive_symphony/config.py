"""
Konfigurationsmanagement für Cognitive Symphony
"""

from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Hauptkonfiguration für Cognitive Symphony"""

    # LLM Provider
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: Literal["openai", "anthropic"] = "openai"

    # Vector Database
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    weaviate_url: str = "http://localhost:8080"
    weaviate_api_key: str = ""

    # Graph Database
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    # Authentication
    jwt_secret_key: str = "change-this-to-a-secure-random-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # System Configuration
    enable_learning: bool = True
    enable_transparency: bool = True
    log_level: str = "INFO"

    # Performance Settings
    max_concurrent_agents: int = 10
    task_timeout_seconds: int = 300
    memory_retention_days: int = 90

    # Optimization Settings
    enable_ab_testing: bool = True
    enable_reinforcement_learning: bool = True
    optimization_interval_hours: int = 24

    class Config:
        env_file = ".env"
        case_sensitive = False


# Globale Settings-Instanz
settings = Settings()
