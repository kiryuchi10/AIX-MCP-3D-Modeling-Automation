# Ubuntu (Linux) Installation & Setup Guide

This guide bootstraps a **clean Ubuntu** environment for the MCP 3D Modeling Automation stack (FastAPI backend + React frontend + DB/Redis + Docker), with practical scripts and reproducible tooling.

> Target: Ubuntu 22.04/24.04 LTS (works for most Debian-based distros with minor tweaks)

---

## 0) First-time machine prep

### Update OS packages

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
  build-essential curl wget git unzip zip ca-certificates gnupg lsb-release \
  software-properties-common apt-transport-https
```

### Recommended: time sync & basic tools

```bash
sudo apt-get install -y htop tmux tree jq
```

---

## 1) Git setup (global identity)

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"

git config --global init.defaultBranch main
git config --global pull.rebase false
```

Verify:

```bash
git config --global --list
```

---

## 2) Python (choose ONE approach)

### Option A) Miniconda (recommended for data/ML)

1) Install Miniconda

```bash
cd ~
wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash miniconda.sh
# follow prompts, then restart shell
```

2) Create environment

```bash
conda create -n mcp3d python=3.11 -y
conda activate mcp3d
python -V
```

### Option B) System Python + venv

```bash
sudo apt-get install -y python3 python3-pip python3-venv

python3 -m venv .venv
source .venv/bin/activate
python -V
pip install --upgrade pip
```

---

## 3) Node.js + npm (React frontend)

### Recommended: install via NVM

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# reload shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

nvm install 20
nvm use 20
node -v
npm -v
```

---

## 4) Docker + Docker Compose

### Install Docker Engine (official repo)

```bash
# remove old packages if present
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

# add Docker’s official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Allow running docker without sudo (recommended)

```bash
sudo usermod -aG docker $USER
newgrp docker

docker version
docker compose version
```

---

## 5) Databases & services (local install OR Docker)

### Option A) Use Docker (recommended)

- MySQL, Redis, etc. run via `docker compose`.
- Keep your host OS clean.

### Option B) Install locally (if needed)

#### MySQL Server

```bash
sudo apt-get install -y mysql-server
sudo systemctl enable --now mysql
sudo mysql_secure_installation
```

#### Redis

```bash
sudo apt-get install -y redis-server
sudo systemctl enable --now redis-server
redis-cli ping
```

---

## 6) Blender install (for automation)

### Option A) Snap

```bash
sudo snap install blender --classic
blender --version
```

### Option B) Download official tarball

```bash
mkdir -p ~/tools/blender && cd ~/tools/blender
# download from blender.org manually or with wget (URL changes by version)
# then:
tar -xf blender-*.tar.xz
./blender-*/blender --version
```

---

## 7) Project bootstrap (backend + frontend)

Assuming repo structure:

```
mcp-3d-modeling-automation/
  backend/
  frontend/
```

### Backend (FastAPI)

```bash
cd mcp-3d-modeling-automation/backend

# activate your python env first
# conda activate mcp3d   OR   source ../.venv/bin/activate

pip install -r requirements.txt

# copy env template
cp .env.example .env

uvicorn app.main:app --reload --port 8000
```

### Frontend (React/Vite)

```bash
cd mcp-3d-modeling-automation/frontend
npm install
npm run dev -- --port 3000
```

---

## 8) CUDA / GPU notes (optional)

- If you are using PyTorch3D / diffusion models with GPU, you must install a matching CUDA toolkit and PyTorch build.
- GPU setup varies by NVIDIA driver version and OS.

Minimal check:

```bash
nvidia-smi
```

---

## 9) Common troubleshooting

### A) Permission denied on Docker socket

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### B) Port already in use

```bash
sudo lsof -i :8000
sudo lsof -i :3000
```

### C) pip build failures (missing headers)

```bash
sudo apt-get install -y build-essential python3-dev
```

---

## 10) Recommended baseline versions

- Python: 3.11
- Node: 20 LTS
- Docker Engine: latest stable
- Ubuntu: 22.04+ LTS

---

## Appendix: One-liner install bundle

```bash
sudo apt-get update -y && sudo apt-get upgrade -y && \
sudo apt-get install -y build-essential curl wget git unzip zip ca-certificates gnupg lsb-release software-properties-common apt-transport-https
```
