# Difficulty scoring detail (notebox)

Per spec appendix A — four dimensions 0/1/2 summed and mapped:
0–2 简单, 3–5 中等, 6–8 困难.

| # | 需求清晰度 | 修改范围 | 环境/依赖复杂度 | 验证复杂度 | 总分 | 分级 |
|---|:---:|:---:|:---:|:---:|:---:|:----:|
| 1 | 0 | 0 | 1 | 1 | 2 | 简单 |
| 2 | 0 | 0 | 1 | 1 | 2 | 简单 |
| 3 | 0 | 0 | 0 | 0 | 0 | 简单 |
| 4 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 5 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 6 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 7 | 1 | 1 | 2 | 2 | 6 | 困难 |
| 8 | 1 | 2 | 1 | 2 | 6 | 困难 |
| 9 | 0 | 1 | 0 | 1 | 2 | 简单 |
| 10 | 0 | 0 | 1 | 1 | 2 | 简单 |
| 11 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 12 | 0 | 0 | 1 | 1 | 2 | 简单→实际归中等（理解题但需读多文件） |
| 13 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 14 | 1 | 2 | 1 | 2 | 6 | 困难 |
| 15 | 1 | 2 | 2 | 2 | 7 | 困难 |

Distribution: 简单 5 / 中等 6 / 困难 4.

Notes:
- Tasks #9/#10 keep the difficulty under 3 because they're localised
  endpoint additions or single-function bug fixes.
- Task #12 is a pure reading task but spans `app/main.py`,
  `tests/conftest.py`, and FastAPI lifespan semantics; marked 中等
  for the breadth of context it forces an agent to load.
- Task #15 (alembic) scores the highest because it touches the runtime
  contract (startup ordering), the build (alembic.ini placement), and
  the test setup all at once.
