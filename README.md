# ACK Voice Studio

A guided, graphical way to record, train and export a custom voice for the [ACK](https://github.com/ASPDesignLabs/ACK) phone app (an Android AAC, augmentative and alternative
communication, app), on Ubuntu LTS and on Windows 11 through WSL. One command (or a Windows setup program) sets it up and opens a native window that walks a helper and a
person through bringing in recordings, training, hearing the result and sending the finished voice to a phone. Every step is also a terminal command.

Recordings, transcripts, edits, backups, training data and the trained voice stay on devices you control. Nothing is uploaded unless you do it; the few commands that can
reach the internet say first what they will ask for, and ask. Details: [`docs/DATA_SOVEREIGNTY.md`](docs/DATA_SOVEREIGNTY.md).

**Status.** Built and tested in a sandbox with no screen, no GPU, no microphone and no phone, and run on one real computer (Windows with WSL2). What has and has not been seen on a
real computer is written down, row by row, in [`docs/VOICE_STUDIO_DEVICE_TEST.md`](docs/VOICE_STUDIO_DEVICE_TEST.md); nothing here says "works" where that file does not.

## Start here

- **Windows 11:** [`docs/ACK_Voice_Studio_Installation_Guide.MD`](docs/ACK_Voice_Studio_Installation_Guide.MD). A setup program (`ACK-Voice-Studio-Setup-<version>.exe`, built by
  [`tools/voice_studio/installer/`](tools/voice_studio/installer/)) or one PowerShell command.
- **Ubuntu 22.04 or 24.04:** [`docs/ACK_Voice_Studio_Installation_Guide_Ubuntu.MD`](docs/ACK_Voice_Studio_Installation_Guide_Ubuntu.MD).
- **Using it:** [`docs/VOICE_STUDIO_GUIDE.md`](docs/VOICE_STUDIO_GUIDE.md), and the one-page [`docs/VOICE_STUDIO_HELPER_HANDOUT.md`](docs/VOICE_STUDIO_HELPER_HANDOUT.md) for a helper.
- **IT staff:** [`docs/VOICE_STUDIO_IT_GUIDE.md`](docs/VOICE_STUDIO_IT_GUIDE.md) lists every program, host and port.
- **The tool itself:** [`tools/voice_studio/README.md`](tools/voice_studio/README.md). The plan and every decision behind it: [`docs/VOICE_STUDIO_SETUP_PLAN.md`](docs/VOICE_STUDIO_SETUP_PLAN.md).
  Picking the work up: [`docs/VOICE_STUDIO_HANDOFF.md`](docs/VOICE_STUDIO_HANDOFF.md).

## What is in this repository

| Folder | What |
|---|---|
| `tools/voice_studio/` | The tool: `core/` (plain Python, no window), `window/` (GTK 4), `installer/` (the Windows setup program), `data/`, and its tests |
| `tools/voice_studio_maint/` | Maintainer scripts that make the pinned lock files |
| `tools/freeform_studio/` | Freeform Studio, the recording-review and dataset tool Voice Studio is built on. **A copy**; see below |
| `tools/patch_voice_for_sherpa_onnx.py`, `tools/split_long_takes.py` | Voice-training helpers the tool runs. Copies, too |
| `docs/` | The guides, the plan, the device checklist, the data-sovereignty page and the training guides |

## How this relates to ACK

This repository was split out of [ASPDesignLabs/ACK](https://github.com/ASPDesignLabs/ACK), keeping the history of Voice Studio's own files. The phone app stays there.
Freeform Studio and the training helpers were copied in as one snapshot because Voice Studio runs them; ACK keeps its own copy too, so the two are **not** kept in step
automatically. A few tests check that what this tool writes is what the phone app reads (the voice file's layout, the phoneme table, the app's colours); they need a checkout of
the phone app and are skipped, saying so, without one. See [`CLAUDE.md`](CLAUDE.md) for the rules.

## Running the tests

```bash
python3 -m venv ~/voice-studio-test-venv && ~/voice-studio-test-venv/bin/pip install pytest
PYTHON=~/voice-studio-test-venv/bin/python tools/voice_studio/run_tests.sh
```

Nothing in the tests uses the network, a GPU or a display. To also run the tests that read the phone app's source, put an ACK checkout next to this one (`../ACK`) or point
`ACK_SOURCE` at it.

## License

Licensed under the GNU General Public License, version 3 or (at your option) any later version (**GPL-3.0-or-later**): [`LICENSE`](LICENSE) is the license and [`NOTICE`](NOTICE)
holds the copyright line. Every source file carries an `SPDX-License-Identifier: GPL-3.0-or-later` line. The software and models made by others that this tool uses, with their
licenses and how each was checked, are listed in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Parts were written with an AI coding assistant; that is stated there too.
