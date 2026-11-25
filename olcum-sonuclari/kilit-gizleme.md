# Tried and not kept: blocking rereads and hiding the reading tools

Traces of gpt-oss:20b failures on the hard set showed the model rereading the same line ranges without editing
(see `okuma-notu.md`). Two hard rules were tried:

- **Reread lock.** If `read_file` asks for lines the model has already read in this task, and the file has not changed
  since, the result is not returned. The model is told the lines are above and to edit now. Reads that history
  compaction has shortened can be read again.
- **Tool hiding.** After 3 reading-only steps in a row with no file changed yet, `read_file`, `search_text`,
  `search_code` and `list_files` are removed from the tool list for one step, with a note to edit, write or run a
  command.

Hard set, 9 tasks × 3, three arms alternated in the same session, 30 steps, 600 s per task.

| | current | lock only | lock + hiding |
|---|---|---|---|
| Solved | 13/27 | 11/27 | 6/27 |
| Fisher p vs current | | 0.79 | 0.09 |
| Finished without changing any file | 7 | 7 | 4 |
| Never attempted an edit | 2 | 5 | 1 |
| Failed edit calls | 31 | 27 | 56 |
| Total time | 33 min | 37 min | 36 min |

What the model did on the step after each trigger:

- **Lock** (42 triggers in the lock-only arm): it read other lines of the file (17) or searched (12). Only 12 times
  did it try an edit, 7 of which applied. The loop moved rather than broke.
- **Hiding** (79 triggers): it called a hidden tool anyway 45 times. It tried an edit 26 times, and 19 of those failed.

The failed edits after hiding were made to look busy, not to fix the task:

- edits where old and new text were the same;
- an added `# debug: print(...)` comment;
- made-up arguments (`line_start`, `commentary`);
- edits that broke Python syntax.

Forcing an edit before the model understands the code gives a wrong edit, not a right one. Neither rule was kept.

Reports: `gptkilit-eski-1..3`, `gptkilit-kilit-1..3`, `gptkilit-ikisi-1..3`.
