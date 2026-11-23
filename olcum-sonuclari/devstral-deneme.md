# Trial: devstral-small-2:24b on the hard set

One local GPU (16 GB). Devstral Small 2 (24B, Q4_K_M) ran 15% on the CPU and 85% on the GPU, and generated about 15 tokens/s (Qwen: about 75).
Same set, step limit (30) and time limit (600 s per task) as the Qwen runs `ornek-yeni-1..3`.

The run was stopped after 17 of 27 tasks (round 1 complete, round 2 at 8 of 9). The result was already clear.

| | `devstral-small-2:24b` | `qwen3.6:35b-a3b` |
|---|---|---|
| Solved | 6/17 (35%) | **23/27** (85%) |
| Average time per task | 376 s | 233 s |
| Hit the 600 s limit | 4 | 1 |
| Hit the 30-step limit | 5 | 4 |

The difference is not chance (Fisher p = 0.001).

| Task | Devstral | Qwen |
|---|---|---|
| `zc_anahtar` | 2/2 | 3/3 |
| `zc_peek` | 0/2 | 1/3 |
| `zc_istatistik` | 0/2 | 3/3 |
| `zm_chunked_none` | 2/2 | 3/3 |
| `zm_running_sum` | 0/2 | 3/3 |
| `zm_windowed_adim` | 0/2 | 2/3 |
| `zk_envvar_oncelik` | 0/2 | 3/3 |
| `zk_iki_hata` | 1/2 | 3/3 |
| `zk_yeni_tip` | 1/1 | 2/3 |

Of the 11 losses, 4 were the time limit and could be partly due to speed. The other 7 were not: 5 ran out of steps
and 2 stopped within a minute (`zk_envvar_oncelik`, both rounds: the model repeated the same search until the agent stopped it).

## Limits

- Not alternated with Qwen: the Qwen runs were earlier the same day.
- The GPU ran at 72–86 °C (median 83 °C), hotter than during the Qwen runs.
- We planted these bugs ourselves.

Reports: `devstral-1` (round 1), `devstral-2.ara.jsonl` (round 2, partial).
