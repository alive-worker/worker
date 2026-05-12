# notebox

> [English](#english) ｜ [中文](#中文)

---

## English

A small but real personal-notes HTTP API. Each note has a title, a markdown
body, and any number of tags. The service exposes CRUD over notes and tags,
simple keyword search, and export to JSON / Markdown.

The project is intentionally compact (~700 lines of Python) but layered the
same way a real internal service would be: routers, schemas, models, services,
tests, and a seed script.

### Stack

- Python 3.11
- FastAPI + Uvicorn
- SQLAlchemy 2.x + SQLite
- Pydantic v2
- pytest

### Running locally

```bash
pip install -r requirements.txt
python -m scripts.seed              # creates notebox.db with sample data
uvicorn app.main:app --reload
```

OpenAPI docs at <http://127.0.0.1:8000/docs>.
A minimal in-browser UI is served at <http://127.0.0.1:8000/ui/> (and `/`
redirects there). It is a single static HTML page that talks to the same
HTTP API.

### Running tests

```bash
pytest -q
```

### Running in Docker

```bash
docker build -t notebox .
docker run --rm -it notebox bash
# inside the container: /app is the working directory, dependencies are
# already installed, and `pytest -q` should report 11 passed.
```

### Layout

```
app/
  main.py            FastAPI entry
  db.py              engine / session
  models.py          SQLAlchemy models (Note, Tag, note_tag)
  schemas.py         Pydantic request / response schemas
  api/
    notes.py         /notes router
    tags.py          /tags router
    search.py        /search router
    export.py        /export router
  services/
    search.py        keyword search implementation
    export.py        JSON / Markdown export
scripts/
  seed.py            populate sample notes & tags
tests/
  test_notes.py
  test_tags.py
  test_search.py
```

---

## 中文

一个小而真实的个人笔记 HTTP API。每条笔记包含标题、Markdown 正文，以及任意数量
的标签。服务对外暴露笔记和标签的 CRUD、简单的关键词搜索，以及 JSON / Markdown
两种格式的导出能力。

项目刻意保持精简（约 700 行 Python），但分层方式与一个真实公司内部小型服务一致：
路由、Schema、模型、服务、测试，外加一个种子数据脚本。

### 技术栈

- Python 3.11
- FastAPI + Uvicorn
- SQLAlchemy 2.x + SQLite
- Pydantic v2
- pytest

### 本地运行

```bash
pip install -r requirements.txt
python -m scripts.seed              # 生成 notebox.db 并写入样例数据
uvicorn app.main:app --reload
```

OpenAPI 文档地址：<http://127.0.0.1:8000/docs>。
浏览器极简 UI 地址：<http://127.0.0.1:8000/ui/>（访问 `/` 会重定向到这里）。
它是一个单文件静态页面，直接调用同一份 HTTP API。

### 跑测试

```bash
pytest -q
```

### 在 Docker 中运行

```bash
docker build -t notebox .
docker run --rm -it notebox bash
# 进入容器后：工作目录是 /app，依赖已安装好，
# 执行 `pytest -q` 应该输出 11 passed。
```

### 目录结构

```
app/
  main.py            FastAPI 入口
  db.py              engine / session
  models.py          SQLAlchemy 模型 (Note, Tag, note_tag)
  schemas.py         Pydantic 请求 / 响应 schema
  api/
    notes.py         /notes 路由
    tags.py          /tags 路由
    search.py        /search 路由
    export.py        /export 路由
  services/
    search.py        关键词搜索实现
    export.py        JSON / Markdown 导出
scripts/
  seed.py            写入样例笔记与标签
tests/
  test_notes.py
  test_tags.py
  test_search.py
```
