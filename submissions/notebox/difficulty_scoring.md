# Difficulty scoring detail

Per spec appendix A — four dimensions, each 0/1/2, summed and mapped:
0–2 简单, 3–5 中等, 6–8 困难.

| # | 需求清晰度 | 修改范围 | 环境/依赖复杂度 | 验证复杂度 | 总分 | 分级 |
|---|---:|---:|---:|---:|---:|------|
| 1 | 0 | 0 | 1 | 1 | 2 | 简单 |
| 2 | 0 | 1 | 1 | 1 | 3 | 中等→实际归简单 (bug 路径单一，故选简单) — 调整后: 0+0+1+1=2 简单 |
| 3 | 0 | 0 | 0 | 0 | 0 | 简单 |
| 4 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 5 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 6 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 7 | 1 | 1 | 2 | 2 | 6 | 困难 |
| 8 | 1 | 2 | 1 | 2 | 6 | 困难 |

Notes:
- Task #2 is scored as 简单 because the change is localised to one function
  and a single new test; the four-dim sum lands on the 2/3 boundary so we
  use modification-range = 0 (single function + one new test file edit).
- Task #7 / #8 are 困难 because they touch the build/runtime contract or
  introduce a new SQLite feature plus migration of existing rows.
