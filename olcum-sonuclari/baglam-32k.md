# Qwen: 32K context instead of 16K (now the default)

Qwen3.6 35B lost the same four hard-set tasks again and again. Traces (`qweniz-1..3`, `olcum.py --iz`) show that the
16K context runs out:

- **Empty replies.** The model's thinking filled the rest of the context: `done_reason` was `length` and the prompt
  plus the generated tokens came to 16,383, one token under `num_ctx`. No `num_predict` limit is set.
- **The model forgot the task.** In `zc_peek` it read large files in full and the prompt passed 14K tokens within
  3–4 steps. Then it answered "I see you've shared the contents of `__init__.pyi` … what would you like me to do?",
  even though the task was still in the conversation.

`olcum.py --baglam N` now sets `num_ctx` for a run.

The four lost tasks, 3 rounds, with 16K and 32K alternated in the same session, 30 steps and 600 s per task:

| | 16K | 32K |
|---|---|---|
| Solved | 4/12 | 11/12 |
| Fisher p | | 0.009 |
| Total time | 86 min | 63 min |
| Timed out (600 s) | 7 | 1 |
| `ollama ps` | 39% CPU / 61% GPU | 40% CPU / 60% GPU |

- In 7 of the 11 traced 32K tasks the prompt reached 18–24K tokens, which would not fit in 16K.
- The model does not fit the 16 GB GPU at either size (22 GB), so 32K moves almost nothing more to the CPU.
- 32K was faster in total. Each call is slightly slower, but 16K runs wasted their time and hit the 600 s limit.
- These are the four tasks Qwen lost, chosen for that reason. The full hard set must be checked before changing the
  default.

## Full hard set

32K, 9 tasks × 3, against the six 16K rounds already on record (`ornek-yeni-1..3`, `qwensembol-eski-1..3`):

| Task | 16K | 32K |
|---|---|---|
| zc_anahtar, zk_envvar_oncelik, zk_iki_hata, zk_yeni_tip, zm_chunked_none | 29/30 | 15/15 |
| zc_istatistik | 4/6 | 3/3 |
| zm_running_sum | 4/6 | 2/3 |
| zc_peek | 2/6 | 1/3 |
| zm_windowed_adim | 2/6 | 1/3 |
| **Total** | **41/54** | **22/27** |

- Nothing got worse: the five tasks Qwen already solved stayed solved.
- On the full set the gain is within chance (Fisher p = 0.78). The 11/12 on the four lost tasks did not hold up:
  `zc_peek` and `zm_windowed_adim` are still the hardest tasks.
- The 32K rounds took 57 min each, against 35 min for the old 16K rounds. The machine was the cause, not the context
  size. An Android emulator was using the CPU that day, and Qwen runs 40% on the CPU. Two tasks, 16K and 32K
  alternated twice in the same session:

  | | 16K | 32K |
  |---|---|---|
  | Solved | 4/4 | 4/4 |
  | Time | 584 s, 63 calls | 632 s, 67 calls |

  That is 9.3 and 9.4 seconds per call. On that day `zc_anahtar` also took 132–182 s at 16K, against 74 s in the old
  rounds.
- In `zm_running_sum` the model also changed `README.rst` twice at 32K, which the task does not need. One of those
  runs still passed.

32K became the default: the agent, the VS Code setting and the desktop app. Desktop settings that still hold the
old default of 16384 move to 32768 once. A value the user chose stays.

Reports: `qwenbaglam-16384-1..3`, `qwenbaglam-32768-1..3`, `qweniz-1..3`, `qwen32k-1..3`.
