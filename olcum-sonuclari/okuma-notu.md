# Tried and not kept: a reminder to edit when nothing is changed halfway

Traces of gpt-oss:20b failures on the hard set (`olcum.py --iz`) showed two patterns:

- In tasks that were lost without any edit, the model spent all 30 steps rereading the same line ranges and repeating
  the same searches.
- `search_text` treated text such as `fail(` as a regular expression and returned an error. The model retried it.

Two changes were tried together:

- When half the steps are used and no file is changed, the model is reminded once to make the edit now, or to answer
  if the task is a question.
- An invalid regular expression in `search_text` is searched as plain text, with a note.

Hard set, 9 tasks × 3, alternated in the same session, 30 steps, 600 s per task.

| | current | with both changes |
|---|---|---|
| Solved | 11/27 | 10/27 |
| Finished without changing any file | 9 | 9 |
| Stopped on the step limit | 13 | 17 |
| Total time | 28 min | 32 min |

The reminder did not change what the model does: as many tasks end without an edit (Fisher p = 1.0 for solved tasks).
Neither change was kept. The plain-text fallback is harmless on its own but showed no measurable effect here.

Reports: `gptokuma-eski-1..3`, `gptokuma-yeni-1..3`; traces: `gptiz-1`.
