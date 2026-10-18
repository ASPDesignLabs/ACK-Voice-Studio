# SPDX-License-Identifier: GPL-3.0-or-later
"""Where the ACK phone app's source is, for the few tests that check this tool against what the app reads (the voice file's layout, the list of sounds, the colours).

The phone app lives in its own repository (ASPDesignLabs/ACK). A test that reads it looks in the folder named by the environment variable ACK_SOURCE, else in a folder called ACK next
to this repository. With neither, those tests are SKIPPED, and the reason says how to run them: they are never passed without having looked. If ACK_SOURCE is set to a folder that does
not hold the app, that is an error, because a typing mistake must not turn into a quiet skip.
"""
import os
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
APP = Path("app/src/main/java/com/example/besu")
HOW = "needs a checkout of the ACK phone app: put it next to this repository as ../ACK, or set ACK_SOURCE to its folder"


def find(environ=None, repo=REPO):
    """The folder that holds the phone app's source, or None when there is none. Raises when ACK_SOURCE names a folder that does not."""
    environ = os.environ if environ is None else environ
    named = environ.get("ACK_SOURCE")
    if named:
        if not (Path(named) / APP).is_dir():
            raise RuntimeError("ACK_SOURCE is %r, but %s is not inside it: point it at the folder of the ACK phone app's repository" % (named, APP))
        return Path(named)
    sibling = Path(repo).parent / "ACK"
    return sibling if (sibling / APP).is_dir() else None


ACK = find()
needs_ack = pytest.mark.skipif(ACK is None, reason=HOW)


def path(*parts):
    """A path inside the phone app's checkout. Only call it from a test marked `needs_ack` (or after checking ACK is not None)."""
    assert ACK is not None, HOW
    return ACK.joinpath(*parts)
