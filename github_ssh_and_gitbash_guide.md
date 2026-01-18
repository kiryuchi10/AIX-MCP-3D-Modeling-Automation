# GitHub SSH + Git Bash / Linux Git Setup Guide

This guide covers:
- Creating SSH keys
- Connecting to GitHub via SSH
- Registering Git identity (username/email)
- Common Git Bash commands and workflows

Works for **Ubuntu/Linux**, **Git Bash on Windows**, and **macOS** (minor path differences).

---

## 1) Set your Git identity (register username/email)

> This is local configuration stored in `~/.gitconfig`.

```bash
git config --global user.name "YOUR_GITHUB_USERNAME_OR_REAL_NAME"
git config --global user.email "YOUR_EMAIL"

git config --global init.defaultBranch main
```

Verify:

```bash
git config --global --list
```

---

## 2) Generate an SSH key

### Recommended: Ed25519

```bash
ssh-keygen -t ed25519 -C "YOUR_EMAIL"
```

When prompted:
- File location: press Enter for default (`~/.ssh/id_ed25519`)
- Passphrase: recommended (store in a password manager)

Start the ssh-agent and add key:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## 3) Add SSH key to GitHub

Print the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Then in GitHub:
- **Settings → SSH and GPG keys → New SSH key**
- Paste the key contents

---

## 4) Test SSH connection

```bash
ssh -T git@github.com
```

Expected message:
- “Hi <username>! You've successfully authenticated...”

If prompted "Are you sure you want to continue connecting?", type `yes`.

---

## 5) Optional: SSH config for cleaner multi-key setups

Edit `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Example config:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

Permissions:

```bash
chmod 600 ~/.ssh/config
```

---

## 6) Clone using SSH (recommended)

✅ SSH format:

```bash
git clone git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

❌ HTTPS format (works but uses tokens/password managers):

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

## 7) Common Git Bash / Linux commands you will use daily

### Status, add, commit

```bash
git status
git add -A
git commit -m "feat: integrate research pipeline"
```

### Push / Pull

```bash
git push -u origin main

git pull origin main
```

### Branching workflow

```bash
# create feature branch
git checkout -b feat/research-integration

# push branch
git push -u origin feat/research-integration

# switch back
git checkout main
```

### Sync your branch with main

```bash
git checkout feat/research-integration
git fetch origin
git merge origin/main
# or rebase if your team prefers it:
# git rebase origin/main
```

### Clean up local branches

```bash
git branch -d feat/research-integration
```

---

## 8) If you must use HTTPS: GitHub token setup

GitHub removed password auth for HTTPS. Use a Personal Access Token (PAT).

- GitHub → Settings → Developer settings → Personal access tokens
- Create token (scope: `repo` for private repos)

Then use HTTPS clone and enter token as password.

---

## 9) (Optional) GitHub CLI: `gh`

### Install on Ubuntu

```bash
sudo apt-get update -y
sudo apt-get install -y gh
```

Authenticate:

```bash
gh auth login
```

This can also configure SSH keys for you.

---

## 10) Troubleshooting

### A) Permission denied (publickey)

1) Confirm agent has key:

```bash
ssh-add -l
```

2) Ensure GitHub has your public key
3) Ensure correct remote URL:

```bash
git remote -v
```

Fix remote to SSH:

```bash
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

### B) Wrong username/email in commits

```bash
git config --global user.name

git config --global user.email
```

Fix:

```bash
git config --global user.name "NEW_NAME"
git config --global user.email "NEW_EMAIL"
```

---

## 11) Quick checklist

- [ ] `git config --global user.name ...`
- [ ] `git config --global user.email ...`
- [ ] `ssh-keygen -t ed25519 -C "email"`
- [ ] `ssh-add ~/.ssh/id_ed25519`
- [ ] Added public key to GitHub
- [ ] `ssh -T git@github.com` works
- [ ] Clone/push over SSH works

