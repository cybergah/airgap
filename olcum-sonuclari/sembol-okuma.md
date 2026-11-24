# Tried and not kept: reading one symbol with read_file

`read_file` got an optional `symbol` argument (function, class or method name, e.g. `Parser.parse`) that returns only
that definition's lines. Python used the syntax tree (decorators and `@overload` groups included); other languages used
definition patterns and brace matching. The current code was compared with it on the hard set, alternated in the same
session, 30 steps, 600 s per task.

| | without symbol (kept) | with symbol |
|---|---|---|
| qwen3.6:35b-a3b, solved | 18/27 | 19/27 |
| qwen3.6:35b-a3b, total time | 105 min | 89 min |
| Tasks where the symbol argument was used | – | 7/27 |
| gpt-oss:20b, solved (1 round) | 5/9 | 3/9 |
| gpt-oss:20b, symbol argument used | – | 0 of 55 file reads |

No difference in solved tasks (Fisher p = 1.0). gpt-oss never used the argument, so its run was stopped after one round.
Qwen used it in 7 tasks, all in more-itertools, and mostly kept reading by line numbers from search results.
The time difference is within run-to-run variation, since the argument was unused in most tasks.
The models already get line numbers from `search_code`, `search_text` and the repository map, so the
argument adds little. It was not kept.

Reports: `qwensembol-eski-1..3`, `qwensembol-yeni-1..3`, `gptsembol-eski-1`, `gptsembol-yeni-1`.
