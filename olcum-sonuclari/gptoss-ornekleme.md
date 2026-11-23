# Tried and not kept: OpenAI's sampling settings for gpt-oss:20b

OpenAI recommends temperature 1.0 and top_p 1.0 for gpt-oss. Airgap sends it temperature 0.2.
Hard set, 9 tasks × 3, the two settings alternated in the same session, 30 steps, 600 s per task.

| | temperature 0.2 (kept) | temperature 1.0, top_p 1.0 |
|---|---|---|
| Solved | 11/27 | 10/27 |
| Per round | 4, 3, 4 | 3, 3, 4 |
| Hit the 30-step limit | 15 | 13 |
| Total time | 30 min | 38 min |

No difference in solved tasks (Fisher p = 1.0); the per-task results are nearly identical. The new setting was slower, so gpt-oss keeps temperature 0.2.
Its main problem on this set is the step limit, not the sampling.

Reports: `gptornek-eski-1..3`, `gptornek-yeni-1..3`.
