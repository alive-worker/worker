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

Distribution: 简单 3 / 中等 3 / 困难 2.

Notes:
- Task #2 (tag delete cascade bug) scores low on modification range because
  the fix is localised to one function plus one new test case.
- Task #7 / #8 score 困难 because they change the build/runtime contract or
  introduce a new SQLite feature (FTS5) that also requires data migration.
