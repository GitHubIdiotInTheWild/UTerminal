# UTerminal

A sleek, modern, and modular terminal environment built with Python.

---

## Features

* **Modular Pipeline:** Separate sub-modules handle system directory mapping (`file_ops.py`), content parsing (`file_viewer.py`), and dynamic size strings (`utils.py`).
* **Asynchronous Processing:** Long-running system subprocesses and audio playback instances are handled on isolated daemon worker threads to keep the UI buttery smooth.
* **Command History Navigation:** Easily cycle through previous commands using the `Up Arrow` and `Down Arrow` keys inside the input terminal box.
* **Clipboard Hook (`copypop-`):** Prepend any terminal utility execution string with `copypop-` to automatically pop that specific payload output directly into your system clipboard buffer.
* **Interactive Audio Feedback:** Features custom multimedia hooks using low-level Windows APIs for native audio cues at comfortable volume levels.

---

## 📁 Repository Blueprint

```text
cmdmodern/
│
├── ModernCMD.py        # Core Application Frame & Window Event Loop
├── file_ops.py         # Directory scanning & file generation extension
├── file_viewer.py      # Plaintext reading & file stream handler
├── utils.py            # Size string formatting utility utilities
├── nope.mp3            # Easter egg audio asset
└── jingle.mp3          # Success notification audio asset
