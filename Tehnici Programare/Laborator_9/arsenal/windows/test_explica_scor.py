import os
from arsenal.windows.inventar import Eveniment, Inventar, evenimente_din_json

START = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")


def test_explica_id_cunoscute():
    assert "brute force" in Eveniment(4625, "warning", "Security", "administrator", "m").explica()
    assert "sters" in Eveniment(1102, "critical", "Security", "administrator", "m").explica()
    assert "serviciu nou" in Eveniment(7045, "warning", "Service Control Manager", "SYSTEM", "m").explica()
    assert "4624" in Eveniment(4624, "information", "Security", "ana", "m").explica()


def test_scor_pe_capturi():
    inv = Inventar.din_json(os.path.join(START, "procese.json"))
    ev = evenimente_din_json(os.path.join(START, "evenimente.json"))
    assert inv.scor(ev) == 7
    assert Inventar([]).scor([]) == 0
