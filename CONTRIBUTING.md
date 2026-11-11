# Contributing to Airgap

Thanks for helping. Airgap is a local, security-hardened coding agent, so two rules
come before everything else:

1. **Nothing may send code or prompts off the machine.** No telemetry, no cloud calls.
2. **Security checks only get stricter.** A change that weakens an approval gate, the
   command analyzer or the sandbox needs a very good reason and a test.

## Where help is most welcome

| Area | What | Where |
|---|---|---|
| 🌍 **Languages** | The UI is English by default and Turkish with `AIRGAP_LANG=tr`. Add another language, or polish the English. Only translate what the user sees: never the prompts or tool results the model receives. | `L(...)`, `RISK_EN`, `_MESAJ_EN` in `kod-ajani/ajan.py`; `L(...)` in `vscode-eklenti/extension.js` and `media/panel.js`; `test_dil.py` |
| 🛡️ **Command analyzer** | Find commands that slip past risk detection and add them as test cases. | `kod-ajani/komut_ornekleri.py`, `komut_sinav.py`, `test_guvenlik.py` |
| 📏 **Benchmarks** | Add tasks with hidden tests, or measure other local models. | `kod-ajani/olcum_gorevleri.py`, `olcum.py` |
| 🗺️ **Repo map** | Better Tree-sitter support for more languages. | `dosya_tanimlari` / `_ts_tanimlari` in `ajan.py` |
| 🐧 **Linux and macOS** | The agent is tested on Windows; reports and fixes for other systems are welcome. | |

## Setup

```bash
git clone https://github.com/cybergah/airgap
cd airgap
ollama pull gpt-oss:20b
ollama pull nomic-embed-text
```

Run the tests before opening a pull request. They do not need a model or a GPU:

```bash
cd kod-ajani && python -B -m unittest discover -p "test_*.py"
node vscode-eklenti/test/duman.js
node vscode-eklenti/test/durum.js
```

Sandbox tests run only when Docker and the `debian:latest` image are available; otherwise
they are skipped.

If your change affects how the agent behaves, please also run the benchmark and paste
the summary into the pull request:

```bash
python kod-ajani/olcum.py --etiket my-change --karsilastir bitirme
```

## Pull requests

- Keep one change per pull request, with a test.
- Describe what you tested, on which OS and with which model.
- The project has no third-party Python dependencies at runtime (Tree-sitter is optional).
  Please keep it that way.

## Security issues

Found a way around an approval, the command analyzer or the sandbox? Please do **not**
open a public issue. Report it privately as described in the
[security policy](https://github.com/cybergah/.github/blob/main/SECURITY.md).
