# Bash Scripts Toolkit (MCP 3D Modeling Automation)

This file provides **copy/paste-ready Bash scripts** for quickly bootstrapping backend/frontend environments, running services, and managing common dev tasks.

> Tip: Put scripts in `scripts/` and run with `bash scripts/<name>.sh`.

---

## 1) `scripts/bootstrap_backend.sh`

Creates a Python venv (or uses existing), installs dependencies, and prepares `.env`.

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

cd "$BACKEND_DIR"

if [ ! -d ".venv" ]; then
  echo "[backend] Creating venv..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
  echo "[backend] Created .env from .env.example"
fi

echo "[backend] Done. Activate with: source backend/.venv/bin/activate"
```

---

## 2) `scripts/run_backend_dev.sh`

Runs FastAPI in reload mode.

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

cd "$BACKEND_DIR"

# shellcheck disable=SC1091
source .venv/bin/activate

export PYTHONUNBUFFERED=1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 3) `scripts/bootstrap_frontend.sh`

Installs npm dependencies.

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

cd "$FRONTEND_DIR"

if [ ! -f package.json ]; then
  echo "[frontend] package.json not found. Are you in the right repo?" >&2
  exit 1
fi

npm install

echo "[frontend] Done. Run dev server with: npm run dev"
```

---

## 4) `scripts/run_frontend_dev.sh`

Runs Vite dev server.

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

cd "$FRONTEND_DIR"

npm run dev -- --host 0.0.0.0 --port 3000
```

---

## 5) `scripts/docker_up_dev.sh`

Brings up dev stack (db/redis/etc.) using Compose.

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Choose your compose file
COMPOSE_FILE="docker-compose.dev.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "Compose file not found: $COMPOSE_FILE" >&2
  exit 1
fi

docker compose -f "$COMPOSE_FILE" up -d

docker compose -f "$COMPOSE_FILE" ps
```

---

## 6) `scripts/docker_down.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

COMPOSE_FILE="docker-compose.dev.yml"

docker compose -f "$COMPOSE_FILE" down
```

---

## 7) `scripts/make_scripts_executable.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

chmod +x "$PROJECT_ROOT"/scripts/*.sh
ls -la "$PROJECT_ROOT"/scripts
```

---

## 8) `scripts/git_new_branch.sh`

Creates a feature branch with a conventional prefix.

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <type> <name>" >&2
  echo "Examples: $0 feat research-integration" >&2
  echo "          $0 docs ubuntu-setup" >&2
  exit 1
fi

TYPE="$1"
NAME="$2"
BRANCH="$TYPE/$NAME"

git checkout -b "$BRANCH"
echo "Created and switched to: $BRANCH"
```

---

## 9) `scripts/git_quick_commit.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"commit message\"" >&2
  exit 1
fi

MSG="$1"

git status

git add -A
git commit -m "$MSG"
```

---

## 10) Project quickstart (manual)

```bash
# 1) services (db/redis)
bash scripts/docker_up_dev.sh

# 2) backend
bash scripts/bootstrap_backend.sh
bash scripts/run_backend_dev.sh

# 3) frontend
bash scripts/bootstrap_frontend.sh
bash scripts/run_frontend_dev.sh
```
