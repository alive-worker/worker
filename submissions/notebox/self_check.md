# §3.3 验证环境 — self-check

Spec requires seven items. Below is what was verified, how, and what is still
pending physical execution.

| # | Check                                | Status        | Evidence                                                                 |
|---|--------------------------------------|---------------|--------------------------------------------------------------------------|
| 1 | 镜像可成功构建                        | PENDING       | Docker engine not present on the authoring machine; build to be re-run before final upload. Dockerfile statically reviewed: valid syntax, all referenced files exist. |
| 2 | 容器可正常启动                        | PENDING       | Same as #1. Default CMD is `/bin/bash`. |
| 3 | 当前工作目录为 `/app`                 | STATIC OK     | `WORKDIR /app` declared on line 5 of Dockerfile.                         |
| 4 | `repo` 存在                          | STATIC OK     | `COPY . ./` copies the whole project into `/app`. `submissions/notebox/repo.zip` also bundles the initial scene for upload per spec field `repo`. |
| 5 | `repo` 为 Git 仓库                   | STATIC OK     | `RUN git init -q -b main && git add -A && git commit ...` lines 24–28.   |
| 6 | 容器内代码为任务起始现场              | STATIC OK     | The committed tree equals the source tree at the moment of build; tests pass on host (`pytest -q` → 11 passed). |
| 7 | 进入容器后无需额外手工初始化即可开始工作 | STATIC OK | Dependencies are pip-installed during build; `python -m scripts.seed` populates sample data on demand. |

## Re-run plan on a Docker host

```bash
docker build -t notebox:trial .
docker run --rm -it notebox:trial bash -lc '
  pwd                          # expect /app
  test -d /app && echo repo-ok
  git -C /app rev-parse --is-inside-work-tree
  python -c "import fastapi, sqlalchemy; print(fastapi.__version__, sqlalchemy.__version__)"
  python -m pytest -q
'
```

All seven items should report OK once docker is available.

## Host-side checks already done

- `pytest -q` → 11 passed (host Python 3.12, requirements installed).
- All Python modules import cleanly.
- `requirements.txt` pins exact versions; reproducible.
