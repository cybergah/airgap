# Default model: qwen3.6:35b-a3b

One local GPU (16 GB; with Qwen, about 40% of the model runs on the CPU). Success is judged by tests the model never sees.
In every comparison the two sides were run one after the other, in the same session.

## 1. Model against model, real-project set (11 tasks × 3)

| | `gpt-oss:20b` | `qwen3.6:35b-a3b` | Reports |
|---|---|---|---|
| All tasks | 30/33 | 31/33 | `model-gpt-oss-1..3`, `model-qwen36-1..3` |
| `mi_yeni_fonksiyon` (edit `more.py` with 5,659 lines, its `__all__`, and `more.pyi`) | **0/3** | **2/3** | |
| Total time | 32 min | 46 min | |

gpt-oss spent all 30 steps reading `more.py` and never edited it. Qwen found the places. When it failed,
it stopped halfway: it said "now I will edit" without calling a tool, or it asked what the task was.
Five more Qwen runs of that task: 2/5 (`qwen-zor-1..5`).

## 2. The cause: the prompt went past the context

Every failed Qwen run had at least one prompt that reached `num_ctx` (16,384 tokens). No successful run had one.
The history trimmer assumed 3 characters per token, and Qwen splits code into more tokens than that.
When a prompt is too long, Ollama silently drops the oldest messages, including the task, and leaves no room for the reply.

The fix: the agent learns the characters-per-token ratio from Ollama's `prompt_eval_count`, subtracts the tool schemas,
and keeps a quarter of the context free (`KOD_AJANI_SIGDIR=0` restores the old estimate).

| Before → after the fix | Tasks | Before | After | Prompts at the limit | Reports |
|---|---|---|---|---|---|
| `qwen3.6:35b-a3b`, 4 tasks × 5 | all | 16/20 | **20/20** (95% CI 84–100%) | 15 → 0 | `sigdir-eski-1..5`, `sigdir-yeni-1..5` |
| | `mi_yeni_fonksiyon` | 3/5 | **5/5** | | |
| `gpt-oss:20b`, 11 tasks × 3 | all | 26/33 | 24/33 | 9 → 0 | `gpt-sigdir-eski-1..3`, `gpt-sigdir-yeni-1..3` |
| `qwen3.6:35b-a3b`, 11 tasks × 3 | all | 31/33 (section 1) | **32/33** (95% CI 85–99%) | 0 after | `qwen-tam2-1..3` |
| | `mi_yeni_fonksiyon` | 2/3 | 2/3 | | |

The four Qwen tasks were `mi_yeni_fonksiyon`, `mi_partition`, `ck_secenek_sirasi` and `ct_yeni_ozellik`.
The gpt-oss difference is within chance (Fisher p = 0.77); the losses are spread over different tasks, and gpt-oss
itself moved between 7 and 10 out of 11 per round. It still solved `mi_yeni_fonksiyon` 0/3: its problem there is not the context.

## Limits

- The full-set Qwen run after the fix (`qwen-tam2`, 57 min, no timeouts) was on a different day from the "before" run, not alternated with it.
  An earlier attempt (`qwen-tam`, not kept) was invalid: the GPU was thermally throttled and an emulator was running,
  every one of its 15 losses was the 600 s time limit, and it took 4 hours.
- An Android emulator was running during part of the Qwen runs, so the times are not reliable; the median task time rose from 157 s to 250 s,
  partly because the new runs finished the work instead of stopping early.
- Two changes tried before this one did not help and were not kept: an outline of large files instead of a cut in the middle,
  and a rule to edit each place as soon as it is known (gpt-oss, `mi_yeni_fonksiyon`: 0/5 → 0/5 for both).
- We planted these bugs ourselves, so the numbers do not predict results on your own code.
