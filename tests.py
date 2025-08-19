#!/usr/bin/env python3

from pathlib import Path

from one import One, Ref


EXAMPLES = Path("examples")


nt_001 = One(EXAMPLES / "nt_001.tsv")

assert nt_001.get(bcv_id="640102").text == "οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν."


nt_002 = One(EXAMPLES / "nt_002.tsv")

assert nt_002.get(token_id="49063").text == "ἀρχῇ"

assert (
    " ".join(row.text for row in nt_002.rows(token_id=Ref("49079-49085")))
    == nt_001.get(bcv_id="640102").text
)


nt_003 = One(EXAMPLES / "nt_003.tsv")

assert nt_003.get(token_id="49078").lemma == "λόγος"

nt_004 = One(EXAMPLES / "nt_004.tsv")

assert nt_004.get(token_id="49078").lemma == "λόγος"


nt_005 = One(EXAMPLES / "nt_005.tsv")

assert nt_005.get(token_id="49063").bcv_ref.raw == "640101#3-#6"


nt_006 = One(EXAMPLES / "nt_006.tsv")

assert nt_006.get(bcv_id="640102").token_ref.raw == "49079-49085"

assert Ref("49079-49085") == Ref("49079-49085")
