# Qwen: 32K context instead of 16K

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

Reports: `qwenbaglam-16384-1..3`, `qwenbaglam-32768-1..3`, `qweniz-1..3`.
