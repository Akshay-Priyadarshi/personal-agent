# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install Poetry
RUN pip install --upgrade pip \
    && pip install uv

# Set work directory
WORKDIR /app

# Copy only dependency files first for caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv venv
RUN uv sync

# Copy the personal_finance_assistant agent code
COPY agents/personal_finance_assistant ./agents/personal_finance_assistant
COPY common_models ./common_models
COPY common_tools ./common_tools
COPY utils ./utils

# Set the entrypoint
CMD ["uv", "run", "agents/personal_finance_assistant"]
