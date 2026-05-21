# notebox · Trae 容器环境

把 notebox 的日常仓库环境构建成镜像，启动后通过 **Trae CN**（或 Cursor）以 SSH 接入，
在容器里 vibe coding。做法严格按照《如何将日常使用的仓库环境构建成 dockerfile，并用
Trae 启动容器？》：业务 Dockerfile 末尾插入一段**可插拔的 SSH 插件块**，并附带
`ssh_plugin/` 两个脚本。

## 目录结构

```
environment/
├── Dockerfile            # 业务镜像（python:3.11-slim）+ 末尾 SSH 插件块
├── ssh_plugin/
│   ├── install_ssh.sh    # 构建期：安装并配置 openssh-server（多发行版自适应）
│   └── entrypoint.sh     # 运行期：后台拉起 sshd，PID 1 常驻，可选跑业务 CMD
├── build.ps1             # Windows 一键构建
├── build.sh              # Linux/macOS/WSL 一键构建
├── ssh_config.example    # ~/.ssh/config 片段（本地 / 远端 ProxyJump 两种）
├── .gitattributes        # 强制 *.sh 用 LF（CRLF 会让容器里的 #!/bin/sh 失效）
└── .gitignore            # 忽略构建期解压出来的 repo/
```

业务代码不在 git 里重复保存，而是构建时由 `build.*` 从 `../repo.zip` 解压到
`./repo/`（`repo.zip` 是业务代码的唯一来源）。

## 快速开始

### 1. 构建镜像

Windows（PowerShell，在本目录下）：

```powershell
.\build.ps1                                  # 镜像名 notebox-trae
# 公司内网无法直连外网时，传代理：
# .\build.ps1 -HttpProxy http://host:port -HttpsProxy http://host:port
```

Linux / macOS / WSL：

```sh
./build.sh                                   # 镜像名 notebox-trae
# HTTP_PROXY=http://host:port HTTPS_PROXY=http://host:port ./build.sh
```

脚本会先把 `../repo.zip` 解压到 `repo/`，再执行 `docker build`。
等价的手动命令：

```sh
cd environment/
mkdir -p repo && unzip -q ../repo.zip -d repo      # 或 Expand-Archive
docker build -t notebox-trae .
```

### 2. 启动容器并暴露 SSH

```sh
docker run -d -p 2222:22 --name notebox notebox-trae
```

容器内 sshd 监听 22，映射到宿主机 **2222**。默认登录：`root` / 密码 `password`
（构建时可用 `--build-arg`/`ENV SSH_PASSWORD=...` 修改）。

### 3. 配置 ~/.ssh/config

把 `ssh_config.example` 里的「本地」块拷进 `~/.ssh/config`：

```sshconfig
Host docker-container
    HostName localhost
    User root
    Port 2222
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

> 容器跑在远端 devbox 上时，改用文件里的 `ProxyJump` 块；本地直接用上面这段即可。

先用普通 ssh 验证能进去：

```sh
ssh docker-container          # 输入密码 password，落在 /app
```

### 4. 用 Trae CN 连接并 vibe coding

Trae → 远程开发 / SSH → 选择 `docker-container`（即 `localhost:2222`）→ 打开 `/app`。
连上后 `/app` 是一个干净的 git 仓库，依赖已装好，可直接：

```sh
pytest -q                                      # 跑测试
python -m scripts.seed && uvicorn app.main:app --host 0.0.0.0   # 起服务
```

## 工作原理

- **业务部分**：`python:3.11-slim`，清华 apt/pip 镜像，装 git/curl/tmux，
  装 `requirements.txt`，把 `repo/` 拷进 `/app`，`git init` 出干净的「initial scene」。
- **SSH 插件块**（Dockerfile 末尾，可整段复制到任何业务 Dockerfile 之后）：
  `COPY ssh_plugin/` → 构建期跑 `install_ssh.sh` 装好 sshd → `EXPOSE 22` →
  `ENTRYPOINT` 设为 `entrypoint.sh`。
- **entrypoint.sh** 后台拉起 sshd，自己作为 PID 1 常驻（转发信号、回收僵尸进程），
  所以即使没有业务 CMD（当前为 SSH-only），容器也不会退出，Trae 随时能连。
  想让容器一启动就自动跑测试，把 Dockerfile 末尾改成 `CMD ["pytest", "-q"]` 即可——
  entrypoint 会在后台跑它，SSH 不受影响。

## 注意事项（来自文档）

- **基础镜像必须是 glibc 系**。`python:3.11-slim` 是 Debian bookworm（glibc）✅。
  **不要**换成 Alpine/musl（`*-alpine`）：TRAE CN 下发的远端 server 依赖 glibc，
  SSH 虽能连上但远端 server 装不起来，典型现象——卡在
  `Preparing local cache package...`、`Check System Requirements` 异常、
  `exit code: 3001`、`Server did not start successfully`。推荐 Debian/Ubuntu/glibc 系。
- **2222 同一时刻只能被一个容器占用**。要切到「另一个项目容器」时：先
  `docker stop notebox && docker rm notebox` 释放 2222，再用新镜像
  `docker run -d -p 2222:22 ...` 起新容器，然后重连 SSH。
  （或给不同项目映射不同宿主机端口，如 `-p 2223:22`，并在 ssh config 里各配一个 Host。）
- **Shell 脚本换行符**：`ssh_plugin/*.sh` 必须是 LF。本目录的 `.gitattributes`
  已强制；在 Windows 上别用会改写换行的编辑器把它们存成 CRLF，否则容器内
  `#!/bin/sh` 会报 `no such file or directory`。

## 可调参数

| 变量 | 时机 | 默认 | 说明 |
| --- | --- | --- | --- |
| `SSH_PASSWORD` | 构建 | `password` | root 登录密码 |
| `SSH_PORT` | 构建 | `22` | 容器内 sshd 端口 |
| `HTTP_PROXY` / `HTTPS_PROXY` | 构建 | 空 | 构建期代理（内网用） |
| `KEEP_ALIVE` | 运行 | `1` | 1=容器常驻；0=经典语义（CMD 退出即停） |
| `SKIP_CMD` | 运行 | `0` | 1=纯 SSH，不跑业务 CMD |
| `ORIG_ENTRYPOINT` | 运行 | 空 | 链式调用基础镜像原有 entrypoint |
