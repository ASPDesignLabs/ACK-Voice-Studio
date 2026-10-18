# ACK Voice Studio — Project Memory

ACK Voice Studio is the guided desktop tool for recording, training and exporting a custom voice for the ACK phone app (an Android AAC, augmentative and alternative
communication, app). It lives in its own repository; the phone app is in `ASPDesignLabs/ACK`. This file accumulates durable, cross-session knowledge that is easy to
re-break if reimplemented from a shallow read. Add to it rather than replacing it.

## How this repository relates to ACK

- **This repository was split out of ACK**, keeping the history of Voice Studio's own files (the commit messages are unchanged; hashes are not the same as in ACK, because
  history was rewritten to keep only these paths). The layout is kept as it was (`tools/voice_studio/`, `tools/voice_studio_maint/`, `docs/VOICE_STUDIO_*`) so every path
  a guide, a test or an installed launcher already names still exists.
- **Freeform Studio and the training helpers are a copy.** `tools/freeform_studio/`, `tools/patch_voice_for_sherpa_onnx.py`, `tools/split_long_takes.py`,
  `docs/ACK_TRAINING_CAPTURE_FORMAT.md` and `LICENSES/Apache-2.0.txt` were copied in as one snapshot commit ("Import a snapshot of Freeform Studio and the voice-training tools
  from ACK"). Voice Studio imports `freeform_studio` and runs `python -m freeform_studio.process`, `.repair` and `.build_dataset` in the studio's own environment, so it
  cannot run without it. **ACK keeps its own copy too**, because the phone app's capture-format tests read it. The two copies are not kept in step by anything;
  when one changes, make the same change in the other by hand and say so in the commit message. `tools/voice_studio/core/update.py` (`COMPARED_ROOTS`) compares the
  tool's files against a release, so a snapshot edit shows up there like any other.
- **A few tests read the phone app's own files** (`test_vs_phonemes_contract.py`, `test_vs_voicezip_contract.py`, and the one test each in `test_vs_window_theme.py`,
  `test_vs_it_guide.py` and `test_vs_guide.py` marked `needs_ack`): they check that the tool writes exactly what the app reads (the voice zip's entry names and limits, the list of
  sounds, the colours, the engine version, the free-room figure, the free-speech line). They find the phone app through `tests/vs_ack_source.py`: the folder named by the environment
  variable `ACK_SOURCE` (an error if it does not hold the app), else a sibling folder `../ACK`; with neither they are **skipped, saying why**, never silently passed, and
  `test_vs_ack_source.py` fails if a test reads the app any other way. The `contracts-with-the-phone-app` job in `.github/workflows/tests.yml` checks the phone app out and fails if
  any of them was skipped. A change to the voice file's layout or the phoneme table must be made in both repositories. (Freeform Studio's own tests, which read the app's
  Kotlin too, are not part of this repository's CI; see "Freeform Studio's tests" below.)
- Everything below that mentions "the app", "ACK Wear", "EXPORT .JSON" and the like describes the phone app in its own repository; it is kept here only where Voice
  Studio's rules depend on it. The app's own deep analyses (HELP, BACKUP, STATEMENT COMPOSER and the rest) stay in ACK's `CLAUDE.md`.

## DATA SOVEREIGNTY and LICENSING — rules that must stay true

The user's standing requirement (stated while making Freeform Studio usable by casual users and SLPs): **voice recordings,
transcripts, edits, exports, backups, training data and the trained voice stay on devices the person controls, 100%.** And
the project is **GPL-3.0-or-later**. Both are enforced by tests so a later change can't quietly undo them; read these before
adding a dependency, a permission, a network call, a file type, or a new source file.

### Freeform Studio (`tools/freeform_studio/`)
- **The server never goes online.** `FasterWhisperEngine` loads with `local_files_only=True` (`Config.asr_allow_download`
  / `--allow-model-download` is the opt-out) and `privacy.apply_offline_defaults()` sets `HF_HUB_OFFLINE=1`,
  `HF_HUB_DISABLE_TELEMETRY=1`, `DO_NOT_TRACK=1` before the Hugging Face libraries import. Measured: without this every model
  load contacted huggingface.co even when cached (and *failed* behind a 403 proxy). **`models.py` (`python -m
  freeform_studio.models fetch NAME`) is the one place allowed to use the internet, and it asks first.** `asr_smoke` follows
  the same rule. A missing model produces a plain `EngineError` naming the exact fetch command (`explain_load_error`).
- **Owner-only files.** `privacy.private_umask()` wraps `main()` of the server and every file-writing command (backup, export,
  build_dataset, repair, models); the token file is created with `O_EXCL` + mode 0600. `doctor` only *reports* loose
  permissions on older data (and the `chmod -R go-rwx` command) — it never changes a user's files by itself.
- **Browser caching.** Everything under `/api/` is `Cache-Control: private, no-store` (audio, transcripts, waveforms). Opening
  the printed `?token=` link 303-redirects to the same page without the token (`address_without_token`, never `//host`), the
  cookie carries the login; `/api/*?token=` still works for scripts. Tests: `tests/test_privacy.py`.
- **Synced folders.** `privacy.sync_risk()` / `sync_warning()` flag paths inside OneDrive/Dropbox/Google Drive/iCloud/etc. and
  Windows `Documents`/`Desktop`/`Pictures` (OneDrive Known Folder Backup); used by the server banner, `doctor` and the backup
  command. It only ever says "may" (folder names, can't see whether sync is on). Never recommend a `Documents` backup path.
- **No-network regression test.** `tests/test_no_network.py` + `tests/egress_workflow.py` run the whole workflow in a
  loopback-only namespace (`unshare -rn`) with a Python socket-logging hook and `strace`, and fail on any destination that
  isn't this computer; the only allowed oddity is `netcheck.lan_ip()`'s UDP `connect()` to `192.0.2.1:9` (a route probe;
  sending to it fails the test). Another test fails if a web address appears in any shipped file. If you add a feature that
  genuinely needs the network, it must be an explicit, user-confirmed command like `models fetch`, not a background call, and
  needs the user's approval first.
- Not measured in the build sandbox (Hugging Face is blocked there): a real speech-model run end to end, a real training
  run, a real phone. `docs/DATA_SOVEREIGNTY.md` says so and gives the user commands to check themselves.

### The ACK phone app is in another repository
- The phone app's own rules (no network permission, no network code, cloud backup switched off, the sovereignty policy test) are kept in `ASPDesignLabs/ACK`
  (its `CLAUDE.md`, "DATA SOVEREIGNTY and LICENSING"). Nothing in this repository changes them; what this repository promises about the voice file is that it is
  handed to the phone by a file or a cable, or once over the home network by `voicefile send`, and never uploaded anywhere.

### Licensing
- **GPL-3.0-or-later.** `LICENSE` is the **byte-identical** FSF text (SHA-256 pinned in `test_license_headers.py`; an earlier
  copy differed from the FSF text in two words). The copyright line lives in `NOTICE`, not in `LICENSE`. **Every source file**
  (`.kt .kts .py .js .mjs .html .css .sh .pro`) carries `SPDX-License-Identifier: GPL-3.0-or-later` in its first lines (after a
  shebang / `<!doctype>`); the test fails for a new file without one. XML resources, docs and images are covered by `NOTICE`.
- `tools/patch_voice_for_sherpa_onnx.py` follows sherpa-onnx's Apache-2.0 `add_meta_data.py` (Xiaomi Corp.): its header is
  `GPL-3.0-or-later AND Apache-2.0` with the attribution and a statement of changes; `LICENSES/Apache-2.0.txt` is the verbatim text.
- **`THIRD_PARTY_NOTICES.md`** lists every outside source with license **and how it was checked** ("not verified" is stated, never
  guessed). A test fails if a binary asset (`.so .otf .ttf .jar .aar`) is committed, or a Freeform Studio requirement is added,
  without being listed. When adding a dependency, read its real license (installed metadata / repo / POM) and add it.
- **Open decisions recorded there (do not "fix" silently):** the license of whichever Piper base checkpoint a voice is trained from (per-voice `MODEL_CARD`);
  the publisher name (`NOTICE` says another holder); signing the Windows setup program. The phone app's own open decisions (a font whose embedded license is
  *no-derivatives*, the two Google Play Services libraries, image provenance) are recorded in `ASPDesignLabs/ACK`'s `THIRD_PARTY_NOTICES.md` and are not repeated here.
- Authorship: Freeform Studio was written with an AI assistant; that is stated in `THIRD_PARTY_NOTICES.md`. Keep saying it.


## ACK VOICE STUDIO — rules that must stay true

The guided desktop tool for recording, training and exporting a custom voice (`tools/voice_studio/`, Python, Ubuntu or WSL; Windows has a helper installer). The plan and every decision
(D = asked, P = chosen and open to veto) are in `docs/VOICE_STUDIO_SETUP_PLAN.md`; the running hand-off is `docs/VOICE_STUDIO_HANDOFF.md`; the person-facing documents are
`docs/VOICE_STUDIO_GUIDE.md`, `docs/VOICE_STUDIO_HELPER_HANDOUT.md`, the two installation guides and `docs/VOICE_STUDIO_IT_GUIDE.md`; the checklist for a real computer is
`docs/VOICE_STUDIO_DEVICE_TEST.md`; release steps are `docs/VOICE_STUDIO_RELEASE_RUNBOOK.md`. The tool's own changelog is `tools/voice_studio/CHANGELOG.md` (not the app's).

- **Built without a screen, a GPU, a microphone or a phone.** Everything was tested in a sandbox (`tools/voice_studio/run_tests.sh`: warnings are errors; it needs only pytest). The window
  (GTK), the training runs, real speakers and a real connection were **not** run, and the checklist's statuses say so. Never write that something "works" on a real computer unless the
  checklist records a real run; the guide and handout tests fail on a claim the checklist's statuses do not allow.
- **`core/` is plain Python: no GUI library, no network library.** It runs on Ubuntu's own Python 3.10 and 3.12, so nothing newer than 3.10 (`test_vs_package_rules.py` checks the syntax).
  The only module that may reach the internet or start a program is `core/fetch.py` (`run_networked`, with `GIT_TERMINAL_PROMPT=0` for git); web addresses live only in
  `data/sources.json` (on an allowed-host list) and the two bootstrap scripts, `get.sh` and `install.ps1` (`test_vs_network_rules.py`, `test_vs_install_ps1.py`). Every networked command says first what it will ask and what the request
  carries, then asks (a typed yes or `--yes`, for that run only); nobody to ask means nothing is contacted. Nothing runs by a timer or at start-up.
- **Every command that changes something shows it first and asks.** Exit codes: 0 done, 1 failed after it started, 2 nothing was done (declined, nobody to ask, a bad option). A failure
  after starting (exit 1) ends with two lines pointing at the problem report (`@reports_failures`, `core/reportcmd.py`). **Nothing is deleted unless the person asked**, restores and
  backups only add, and an earlier backup is never replaced or removed. The recordings, the transcripts and the trained voice never leave the computer except to a place the person names.
- **Words are in `data/text/en.json`**, never in the code: sorted `strings` and `plurals`, keys `namespace.name`, and errors in three parts (`what`, `changed`, `next`, read with
  `error_text(cat, ns, code)`). A new namespace or error code is registered in `test_vs_text.py` (its lists, the raise sites, which need the code as a literal in `Name("code")`). The
  wording rules are tested: at most 300 characters and 25 words a sentence, no jargon list, no four-capital-letter words, and nothing that sounds like permission the person was not given.
- **Documents are held to the code by tests.** A quoted sentence in a guide or the checklist must be one the tool really says (`device_doc.says`), every command and option named must exist,
  and every figure must be the real one. When you change a sentence in `en.json`, search `docs/` and `tools/voice_studio/README.md` for it; the failing test names the file. Never "fix"
  a doc test by loosening it.
- **A release is a git tag named `voice-studio-vX.Y.Z`, never a bare `vX.Y`.** While this tool lived inside the phone app's repository, that repository also held the app's tags
  (`v1.0-beta.1` to `v1.0-beta.7`), which are **not** releases of this tool; they stay there, and this repository starts with none. The registry's `tag_prefix` (`data/sources.json`,
  `releases`) is still what makes `update check` and `update get` count only the tool's own, so a stray tag of any other kind never counts. An earlier version of the update
  command, its tests and its docs wrongly said "ACK has no tagged release yet" and would have listed the app's tags; it was found by reading `git tag -l`. **Look at the real repository
  before writing a claim about it.** `get.sh` and `install.ps1` fetch `main` until a release exists; the version in `tools/voice_studio/__init__.py` must match the tag (the runbook).
- **Test new code by breaking it.** Copy the repository, change one line at a time (`>=` for `>`, a dropped check, a swapped argument), run the tests, and give every survivor a test, a
  simplification of redundant code, or a written note that it is equivalent. Run the breaks in parallel with a separate `TMPDIR` for each copy, or the runs interfere. This found real
  bugs more than once (a race that could delete a file someone else had just made; a path nested too deep crashing six readers).
- **A window page is the face of a command, never a second copy of it.** The window (`tools/voice_studio/window/`, GTK 4.6 is the floor) draws; `core/windowmodel.py` decides (the page list `PAGES`, the views,
  the `(tool, argv)` each button hands to `Services.run`, the report form's rules) and `core/windowio.py` asks the Yes or No question. A page never asks a question the command does not ask and never
  writes a file or opens a connection itself (`test_vs_window_gtk.py` reads the source). A page that can lead to the internet says so in the checklist: **Updates, and on Check the tool the mend and
  fresh-copy buttons**, each only after the command says what it will ask for; an earlier line in the checklist wrongly said Updates was the only one (found by reading `refresh_flow.py`). The headless tour
  (`window/selftest.py`, `selftest_tools.py`, run by `test_vs_window_gtk.py` under GTK 4.14 and, with `ACK_VS_GTK46_RUNNER`, in the Ubuntu 22.04 copy) presses every button. **A tour check inside
  `if something_exists:` silently never runs** when the copy of the project has no such thing (no tasks, one round): give the page the input instead (the tour builds a `HearView`, patches
  `job_choices`, calls `folder_chosen`), because the headless file chooser cannot be made to return a folder. Breaking the pages one line at a time found 16 unchecked behaviours in 54 breaks.
- **The data-sovereignty rules apply here too** (see that section): `docs/DATA_SOVEREIGNTY.md` has the rows for this tool and `test_vs_data_sovereignty_doc.py` fails if a command that can
  reach the network is missing a row. Every source file carries `SPDX-License-Identifier: GPL-3.0-or-later`; `THIRD_PARTY_NOTICES.md` section 7 lists what the tool installs, with how each
  licence was checked (`test_vs_notices.py`).
- **`voicefile send` is the only place the tool listens, and only `core/lansend.py` may do it** (plan VS-3.5 and VS-5.1, choices P25; the checklist is section I16). It hands the finished voice zip to a phone on the
  home network once. `test_vs_network_rules.py` holds the module to: imports only `socket` and `ssl`, never dials (no `connect`, `create_connection`, `getaddrinfo`...), binds exactly once, never `0.0.0.0` or
  IPv6, and serves one file by an exact path (`https://<ip>:<port>/<22-character token>/<zip name>`; any other request gets the same short 404; twelve of those stop it; ten minutes at most; TLS 1.2 or
  newer; a half-sent file allows a retry). `core/phonecert.py` makes the certificates by starting the local `openssl` program (a program the tool starts, not a network program): a wizard-made authority limited by name
  constraints to `10/8`, `172.16/12`, `192.168/16` and one name that cannot exist (so a re-issued leaf for a new address needs no change on the phone, which resolves the VS-0.3 question), kept in
  `state/phone-certificate/` (not backed up, folder 0700, key 0600, never replaced, a damaged or ended one is reported and never used); the short-lived leaf is made per send in a work folder that is removed afterwards.
  `core/qrcode.py` is a pure-Python encoder (tested against the standard's worked values and an independent decoder written from the specification); the QR is drawn only when the terminal can show black on white
  (`io.ansi`), and the address is always printed. **Not confirmed on a phone: that Android enforces the name constraints, that the QR scans, and the network under WSL (VS-3.6 is not built).** When a statement elsewhere says the tool
  "opens no listening port", it means outside this one command; keep the IT guide, `docs/DATA_SOVEREIGNTY.md` and the checklist in step with `core/lansend.py` (their tests read the code).
- **`wsl` is the one command that writes a Windows file, and it writes exactly one** (plan VS-3.6, choices P26; the checklist is section I17). `python3 -m voice_studio.wsl check | phone | idle`
  (`core/wsl.py`, `core/wsl_flow.py`) helps with two settings in `.wslconfig` in the person's Windows home folder: `networkingMode=mirrored` under `[wsl2]` (a phone can reach Ubuntu) and
  `instanceIdleTimeout=-1` under `[general]` (Ubuntu is not stopped about a minute after its last window closes, finding F3). The rules: the file is **reached as a file** through the Windows drive
  (`/mnt/c/Users/<name>`, or where `/etc/wsl.conf` puts it), never through a Windows program, because those do not always work (F4); the two Windows questions (`cmd.exe /c ver`, `cmd.exe /c echo
  %USERPROFILE%`) have a ten-second limit and nothing depends on them; an edit is **one setting, shown as the lines that differ, asked once (`--yes` answers it), the old file copied first to a name
  that does not exist (`.bak`, then with the time), the new text written to a temporary file and moved into place, then read back**, and every other line, comment, line end and byte order mark is kept
  (read and written as bytes: a text-mode read turns CRLF into LF); a file that is not UTF-8 text or repeats the key or the section is refused. **It never restarts WSL and never runs the firewall
  command: it prints them.** `rounds start` reads the file (no Windows program) and says, before it asks, that closing the last window can stop the round; it never refuses for it. **Unverified:** the firewall
  command and where Microsoft keeps each key were taken from a search summary of Microsoft's page, `wslinfo --networking-mode` was not seen, and nothing has run on a real Windows.
- **The model card is a separate file written last, and it names nothing personal** (plan VS-5.2, choices P27; the checklist is section I4). `voicefile make` ends by writing `MODEL_CARD.txt` (`core/modelcard.py`) in the voice file's own new folder:
  **never inside the zip** (ACK takes exactly two files from it), owner-only, and only after the zip has been read back, so a card that cannot be written (`card_failed`) leaves the good zip. It is built from stored facts and says when
  one is missing. **The starting voice is read from the first round of the chosen round's training (`Round.voice`), never from the project's present choice**; the chain, the pages and the "no legal advice" sentence are the catalog's and the
  registry's own words shown before the download, and the acknowledgments are the project's. For someone else's voice it holds only which of the five fixed ways the consent note says the agreement was given, never a name, a date or a word of the
  note. **It does not name the project and does not print the zip's file name** (that carries the project's folder name; the first version did and the privacy test caught it). It never says or suggests that use of a voice is allowed; it says
  sharing is a separate decision (the same `implies_permission` check that guards the screens runs over its text). A new fact on the card must be stored, plain, and not personal; add the test that it is not copied from a free-text field.

- **The Windows setup program is a wizard that asks and an engine that does, Windows 11 only, unsigned, and it sees the password** (plan VS-7.4, decision D44, choices P28; the checklist is section I18; `tools/voice_studio/installer/`). The developer's decisions: signing is postponed;
  a window flow asks for an Ubuntu account name and password; the program is **pulled from its source while it runs, never carried in the file**; **Windows 11 only** (build 22000, the same number in `install.ps1`'s `MinBuild` and the wizard's `MIN_BUILD`, a test holds them equal; Windows 10 is
  refused with a message that changes nothing). `ack-voice-studio.nsi` (NSIS, built by `installer/build.sh`, same bytes every time) is a **one-user, no-administrator** wizard with **no silent mode**; it runs `engine.ps1` hidden, one step per run (`check`, `platform`, `distro`, `validate`,
  `user`, `sudo-on`, `setup`, `sudo-off`, `launcher`, `open`, `unlauncher`), through the 64-bit PowerShell by `Sysnative` (a 32-bit program would reach a System32 without `wsl.exe`), with `-ExecutionPolicy Bypass` for that child process only. **The password rules, each held by a test:** typed into
  the wizard, put in `ACK_VS_PASSWORD` of the one program started for `validate` or `user` and removed straight after (`PasswordIn`/`PasswordOut`), read once by the engine and removed from the environment, sent to Ubuntu on the standard input of **one** `chpasswd` (bytes, UTF-8 without a BOM, never
  the PowerShell pipeline, which adds a carriage return), never in an argument, a printed line, the log (it masks the value), the registry or a file; printable ASCII of 8 to 128 characters only (an accent could be read three ways between Windows, WSL and Linux); **set only on an account that has none**
  (`passwd -S`'s state is not `P`), so an existing account's password is never changed and an account found at the check skips the account page. This deliberately differs from `install.ps1`, which never sees a password, and the account page says so; any text that says the tool "never sees" a password
  must say which installer it means. **The temporary `NOPASSWD` permission** (`/etc/sudoers.d/ack-voice-studio-install`, `visudo`-checked, mode 0440) exists only between `sudo-on` and `sudo-off`, and **the failure path runs `sudo-off` first** (`Fail`); do not add a way out of the install that skips it.
  **A restart (engine code 3) is asked about, remembered and resumed** (the first real run asked for one and, run again, started over): WSL counts as set up when any of `wsl -l -v`, `wsl --status`, `wsl --version` succeeds (**`wsl -l -v` alone fails when no Ubuntu is installed yet, which looped the restart request**); `installer-state.ini` beside the log (`Read/Update-AckVsEngState`, plain ASCII, never a key that could hold a password) records `platform=restart` with the time Windows started and every step reached, the Ubuntu and account names; a pending restart is waited for, never repeated, and WSL silent after it stops once (`platform=failed`, the next run tries once more); `AskRestart` asks `Restart now?` (`shutdown.exe /r /t 20` only after a Yes), writes one `HKCU` `RunOnce` value for `Resume.exe` (a copy of the setup program, not copied over itself) either way, and `Quit`s; the resumed copy skips the pages already read, offers the remembered account name and asks for the password again. Do not make a restart an `Abort` (it looks like a failure), and do not store the password to spare a retype. The uninstaller deletes the six files it wrote, `RMDir` without `/r`, one `HKCU` key, and the tool's own Start menu entry by the marker in its description; **it never removes Ubuntu, the tool or any
  recording, transcript or voice** (a test bars `--unregister` and `RMDir /r`). **PowerShell facts that bit:** `$` in a .NET regex matches before a trailing line break, so every validator ends `\z` (Python's is `\Z`); `Process.ArgumentList` does not exist in 5.1; `wsl.exe` writes UTF-16, so lines are cleaned
  of NULs; `-DryRun` is a `[switch]`. **Not seen:** the wizard on a screen, any of it on a real Windows, **Ubuntu registering without its first-run question** (cloud-init with `--no-launch`, fallback `ubuntu2404.exe install --root`: the least certain step), and how SmartScreen treats an unsigned file. The workflow
  `.github/workflows/voice-studio-installer.yml` builds the unsigned file and parses and dry-runs the engine on a Windows runner; it signs and publishes nothing. Open for the developer: the publisher name (NOTICE says another holder), a self-hosted source, signing, a silent mode.
