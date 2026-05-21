# Trae-ready image for the notebox project (Python + FastAPI + SQLAlchemy + SQLite).
#
# This is the business Dockerfile (same as submissions/notebox/Dockerfile) with
# the pluggable SSH block appended at the end so Trae CN / Cursor can attach over
# SSH for vibe coding.
#
# IMPORTANT (TRAE CN compatibility): the base image must be glibc-based.
# python:3.11-slim is Debian "bookworm" (glibc) -> OK. Do NOT switch to an
# Alpine/musl base (e.g. *-alpine): the TRAE CN remote server is built against
# glibc and will fail to start (Preparing local cache package... / exit 3001).
#
# Build context for this Dockerfile is THIS folder (environment/). The business
# code is materialised into ./repo/ from ../repo.zip by build.ps1 / build.sh.

# ---------------------------------------------------------------------------- #
# Business image
# ---------------------------------------------------------------------------- #
FROM python:3.11-slim

# Required by spec: container repo path is /app.
WORKDIR /app

# Optional corporate proxy (uncomment / override with --build-arg if your build
# host has no direct internet access, e.g. on a corporate network):
#   docker build --build-arg HTTP_PROXY=http://host:port --build-arg HTTPS_PROXY=http://host:port -t notebox-trae .
ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""
ENV http_proxy=${HTTP_PROXY} https_proxy=${HTTPS_PROXY} \
    HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY}

# Swap Debian apt sources to a Tsinghua mirror so builds succeed on China
# networks where deb.debian.org is slow/unreachable. Safe on any host.
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources; \
    fi; \
    if [ -f /etc/apt/sources.list ]; then \
        sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list; \
    fi

# Minimal system deps. git is required by spec; curl/tmux help interactive
# sessions inside the container.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        tmux \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first so they cache across rebuilds.
COPY repo/requirements.txt ./
RUN pip install --no-cache-dir \
        -i https://pypi.tuna.tsinghua.edu.cn/simple \
        -r requirements.txt

# Copy the rest of the repository contents into /app.
COPY repo/ ./

# Ensure /app is a clean git repo at the task starting state.
RUN git init -q -b main \
    && git config user.email "agent@notebox.local" \
    && git config user.name  "notebox-agent" \
    && git add -A \
    && git commit -q -m "initial scene"

# ========== SSH plugin (pluggable, for Cursor/Trae vibe coding) ==========
# Drop-in block: copy the same `ssh_plugin/` folder next to this Dockerfile
# and paste this block at the end of any business Dockerfile. Nothing else
# in the business logic needs to change.
#
# Optional customisation (override at build with --build-arg, or set ENV here):
#   ENV SSH_PASSWORD=mysecret           # change root password (default: password)
#   ENV SSH_PORT=22                     # change sshd port     (default: 22)
#   ENV ORIG_ENTRYPOINT=/docker-entrypoint.sh   # chain base image's ENTRYPOINT
#
# NOTE: this block runs as root (required to install sshd). python:3.11-slim
#       already runs as root, so no USER restore is needed.
ENV SSH_PASSWORD=password \
    SSH_PORT=22
USER root
COPY ssh_plugin/ /opt/ssh_plugin/
RUN chmod +x /opt/ssh_plugin/*.sh && /opt/ssh_plugin/install_ssh.sh
EXPOSE 22
ENTRYPOINT ["/opt/ssh_plugin/entrypoint.sh"]
# ========== end SSH plugin ==========

# SSH-only workbox: no business CMD is run on start. Connect via Trae/SSH and
# work in /app. (To auto-run the test suite on start instead, set e.g.
# CMD ["pytest", "-q"] -- the entrypoint runs it in the background, SSH stays up.)
CMD []
