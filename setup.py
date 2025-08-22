#!/usr/bin/env python3
"""
Setup script for Test Bot.

This script helps with installation and setup of the Test Bot project.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="test-bot",
    version="1.0.0",
    author="AI Assistant",
    author_email="hello@sketch.dev",
    description="Telegram bot for organizing events and finding friends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/test-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: AsyncIO",
        "Framework :: FastAPI",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.11.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.7.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pre-commit>=3.6.0",
        ],
        "prod": [
            "gunicorn>=21.2.0",
            "sentry-sdk[fastapi]>=1.38.0",
            "prometheus-client>=0.19.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "test-bot=main:main",
            "test-bot-manage=manage:main",
        ],
    },
)
