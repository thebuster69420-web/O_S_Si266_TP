import os
from collections import Counter
import pytest
from arsenal.aparare.detector import secunde, esecuri_cu_ora, pe_ip_in_fereastra, top

JURNAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start", "auth.log")


def test_secunde_din_rand():
    rand = "Nov  2 09:16:03 srv sshd[2051]: Failed password for root from 203.0.113.9 port 51230 ssh2"
    assert secunde(rand) == 9 * 3600 + 16 * 60 + 3
    assert secunde("<linie stricata fara structura>") is None


def test_fereastra_separa_atacul_dens():
    esecuri = [{"user": "root", "ip": "a", "t": 0},
               {"user": "root", "ip": "a", "t": 5},
               {"user": "root", "ip": "a", "t": 9},
               {"user": "root", "ip": "b", "t": 0},
               {"user": "root", "ip": "b", "t": 500}]
    c = pe_ip_in_fereastra(esecuri, 60)
    assert c["a"] == 3
    assert c["b"] == 1


def test_fereastra_pe_jurnal():
    c = pe_ip_in_fereastra(esecuri_cu_ora(JURNAL), 60)
    assert c["203.0.113.9"] == 13
    assert c["198.51.100.7"] == 1


def test_fereastra_invalida():
    with pytest.raises(ValueError):
        pe_ip_in_fereastra([], 0)


def test_top_pastreaza_primele():
    c = Counter({"a": 13, "b": 2, "c": 5})
    assert top(c, 2) == {"a": 13, "c": 5}
    with pytest.raises(ValueError):
        top(c, 0)
