"""
Setup configuration for Cognitive Symphony
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cognitive-symphony",
    version="0.1.0",
    author="bullpull02",
    author_email="bullpull02@gmail.com",
    description="Ein selbstoptimierendes Meta-Orchestrations-System für Multi-Agent-KI-Ökosysteme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bullpull02/cognitive-symphony",
    project_urls={
        "Bug Tracker": "https://github.com/bullpull02/cognitive-symphony/issues",
        "Documentation": "https://github.com/bullpull02/cognitive-symphony/tree/main/docs",
        "Source Code": "https://github.com/bullpull02/cognitive-symphony",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "ruff>=0.1.9",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cognitive-symphony=cognitive_symphony.cli:main",
        ],
    },
    keywords=[
        "ai",
        "artificial-intelligence",
        "multi-agent",
        "orchestration",
        "machine-learning",
        "reinforcement-learning",
        "metakognition",
        "self-optimization",
        "langchain",
        "gpt-4",
        "claude",
    ],
    include_package_data=True,
    zip_safe=False,
)
