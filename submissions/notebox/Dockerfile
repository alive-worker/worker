# Base image: small, current Python.
FROM python:3.11-slim

# Required by spec: container repo path is /app.
WORKDIR /app

# Minimal system deps. git is required by spec (Git initialisation) and
# useful for any agent task that inspects history. curl/tmux help interactive
# sessions inside the container.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        tmux \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first so they cache across rebuilds.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the repository contents into /app.
COPY . ./

# Ensure /app is a clean git repo at the task starting state.
# Spec requires the container code to be in the agent's initial scene.
RUN git init -q -b main \
    && git config user.email "agent@notebox.local" \
    && git config user.name  "notebox-agent" \
    && git add -A \
    && git commit -q -m "initial scene"

# Default command: drop into a shell so an agent can begin work immediately.
CMD ["/bin/bash"]
