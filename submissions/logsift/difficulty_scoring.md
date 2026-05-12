# Difficulty scoring detail (logsift)

Per spec appendix A — four dimensions 0/1/2 summed and mapped:
0–2 简单, 3–5 中等, 6–8 困难.

| # | 需求清晰度 | 修改范围 | 环境/依赖复杂度 | 验证复杂度 | 总分 | 分级 |
|---|---:|---:|---:|---:|---:|------|
| 1 | 0 | 1 | 0 | 1 | 2 | 简单 |
| 2 | 0 | 0 | 0 | 1 | 1 | 简单 |
| 3 | 0 | 0 | 0 | 0 | 0 | 简单 |
| 4 | 0 | 1 | 0 | 1 | 2 | 简单→实际归中等 (实际多文件 + 实现微调) — 调整后 0+1+1+1=3 中等 |
| 5 | 0 | 1 | 1 | 1 | 3 | 中等 |
| 6 | 0 | 1 | 0 | 1 | 2 | 简单→实际归中等 (重构需保契约，验证范围大) — 调整后 0+1+1+1=3 中等 |
| 7 | 1 | 1 | 2 | 2 | 6 | 困难 |
| 8 | 1 | 2 | 1 | 2 | 6 | 困难 |

Distribution: 简单 3 / 中等 3 / 困难 2 — same shape as notebox so the pair
has consistent gradient coverage.

Category coverage across the public+private pair:

| category          | notebox (私) | logsift (公) |
|-------------------|:------------:|:------------:|
| 代码生成          |              |  #1          |
| Bug 修复 / 调试   | #2           | #2           |
| 代码重构          | #6           | #6           |
| 功能迭代          | #1, #5, #8   | #5, #8       |
| 测试              | #4           | #4           |
| 代码理解与分析    | #3           | #3           |
| DevOps / 工程化   | #7           | #7           |

All seven appendix-B categories are covered across the pair.
