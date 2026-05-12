# Difficulty scoring detail (notebox)

Per spec appendix A — four dimensions 0/1/2 summed and mapped:
0–2 简单, 3–5 中等, 6–8 困难.

| # | 需求清晰度 | 修改范围 | 环境/依赖复杂度 | 验证复杂度 | 总分 | 分级 | category |
|---|:---:|:---:|:---:|:---:|:---:|:----:|----|
| 1 | 0 | 0 | 1 | 1 | 2 | 简单 | 功能迭代 |
| 2 | 0 | 1 | 1 | 1 | 3 | 中等 | Bug修复/调试 |
| 3 | 0 | 0 | 0 | 0 | 0 | 简单 | 代码理解与分析 |
| 4 | 0 | 1 | 1 | 1 | 3 | 中等 | 测试 |
| 5 | 0 | 1 | 1 | 1 | 3 | 中等 | 功能迭代 |
| 6 | 0 | 1 | 1 | 1 | 3 | 中等 | 代码重构 |
| 7 | 1 | 1 | 2 | 2 | 6 | 困难 | DevOps/工程化 |
| 8 | 1 | 2 | 1 | 2 | 6 | 困难 | 功能迭代 |
| 9 | 0 | 1 | 0 | 1 | 2 | 简单 | 代码生成 |
| 10 | 0 | 1 | 1 | 1 | 3 | 中等 | 测试 |
| 11 | 0 | 1 | 1 | 1 | 3 | 中等 | 测试 |
| 12 | 0 | 0 | 1 | 1 | 2 | 简单 | 代码理解与分析 |
| 13 | 0 | 1 | 1 | 1 | 3 | 中等 | 功能迭代 |
| 14 | 1 | 2 | 1 | 2 | 6 | 困难 | 代码重构 |
| 15 | 1 | 2 | 2 | 2 | 7 | 困难 | DevOps/工程化 |
| 16 | 0 | 1 | 1 | 1 | 3 | 中等 | 代码生成 |

Distribution: 简单 5 / 中等 7 / 困难 4 (16 total).

Category counts: 代码生成 2, Bug修复/调试 1, 代码理解与分析 2, 测试 3,
代码重构 2, 功能迭代 4, DevOps/工程化 2 — all seven categories covered.

Notes:
- Task #2 is now scored 中等 (raised from 简单) because the fix touches
  app/db.py (SQLAlchemy event listener) **and** app/api/tags.py **and**
  adds a new pytest using raw SQL.
- Task #10 was originally a Bug-fix prompt; after host testing showed
  the dedupe was already fixed in source, the prompt was re-scoped to a
  test-补全 task targeting whitespace + duplicate-name edge cases.
