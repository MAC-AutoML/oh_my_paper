# Local push notes

These notes document how this workspace successfully pushes to `MAC-AutoML/oh_my_paper` without storing credentials in the repository.

## Normal path

```bash
git status --branch --short
git push origin main
```

After pushing, verify local and remote are aligned:

```bash
git rev-list --left-right --count origin/main...HEAD
git ls-remote origin refs/heads/main | cut -f1
git rev-parse HEAD
```

Expected ahead/behind output after a successful push:

```text
0	0
```

## If VSCode Git credential helper fails

In this environment, plain `git push` can fail with a stale VSCode askpass socket, for example:

```text
Missing or invalid credentials.
Error: connect ECONNREFUSED /run/user/0/vscode-git-*.sock
remote: No anonymous write access.
fatal: Authentication failed
```

Use a temporary `GIT_ASKPASS` helper that reads `GITHUB_TOKEN` from the environment or from local shell startup files. Do **not** print the token and do **not** commit the helper.

```bash
set +x
mkdir -p /root/.local/bin
cat > /root/.local/bin/ohmp-git-askpass.sh <<'ASKPASS'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *Password*)
    token="${GITHUB_TOKEN:-}"
    if [ -z "$token" ]; then
      token="$(awk -F= '/^[[:space:]]*export[[:space:]]+GITHUB_TOKEN=/{v=$2; gsub(/["'"'"';[:space:]]/,"",v); print v; exit}' /root/.bashrc /root/.zshrc 2>/dev/null)"
    fi
    printf '%s\n' "$token"
    ;;
  *) printf '\n' ;;
esac
ASKPASS
chmod 700 /root/.local/bin/ohmp-git-askpass.sh

GIT_TERMINAL_PROMPT=0 \
GIT_ASKPASS=/root/.local/bin/ohmp-git-askpass.sh \
git -c credential.helper= \
    -c core.askPass=/root/.local/bin/ohmp-git-askpass.sh \
    push origin main

rm -f /root/.local/bin/ohmp-git-askpass.sh
```

## SSH note

`/root/.ssh/xty_admin` can read the GitHub repository in this environment, but GitHub reports it as a deploy key without write permission. Use HTTPS + `GITHUB_TOKEN` for pushes unless repository permissions change.

## Maintainer safety note

Before pushing, maintainers should run the repository's internal validation suite
and confirm ignored local materials, credentials, runtime state, and local
dependencies are not tracked. Keep raw materials and secrets local-only.
