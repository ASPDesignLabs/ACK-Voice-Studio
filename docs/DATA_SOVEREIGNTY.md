<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Keeping your voice data on your own computer

This is for anyone using Freeform Studio, the training steps and ACK Voice Studio (the desktop tool that guides them) to make a voice for
their own AAC, and for speech-language pathologists (SLPs) helping someone else do it. It says where the data is, when anything touches the internet, how to check
that yourself, and what to think about when the voice isn't yours.

**The rule this project follows:** recordings, what the PC heard, your edits, exports, backups, the training data and the
trained voice stay on devices you control. Nothing is uploaded, and nothing is sent anywhere, unless you do it.

This is not legal advice. It records what the software does, how that was checked, and the questions to ask.

## 1. Where everything lives

| What | Where (default) |
|---|---|
| Raw recordings, transcripts, your edits | `~/piper-recording-studio/output/_freeform/<code>/takes/` |
| Pieces you exported for training | `~/piper-recording-studio/output/<code>/freeform/`, and `output/_freeform/<code>/retired/` for what was replaced |
| Backups | `~/backups/freeform-studio` (or the folder you chose with `--backup-dir`) |
| Training dataset | `~/piper/freeform-dataset-<date>/` |
| Training cache, checkpoints, logs | `~/piper/my-training/`, `~/piper/checkpoints/`, `~/piper1-gpl/lightning_logs/` |
| The trained voice | the `.onnx` and `.onnx.json` files you exported, then inside the ACK app's private storage |
| **ACK Voice Studio:** a person's project (the recordings brought in, the text written from them, training sets, training rounds and their saved points, finished voice files, and the note about who agreed) | `~/ack-voice-studio/projects/<name>/`, in the Linux home folder (under WSL, inside the Linux disk image, not in a OneDrive or other synchronised Windows folder). The training sets and each round's working files are in its `scratch` folder, which can be moved to another drive you choose |
| ACK Voice Studio: the test sounds made by hearing a voice on the computer | the project's `listening` folder, grouped by the round or voice file they came from. Small. Offered for removal after 30 days; never removed on their own |
| ACK Voice Studio: a backup of one project (`python3 -m voice_studio.backup`) | the folder you name, never inside a project. One plain `.tar` of the recordings, the notes and the finished voices. **Not encrypted.** The tool checks it by reading it back, never replaces or removes an earlier one, and warns when the folder looks synchronised |
| ACK Voice Studio: its programs, downloads and the starting voices | `~/ack-voice-studio/tool/`. The programs and downloads are made again by set-up; the starting voices are kept, because they may not be downloadable again. None of it holds your recordings |
| ACK Voice Studio: its small records | `~/ack-voice-studio/state/`: what you agreed to download, the window's colour and size choices (written only after you say yes), the record of tasks that are running or ran, and, only if you send the voice file to a phone over Wi-Fi, the small certificate file for the phone and its secret part (`state/phone-certificate/`, readable only by you, never in a backup) |
| A problem report you save from ACK Voice Studio (`python3 -m voice_studio.report save`) | the one file you name, as plain text, readable by you only. Your names and folders are blanked, and it has no recordings, no text you made and no phrases. It is about your computer, though, and **not encrypted**; the tool never sends it |
| On your phone, while recording in the browser | the browser keeps each audio part until the PC confirms it, then deletes it; unsent edits are kept as a draft |
| On your phone, while recording with the ACK app | inside ACK's own private storage, until you save a package; ACK has no network permission and its cloud backup is switched off |
| Packages saved by the ACK app | wherever you put the `.zip` file, then `~/piper-recording-studio/output/_freeform/<code>/incoming/` once you add it in Freeform Studio. Copies of what is on your phone; **not** included in backups; never deleted by the program |
| Everything else the ACK phone app keeps (its EXPORT .JSON backups, safety copies, the Terminal log, saved message logs, the usage summary, the partner card's sentences, the clipboard, the watch's copy of names) | Described in the phone app's own repository (`ASPDesignLabs/ACK`, `docs/DATA_SOVEREIGNTY.md`, sections 1 and 8). None of it is made by this tool |

## 2. When anything uses the internet

| When | Who is contacted | What is sent | How to avoid it |
|---|---|---|---|
| Installing (`install.sh`, `pip`) | PyPI | package names, your address | install once, then work offline |
| `python -m freeform_studio.models fetch` | huggingface.co | the model name, your address, library versions. **Asks first. No audio, no text.** | skip it by copying a model folder and using `--asr-model /path` |
| Setting up ACK Voice Studio (`install.ps1` or `get.sh`, then `python3 -m voice_studio`) | github.com and raw.githubusercontent.com (the tool itself); the Ubuntu package servers (a few programs); PyPI (`pypi.org`, `files.pythonhosted.org`: the programs it runs on); on a Windows without WSL, Microsoft's servers | package and file names, your address. **Each download is listed with its size and asked about first; the person's yes is kept in `state/consent.json`** | set it up once, then work offline; or hand over the files yourself (the IT guide, section 6) |
| The Windows setup program for ACK Voice Studio (`ACK-Voice-Studio-Setup-<version>.exe`, which runs `installer/engine.ps1` hidden) | It makes **no connection itself**: it starts PowerShell and `wsl.exe`, and the set-up step runs the very command `install.ps1` uses, so the hosts are those of the row above (github.com and raw.githubusercontent.com; the Ubuntu package servers; PyPI; Microsoft's servers for WSL and Ubuntu) | the same as set-up. **It asks for an Ubuntu account name and a password and sees the password** (it is sent once to Ubuntu on standard input and kept in no file, log, message or command line), which the command-line installer never does. A log of the steps, with no password, is kept at `%LOCALAPPDATA%\ack-voice-studio\installer.log`, and the step it got to, the Ubuntu name, the account name and the time Windows started (never the password) in `installer-state.ini` beside it; after a restart it adds one `RunOnce` value for this user so that it can carry on | run `install.ps1` or `get.sh` by hand instead; nothing in the program needs the internet except the same downloads |
| Getting the listening model (`recordings model`) and a starting voice (`voices get`) | huggingface.co, and the download hosts it redirects to (`*.hf.co`) | the file names, your address. **Asks first; a starting voice asks twice and shows its licence.** No audio, no text | skip it by putting the files in place yourself |
| Looking for a newer release of the tool, and fetching one (`python3 -m voice_studio.update`) | github.com | the request itself: your address and the name of the program asking. **Says first what it will ask and shows the commands; nothing is checked in the background.** Nothing of yours | don't run it |
| Mending a damaged download or building the programs again (`refresh repair`, `refresh rebuild`) | the same hosts as set-up | the same as set-up, under the same agreement | `refresh check` only looks, and reaches no network |
| Giving the finished voice file to your phone over the home network (`voicefile send`) | **no host on the internet.** For a few minutes this computer waits for one device on your own home network to ask for the one file, at an address that holds a secret token, over a secure connection, and stops after the first complete download | the finished voice file, to whichever device opens that exact address first. **Asks first; shows the address; ends by itself in 10 minutes; nothing else on the computer can be fetched.** The first time it makes a small certificate file you put on the phone; its secret part stays on this computer and is not in a backup | don't run it, and copy the zip file by cable or USB drive instead |
| Helping Ubuntu under Windows reach a phone and stay running (`python3 -m voice_studio.wsl`) | **nobody.** It reads, and after a typed yes changes, one file on this same computer: `.wslconfig` in your Windows home folder. It starts at most two short Windows programs on this computer to ask what Windows is called and what version it is | nothing leaves the computer. **Shows the change first, asks, and keeps a copy of the old file. It never restarts WSL and never runs the firewall command; it only prints it.** Opening the firewall for a phone is your decision | don't run it, or make the same change by hand |
| **Everything else in ACK Voice Studio:** projects, bringing recordings in, letting the computer listen, training sets, training rounds, making the voice file, hearing the voice, backup, moving scratch, uninstall, Free up space, the problem report and the window | **nobody** | nothing | (nothing to avoid). Not measured with the network cut off for a whole training round; by design it needs none |
| The server, review pages, export, backup, dataset building, `doctor` | **nobody** | nothing | (nothing to avoid) |
| Bringing a package from the ACK app into Freeform Studio (`ack_import` or the Review page's *Add recordings from ACK*) | **nobody** | nothing | (nothing to avoid). The package moves by cable or USB drive; ACK has no way to send it anywhere |
| The first training run | github.com, to fetch the `val_mos` quality scorer's code and weights, **and run that code** (`torch.hub`, `trust_repo=True`). Nothing of yours is sent. | the request itself | run it once online, then it works from its cache; or turn the scorer off (`--model.mos_metric none`, read in the trainer's source, not tried here) |
| Downloading a base voice checkpoint (training guide, step 3) | huggingface.co | the request | it is a step you take yourself |
| **Pasting recordings, transcripts or datasets into a hosted AI assistant or any website** | whoever runs it | **everything you paste** | don't. This is the easiest way to lose control of this data, and nothing here can stop it. |

**The server never goes online.** It loads the speech model from disk only (`--allow-model-download` is the opt-out, off by
default), and it switches Hugging Face's libraries to offline mode so they don't even ask whether a newer version exists.
Without that, each model load contacted huggingface.co, which was measured on 2026-10-01.

## 3. How to check it yourself

You don't have to take any of this on trust.

**The simplest test (no tools needed).** Disconnect your router from the internet (unplug its internet cable), keep Wi-Fi on so
your phone can still reach the PC, and record, review, edit, export and back up a take. Everything should work. If something
doesn't, tell the project: that means something needed the internet.

**ACK Voice Studio.** After set-up, the same test works for it: everything except fetching the listening model or a starting voice, looking for a newer release, and mending a download works with the internet cable unplugged. The IT guide (`VOICE_STUDIO_IT_GUIDE.md`, section 5) lists every host it can reach and why, and the tool shows each download with its address and size and asks before it starts. A whole training round with the network cut off has not been measured; by design it needs none.

**Watch every connection a program makes** (Linux or WSL):

```bash
cd ~/ack-tools/tools && source ~/freeform-studio-venv/bin/activate
strace -f -qq -e trace=connect,sendto -o /tmp/net.log python -m freeform_studio --host 0.0.0.0 --asr-engine fake
# use it, press Ctrl+C, then:
grep -E 'AF_INET6?' /tmp/net.log | grep -v -E '127\.0\.0\.1|::1'
```
Expect nothing, or only a `connect` to `192.0.2.1:9` and to your own computer's address. The first is a UDP "connect" the
program uses to find which local address to put in the link; nothing is sent to it. The test suite checks that this
address is never sent anything.

**Run the project's own check.** `python -m pytest freeform_studio/tests/test_no_network.py -v` runs the whole workflow (including bringing in a package from the ACK app and processing it) inside a
network namespace that has *only* the loopback interface (when your system allows it), logs every connection made by any
program, including `ffmpeg`, and fails on anything that isn't this computer. It first proves that `1.1.1.1` and a web address
are unreachable, so a pass shows nothing *needs* the network, not only that nothing used it.

**Check your own training.** Training is a separate program and was not run under these checks:

```bash
strace -f -qq -e trace=connect,sendto -o /tmp/train.log python3 -m piper.train fit ...your usual options...
grep -E 'AF_INET6?' /tmp/train.log | grep -v -E '127\.0\.0\.1|::1'
```
The first run will show connections to GitHub's servers (the scorer's download; strace shows addresses, not names). After that it should show nothing but this computer.

**Ask the doctor:** `python -m freeform_studio.doctor` also says whether the speech model is on this computer, whether other
accounts can read your recordings, and whether your recordings or backups are in a folder a cloud service may be uploading.

What was verified, and what was not, when this was written (2026-10-01):

* Verified by measurement: the server, the command-line tools and `ffmpeg`, driven through the full workflow with a stand-in
  speech engine, made no connection to anything but this computer, and the whole workflow passed with no network at all.
  The speech model loader makes zero connections in local-only mode. (The phone app's own checks, no network permission and no
  cloud backup, are kept with the phone app, in its repository.)
* **Not measured:** a real speech model run end to end (the network where it was built blocks Hugging Face), a real training
  run, and a real phone. Those are covered by reading the code and by the checks above that you can run.

## 4. Phones and shared computers

* **Phone browser.** Browser sync can upload your history, and the link you open was once in the address bar with the access
  token in it. (The server now moves you to a clean address on the first visit, but the first visit happened.) Use a browser
  profile with sync off, or a browser without an account, for this page. If the phone is shared, clear the site's data in the
  browser's settings when you finish. The phone's keyboard, voice typing and any screen-recording or backup apps are outside
  this project's control.
* **The start-up message prints the access link.** Don't share a screenshot of the terminal. The token only works on your own
  network, but it opens your recordings.
* **Your network.** `--host 0.0.0.0` lets other devices on your network reach the server. Keep the access token on (the
  default), use `https` (the phone microphone needs it anyway), and don't run it on a public or shared Wi-Fi.
* **Packages from the ACK app.** A package is a recording of a voice, so treat the `.zip` like the recordings themselves: carry it by cable or
  USB drive, keep it out of cloud-synced folders, and delete your copies when you no longer need them (the program never does). ACK's *save*
  button writes the file where you choose and offers it to no other app, on purpose.
* **Shared computers.** New files are readable by your account only, but older files keep the permissions they had (`doctor`
  tells you). On a computer others use, use your own Windows account or WSL distribution, and turn on disk encryption
  (BitLocker on Windows). Nothing here can protect a recording from someone with your logged-in session.
* **Cloud-synced folders.** Don't keep recordings or backups in OneDrive, Dropbox, Google Drive, iCloud, or your Windows
  `Documents` or `Desktop` folders. `/mnt/c/Users/<you>/freeform-backups` is a reasonable place; check it isn't synced.

## 5. If the voice isn't yours (SLPs, family, support workers)

A voice recording can identify a person, and what they say may be health information. Depending on where you work, rules such
as HIPAA (US), or GDPR and UK GDPR (where a voice recording used to identify someone can be treated as biometric data), may
apply. Ask your organization's privacy officer. Some things to settle with the person (or their guardian) *before* you record:

1. **Consent, in a form they can understand.** What is recorded, that it trains a synthetic copy of their voice, where it is
   kept, who can hear it, how long it is kept, and that they can stop and ask for it to be deleted. Offer it in the person's
   own communication mode.
2. **What the finished voice could be used for.** A voice model can imitate the person. Say who may have the file and under
   what conditions. Treat the `.onnx` file as sensitive as the recordings.
3. **One person, one set of folders.** Use a separate `--output` folder (or Windows user or WSL distribution) per client, so
   recordings, backups and training data are never mixed.
4. **What "delete" means here.** The tool never deletes your recordings, and only prunes its own old backups by a stated rule.
   So deleting a person's data is a job to do on purpose, and it spans several places:
   * the recordings: `output/_freeform/<code>/takes/` and `retired/`, and `output/<code>/freeform/`
   * every backup: `python -m freeform_studio.backup --list`, then delete those files from the backup folder
   * the training data: `~/piper/freeform-dataset-*` and `~/piper/my-training/` (its `cache-*` folders hold processed audio)
   * the checkpoints (`~/piper/checkpoints/`, `lightning_logs/`) and the exported `.onnx`/`.onnx.json`. **A checkpoint contains
     what the model learned about the voice, and it cannot be "un-trained", so delete them if consent is withdrawn.**
   * copies on phones, USB drives and other computers, and the voice imported into the ACK app
   * **on the phone, in the ACK app:** its DELETE DATA (PROTOCOL → DATA PORT) lists every area it holds and asks twice before it deletes one; DELETE CUSTOM VOICE
     (AUDIO ARCHITECT) removes the imported voice; and Android's own **Clear storage** (Settings, Apps, ACK, Storage; the wording varies by phone) is the complete route
     and returns ACK to a new install. The phone app's repository describes each area. The paired watch may keep Target Computer names until it next connects
   * nothing in ACK or in this tool removes a file you saved elsewhere (an export, a package, a backup, a voice `.zip`) or anything you copied to
     another app. Delete those yourself
5. **Handing over.** Give the person their recordings and voice, then delete your copies of everything above.
6. **The base voice's license.** A voice trained from a base checkpoint is a derivative of it, and base voices come with their
   own conditions. Read the base voice's `MODEL_CARD` (Piper's documentation says some voices have restrictive licenses) and
   note which base you used next to the finished voice. See `THIRD_PARTY_NOTICES.md`.

## 6. What this does not protect against

* Malware, or anyone using your logged-in computer. Recordings are ordinary files.
* Copies you make yourself (a USB stick, an email, a cloud drive, a chat window).
* Hosted AI tools and websites you paste data into.
* The phone's own operating system and apps.
* **The phone app's own storage is not encrypted and it has no app lock.** The phone's lock screen is the only barrier: anyone who can unlock the
  phone, or read its storage with the right tool, can read what ACK holds.
* An **EXPORT .JSON** file, a **safety copy**, a voice or GIF `.zip`, a **training package**, an ACK Voice Studio **backup** or a saved
  **problem report** can be read by anyone who gets the file. None of them has a password.
* The watch link: see section 8.
* A synced folder this software can't recognise: the sync check looks at folder names, and only ever says "may".

## 7. How these rules are kept

They are checked by tests, so a change that breaks one fails before it ships: `test_no_network.py` (no connections, no web
addresses in shipped files), `test_privacy.py` (offline model loading, owner-only files, browser caching, the clean link, synced
folders), `test_sovereignty_policy.py` (the phone app: no network permission, no cloud backup, no network code; it needs the phone app's source and is skipped without it) and
`test_license_headers.py` (licensing). ACK Voice Studio has its own: `test_vs_network_rules.py` (only the download module may import anything that can reach the network or start a program, no web address is written anywhere but the list of downloads and the bootstrap script, and `System.run` refuses network programs), `test_vs_it_guide.py` (the hosts in the IT guide are the hosts the code knows, and the update and report commands reach no network), `test_vs_areas.py` (every folder the tool makes is in an area that says whether a backup holds it and whether it can be deleted), `test_vs_report.py` and `test_vs_reportcmd_flow.py` (a problem report is checked with planted names and cannot hold a recording or a phrase) and `test_vs_data_sovereignty_doc.py` (this page's rows about it are the code's).

The phone app's own guards (that its EXPORT .JSON warning describes every field, and that its DELETE DATA covers every place it stores data) are tests in the phone app's
repository. To keep a copy of what the phone holds, or to move to a new phone without a cable, use ACK's own export; those files stay under your control.

## 8. Can the watch link leave your devices? (ACK Wear)

This is about the phone app and its watch companion, not about this tool. **Short answer: yes, it can, and the phone app does not control it.** The full explanation, with
what Google says word for word, what was read and when, and what was not checked, is in the phone app's repository (`ASPDesignLabs/ACK`, `docs/DATA_SOVEREIGNTY.md`, section 8).
If a voice's data must never reach Google's servers, do not use the watch app. Nothing in ACK Voice Studio or Freeform Studio sends anything to a watch.
