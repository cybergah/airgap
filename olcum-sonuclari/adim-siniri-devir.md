# Tried and not kept: a handoff note at the step limit

gpt-oss:20b stops on the 30-step limit in about half of its hard-set failures. Two ways to give it more room were compared
with the current limit:

- **60 steps**: the same agent with a 60-step budget.
- **30 + note + 30**: after 30 steps the model writes a short progress note (what it found, what it changed, the next step);
  the history is cleared and it continues for 30 more steps from the task and that note only.

Hard set, 9 tasks × 3, the three arms alternated in the same session, 600 s per task.

| | 30 steps (kept) | 60 steps | 30 + note + 30 |
|---|---|---|---|
| Solved | 11/27 | 11/27 | 12/27 |
| Stopped on the step limit | 14 | 4 | 9 |
| Total time | 28 min | 47 min | 42 min |

No arm is better (Fisher p = 1.0 for every pair). More steps mostly turn a step-limit stop into a later stop:
tasks that need more than 30 steps rarely get solved with 60. The handoff note fired in most long runs and worked
mechanically, but it did not beat a plain 60-step budget and costs half again the time, so it was not kept.
The step limit stays at 30; the remaining failures look like wrong fixes, not lack of steps.

Reports: `gptadim-a30-1..3`, `gptadim-a60-1..3`, `gptadim-ozet-1..3`.
