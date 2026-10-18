# SPDX-License-Identifier: GPL-3.0-or-later
"""How the few tests that read the ACK phone app's source find it (vs_ack_source.py): ACK_SOURCE, else a folder called ACK beside this repository, else they are skipped saying how to
run them. A wrong ACK_SOURCE is an error, never a quiet skip. Also: no test file reads the phone app any other way, so none can fail (or, worse, pass) without it."""
import re
from pathlib import Path

import pytest

import vs_ack_source as ack

HERE = Path(__file__).resolve().parent


def make_app(folder):
    (Path(folder) / ack.APP).mkdir(parents=True)
    return Path(folder)


def test_a_named_folder_is_used(tmp_path):
    app = make_app(tmp_path / "somewhere")
    assert ack.find({"ACK_SOURCE": str(app)}, repo=tmp_path / "repo") == app


def test_a_named_folder_that_does_not_hold_the_app_is_an_error_not_a_skip(tmp_path):
    (tmp_path / "empty").mkdir()
    with pytest.raises(RuntimeError, match="ACK_SOURCE"):
        ack.find({"ACK_SOURCE": str(tmp_path / "empty")}, repo=tmp_path / "repo")
    with pytest.raises(RuntimeError, match="ACK_SOURCE"):
        ack.find({"ACK_SOURCE": str(tmp_path / "missing")}, repo=tmp_path / "repo")


def test_the_named_folder_wins_over_the_one_beside_the_repository(tmp_path):
    beside = make_app(tmp_path / "ACK")
    named = make_app(tmp_path / "other")
    assert ack.find({"ACK_SOURCE": str(named)}, repo=tmp_path / "repo") == named
    assert ack.find({}, repo=tmp_path / "repo") == beside


def test_a_folder_called_ACK_beside_the_repository_is_found(tmp_path):
    repo = tmp_path / "work" / "repo"
    assert ack.find({}, repo=repo) is None, "nothing there: skipped, not guessed"
    (tmp_path / "work" / "ACK").mkdir(parents=True)
    assert ack.find({}, repo=repo) is None, "a folder called ACK that is not the phone app does not count"
    beside = make_app(tmp_path / "work" / "ACK")
    assert ack.find({}, repo=repo) == beside
    assert ack.find({}, repo=tmp_path / "elsewhere" / "repo") is None, "only the folder beside the repository counts"


def test_an_empty_ACK_SOURCE_is_the_same_as_none(tmp_path):
    assert ack.find({"ACK_SOURCE": ""}, repo=tmp_path / "repo") is None


def test_the_skip_says_how_to_run_the_tests():
    mark = ack.needs_ack.mark
    assert mark.name == "skipif" and "../ACK" in mark.kwargs["reason"] and "ACK_SOURCE" in mark.kwargs["reason"]


def test_no_test_reads_the_phone_app_except_through_the_helper():
    """A test that names the app's source folder must import the helper: the helper is what skips it when the app is not there."""
    offenders = []
    for path in sorted(HERE.glob("test_vs_*.py")):
        if path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8")
        reads_app = re.search(r"""["']app["']\s*[,/]\s*["']src["']|app/src/|["']app["']\s*/\s*["'](?:libs|src)""", text)
        if reads_app and "vs_ack_source" not in text:
            offenders.append(path.name)
    assert not offenders, "reads the phone app's files without vs_ack_source: %s" % offenders
