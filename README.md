<div align="center">

<img src="docs/banner.svg" alt="Airgap: your code never leaves the machine" width="100%">

A security-hardened AI coding agent that runs **100% locally** on [Ollama](https://ollama.com):
as a Windows app, in VS Code and in your terminal. No cloud, no API keys, no telemetry.

[![release](https://img.shields.io/github/v/release/cybergah/airgap?color=00FF41&labelColor=0D1117)](https://github.com/cybergah/airgap/releases/latest)
[![tests](https://github.com/cybergah/airgap/actions/workflows/testler.yml/badge.svg)](https://github.com/cybergah/airgap/actions/workflows/testler.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#quick-start)
[![Runs on Ollama](https://img.shields.io/badge/runs%20on-Ollama-000000)](https://ollama.com)
[![100% local](https://img.shields.io/badge/cloud-none-00FF41)](#security-model)

[Quick start](#quick-start) · [Security model](#security-model) · [Benchmarks](#benchmarks) · [Contributing](CONTRIBUTING.md) · [Türkçe](README.tr.md)

</div>

---

<p align="center">
  <img src="docs/airgap-desktop.gif" alt="A real run of Airgap.exe: gpt-oss:20b runs the failing unittest, reads cart.py, proposes a one-line fix to apply_discount, waits for approval each time, and the tests pass" width="100%">
  <br><sub>A real run of <code>Airgap.exe</code> with <code>gpt-oss:20b</code> on a local GPU. Every command and edit was approved by a human; only the waiting time was shortened.</sub>
  <br><br><a href="https://github.com/cybergah/airgap/releases/latest"><b>⬇ Download Airgap.exe</b></a> · <a href="#quick-start">VS Code and terminal</a>
</p>

```mermaid
flowchart TD
    U(["👤 You"]) -->|task| A["🛡️ Airgap agent"]
    A <-->|localhost| O[("Ollama<br/>model on your GPU")]
    N["📄 AGENTS.md"] -.->|untrusted note,<br/>cannot grant permissions| A
    A --> T{"tool call"}
    T -->|read · search| F["project files"]
    T -->|write · edit| D["diff + your approval"] --> F
    T -->|run_command| C["command analyzer<br/>PowerShell / shlex parser"]
    C -->|risky| R["warning,<br/>no auto-allow"] --> AP
    C --> AP["your approval"]
    AP -->|sandbox on| S[["Docker sandbox<br/>no network · read-only .git<br/>seccomp probed · fails closed"]]
    AP -->|sandbox off| H["your shell"]
```

## Why Airgap?

Cloud coding agents read your whole repository and send it to someone else's servers.
Airgap does the same job with a model running on **your** GPU, and it treats that model the
way a security engineer would: **as untrusted input**.

- 🔒 **Local by design.** Inference through Ollama on your machine. Your code, prompts and secrets stay with you.
- 🧱 **Defense in depth.** Approval gates, a command analyzer built on real shell parsers, prompt-injection-resistant project notes, and an optional network-less Docker sandbox that **fails closed**.
- 📏 **Measured, not hyped.** A 24-task benchmark with hidden tests, plus bugs planted in real open-source projects. The numbers, the confidence intervals and the caveats are published.
- 🧩 **Terminal and VS Code.** A streaming chat panel with diff views and approve/reject buttons, plus in-editor "edit this selection".

## Features

| | |
|---|---|
| **Agent loop** | Reads, edits, runs and verifies with 7 tools: `list_files`, `read_file`, `search_text`, `search_code`, `write_file`, `edit_file`, `run_command` |
| **Approvals** | Every write and every command shows a diff or the exact command line first |
| **Checkpoints** | Every turn can be undone; checkpoints live outside the project and never touch your `.git` |
| **Semantic search** | Local embeddings (`nomic-embed-text`); git-ignored files are never indexed |
| **Repo map** | The most important definitions go to the model every turn (approach adapted from Aider): Python `ast`, Tree-sitter for JavaScript, TypeScript and C#, regex fallback for everything else |
| **Selection edit** | Select code, press **Ctrl+Alt+K**, describe the change, review the diff, apply or reject |
| **Live status** | Streaming answers, visible reasoning, and a status line while the model is busy ("Model writing · 12 s") |
| **Editor context** | The open file, cursor line and selection go with your message, shown under it ("📎 a.py · lines 12–20 selected"). Type `@path/file.py` to attach up to 3 files. Secret and out-of-project files are never sent |
| **Persistent chat** | Close VS Code and the panel and the agent's memory come back, stored only on this machine. "New chat" clears both |
| **Thinking level** | How much reasoning models such as gpt-oss do (`kodAjani.dusunmeSeviyesi`, `--dusunme-seviyesi`). The default is recommended: "low" failed on large tasks in our benchmarks |

## Security model

Airgap assumes the model can be wrong, confused, or manipulated by the files it reads.

**Gates**
- Writing files and running commands require approval. Reading `.env`, key and credential files requires approval too, and they are never indexed or put into the repo map.
- Environment variables whose names contain `TOKEN`, `SECRET`, `PASSWORD`, `API_KEY` and similar are stripped before any command runs.
- Permission rules are read **only** from `%LOCALAPPDATA%\kod-ajani\izinler.json`. A repository cannot grant itself permissions.

**Command analyzer.** Risky commands (deletion, network, package installs, `git push`, paths outside the project) trigger a warning, and "always allow" stops working for them. Detection has two layers: pattern matching, and splitting the command with **PowerShell's own parser** (`shlex` for `sh` inside the sandbox). That catches obfuscations like ``Rem`ove-Item``, `/bin/rm`, `git -C . push` and `[IO.Directory]::Delete(...)`. Commands whose names are computed at runtime, or that cannot be parsed, are flagged.

**Prompt-injection defense.** A project's `AGENTS.md` is given to the model as an *untrusted note from the repository author*, never as rules: it cannot grant permissions or skip approvals. Notes that mention networking, secret files, risky commands or "no approval needed" raise a warning, and notes pointing outside the project or at a secret file are not read at all. This is tested against malicious files (`deneme_enjeksiyon.py`).

**Docker sandbox** (`--korumali`, or `kodAjani.korumaliCalistirma` in VS Code)
- Commands run in an unprivileged container with **no network**. The project is mounted at `/work`; `.git` and similar folders are read-only; secret files appear empty. Your disk, environment variables and the Docker socket are invisible.
- Before the first command, Airgap **actively probes** Docker's seccomp filter by attempting a forbidden syscall (`unshare`). If the probe succeeds or cannot run, every command is rejected. `/proc`'s "Seccomp" line is not trusted, because Docker Desktop reports it as enabled even when the filter is off.
- If Docker is not running or the image is missing, commands are **rejected**, never run on the host.

> **Stay local:** use a model that runs on your machine. Ollama models whose names end in `:cloud` run on remote servers, and so does any `OLLAMA_HOST` that points to another machine.
>
> **Honest limits.** Without the sandbox these rules are not a security boundary: an approved command runs with your privileges, and pattern-based detection can be bypassed. Code generated at runtime cannot be read, only flagged. Even in the sandbox the agent can modify project files, so review changes before running the code yourself.

## Benchmarks

`olcum.py` runs 24 tasks against the real model; success is judged by **tests the model never sees**, and the model's code runs in the sandbox.

| Set | Model | 0.13.1 | 0.14 | 95% CI (0.14) |
|---|---|---|---|---|
| 24 tasks × 3 runs (bug fixes, features, multi-file edits, questions, trap tasks) | `gpt-oss:20b` | 67/72 | **70/72 (97%)** | 90–99% |
| Bugs planted in real projects (click, more-itertools, cachetools) | `gpt-oss:20b` | 25/33 | **28/33 (85%)** | 69–93% |
| The 6 flakiest tasks × 5 | `gpt-oss:20b` | 19/30 | **29/30** | |

**Default model: `qwen3.6:35b-a3b`.** Both models in the same session; for the fix, old and new code were run alternately:

| Set | `gpt-oss:20b` | `qwen3.6:35b-a3b` |
|---|---|---|
| Bugs planted in real projects, 11 × 3 | 30/33 | 31/33 |
| The three-place task in a 5,659-line file (`mi_yeni_fonksiyon`) | 0/3 | 2/3 |
| Same task after fitting the history to the model's real token count | 0/3 | **7/8** (5/5 and 2/3) |
| 4 real-project tasks × 5, before → after that fix | | 16/20 → **20/20** |
| Real projects 11 × 3, before → after that fix | 26/33 → 24/33 (within chance) | 31/33 → **32/33** (95% CI 85–99%) |

Qwen took about 1.5 times as long (57 min against 32 for the 11 × 3 set). The "before" Qwen run and the "after" run were on different days.
Report: [`qwen36-varsayilan.md`](olcum-sonuclari/qwen36-varsayilan.md).

Old and new were run alternately, 3 rounds. The gain comes from keeping the model's reasoning between tool calls;
the static check alone did not help. Full report with the costs (real-project tasks take about a quarter longer):
[`0.14-tam-kontrol.md`](olcum-sonuclari/0.14-tam-kontrol.md). Comparisons with other models (Devstral, Qwen2.5-Coder)
are in [`olcum-sonuclari/`](olcum-sonuclari/).
We planted these bugs ourselves, so the numbers do not predict results on your own code.

## Quick start

**Requirements:** Python 3.10+, git, [Ollama](https://ollama.com), and for the panel, VS Code. Unit tests run on Windows, Linux and macOS; end-to-end use with a real model has been tested on Windows ([reports from other systems welcome](CONTRIBUTING.md)).

```bash
ollama pull qwen3.6:35b-a3b    # default; about 22 GB, works on a 16 GB GPU with part of it on the CPU
ollama pull nomic-embed-text
git clone https://github.com/cybergah/airgap
```

A lighter option is `gpt-oss:20b`: it is faster and fits a smaller GPU, but in our benchmark it struggled with large tasks that touch several files. Pick the model with `--model` or in the settings.

**Terminal**

```bash
python airgap/kod-ajani/ajan.py --dizin /path/to/your/project
```

<p align="center">
  <img src="docs/airgap-demo.gif" alt="A real Airgap run in the terminal: gpt-oss:20b on a local GPU reads the code, runs the failing test, proposes a one-line fix to is_leap_year, waits for approval, and the tests pass" width="100%">
  <br><sub>A real run in the terminal on a local GPU. Every command and edit was approved by a human; only the waiting time was shortened.</sub>
</p>

Chat commands: `/undo` undo the last turn · `/new` new chat · `/approve` toggle approvals · `/help` help · `/quit` quit.
One-shot mode: `--gorev "fix the failing tests" --otomatik`. Sandbox: `--korumali` (first run `docker pull python:3.13-slim`).

**VS Code**

Download `kod-ajani-<version>.vsix` from the [latest release](https://github.com/cybergah/airgap/releases/latest) and install it:

```bash
code --install-extension kod-ajani-0.15.0.vsix --force
```

The extension ships with the agent inside; you only need Python and Ollama. To build it yourself: `python airgap/kod-ajani/paketle.py` (writes `airgap/dist/`).

Open a folder and click the `</>` icon in the activity bar. Settings live under **Airgap**.

**Desktop app (Windows)**

A standalone window with the same agent, no VS Code needed: chat, inline diffs with
unified/split views, approvals inside each card, one-click undo, `@` file suggestions,
recent projects and a live Ollama status. It runs on `127.0.0.1` only, every request
carries a random key, and fonts and icons are bundled: nothing is loaded from the network.

**Download [`Airgap.exe`](https://github.com/cybergah/airgap/releases/latest)** and run it: no Python or Node needed, only
[Ollama](https://ollama.com) and Microsoft Edge (built into Windows 11). Or run it from source:

```bash
cd airgap/kod-ajani/masaustu/arayuz
npm ci
npm run build
cd ../..
python masaustu/uygulama.py
```

To build a single `Airgap.exe` that needs neither Python nor Node:
`python -m pip install pyinstaller`, then `python masaustu/paketle_exe.py` (writes `airgap/dist/Airgap.exe`).
The window is Microsoft Edge in app mode (built into Windows 11). End-to-end checks with a real model:
`python masaustu/uctan_uca.py`.

**Optional:** better repo maps for JavaScript, TypeScript and C#:

```bash
python -m pip install tree-sitter tree-sitter-javascript tree-sitter-typescript tree-sitter-c-sharp
```

## Language

The interface is in **English** by default, and fully available in **Turkish** (Airgap started as *Kod Ajanı*):

- VS Code: setting **Airgap › Dil** (`kodAjani.dil`) → `tr`
- Terminal: `AIRGAP_LANG=tr` (PowerShell: `$env:AIRGAP_LANG="tr"`)

Only what *you* see changes. Prompts, tool results and everything else the model receives stay identical, so behavior and benchmark numbers do not depend on the UI language. Code identifiers are still Turkish; want to add another language? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Tests

340 unit tests plus VS Code smoke and panel tests run on every push on Windows, Linux and macOS. Real-model benchmarks and the real VS Code window test run locally.

```bash
cd kod-ajani && python -B -m unittest discover -p "test_*.py"
node kod-ajani/vscode-eklenti/test/duman.js
```

## Roadmap

- **English codebase:** comments first, then CLI flags, then identifiers ([#9](https://github.com/cybergah/airgap/issues/9)).
- **More languages in the repo map:** Go, Rust and Java through Tree-sitter ([#1](https://github.com/cybergah/airgap/issues/1), [#2](https://github.com/cybergah/airgap/issues/2), [#3](https://github.com/cybergah/airgap/issues/3)).
- **Linux and macOS** checked end to end with a real model ([#6](https://github.com/cybergah/airgap/issues/6)).
- **A signed Windows build**, so SmartScreen stops warning.
- **Harder benchmarks:** more tasks with hidden tests, and more real projects ([#5](https://github.com/cybergah/airgap/issues/5)).

## Contributing

Bug reports, translations, new benchmark tasks and security findings are all welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md),
or pick an issue labelled [**good first issue**](https://github.com/cybergah/airgap/labels/good%20first%20issue): most need no
knowledge of how the agent works. Comment on an issue to claim it.
Questions or ideas? Talk to us in **[DevHarbor](https://t.me/devharborhq)**, a developer community on Telegram.

**Beat the command analyzer.** Find a risky command that Airgap does not flag ([#4](https://github.com/cybergah/airgap/issues/4)):
it becomes a test case, and your name goes in the list below. Serious sandbox escapes: please report them privately first,
following the [security policy](https://github.com/cybergah/.github/blob/main/SECURITY.md).

| Found by | Command | Fixed in |
|---|---|---|
| *your name here* | | |

## License

[MIT](LICENSE) © Cybergah

## Author

Created by **Petrus**: developer, hacker, founder of [Cybergah](https://github.com/cybergah).
[GitHub](https://github.com/delilzagros) · [X @AEVERTIS](https://x.com/AEVERTIS) · [Telegram](https://t.me/aevertis)

<div align="center">
<sub>Part of <a href="https://github.com/cybergah">Cybergah</a>, offline-first, privacy-respecting open-source tools.</sub>
</div>
