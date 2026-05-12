# §3.3 验证环境 — self-check

All seven items verified by actually building and running the image.

| # | Check                                | Status | Evidence (Docker 29.4.3, desktop-linux)                                  |
|---|--------------------------------------|--------|--------------------------------------------------------------------------|
| 1 | 镜像可成功构建                        | PASS   | `docker build -t notebox:trial .` → `naming to docker.io/library/notebox:trial done`. |
| 2 | 容器可正常启动                        | PASS   | `docker run --rm notebox:trial bash -lc 'echo ok'` → `ok`.               |
| 3 | 当前工作目录为 `/app`                 | PASS   | `pwd` → `/app`.                                                          |
| 4 | `repo` 存在                          | PASS   | `ls -A /app` → `.git Dockerfile README.md app requirements.txt scripts tests` (no host residue: `.pytest_cache`, `submissions/`, `_docx_extract/` excluded via `.dockerignore`). |
| 5 | `repo` 为 Git 仓库                   | PASS   | `git -C /app rev-parse --is-inside-work-tree` → `true`.                  |
| 6 | 容器内代码为任务起始现场              | PASS   | `git log --oneline` → single commit `initial scene`; `git status --short` → empty (clean tree). |
| 7 | 进入容器后无需额外手工初始化即可开始工作 | PASS   | `python -c "import fastapi,sqlalchemy,pydantic"` resolves; `python -m pytest -q` → `11 passed`. |

## Reproduce locally

```bash
docker build -t notebox:trial .
docker run --rm notebox:trial bash -lc '
  pwd
  git -C /app log --oneline
  git -C /app status --short
  python -m pytest -q
'
```

Expected last line: `11 passed`.

## Notes on the build

- Dockerfile swaps Debian apt + PyPI to Tsinghua mirrors so the image
  builds reliably in mainland-China network conditions; the upstream
  package contents are identical.
- `.dockerignore` excludes the host `.git`, `.pytest_cache`, `submissions/`,
  and Python caches so the in-container `git init` produces a clean
  initial-scene commit rather than re-initialising the host's repository.
