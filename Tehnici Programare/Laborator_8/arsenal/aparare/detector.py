# -*- coding: utf-8 -*-
"""Laboratorul 8 - partea B. Detectorul de brute force."""
import argparse, json, re
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip, esec


def suspecti(counts, prag=10):
    """Sarcina 5. Adresele cu cel putin prag esecuri, cele mai multe intai.

    counts e un Counter (sau dict) ip -> numar. Intoarce o lista de perechi
    (ip, numar) cu numar >= prag, sortata descrescator dupa numar.

    Parametrul prag are valoarea implicita 10. Daca prag e sub 1, opreste
    functia cu:  raise ValueError("prag invalid: <prag> (cel putin 1)")

    suspecti(Counter({"203.0.113.9": 13, "198.51.100.7": 2}))
        ->  [('203.0.113.9', 13)]
    suspecti(acelasi, prag=2)
        ->  [('203.0.113.9', 13), ('198.51.100.7', 2)]
    """
    if prag < 1:
        raise ValueError("prag invalid: %s (cel putin 1)" % prag)
    rezultat = []
    for ip, n in Counter(counts).most_common():
        if n >= prag:
            rezultat.append((ip, n))
    return rezultat

def raport_json(cale, prag=10):
    """Sarcina 6. Raportul complet, ca dictionar gata de pus in JSON.

    Leaga parse-ul cu detectorul si intoarce un dictionar cu trei chei:
        {"esecuri": numarul total de esecuri,
         "pe_ip": dictionar simplu ip -> numar (foloseste dict(...)),
         "suspecti": lista de (ip, numar) de la suspecti(counts, prag)}

    Nu tipari; doar intoarce. Cu acest dictionar, main() scoate JSON-ul.
    """
    esecuri = citeste_esecuri(cale)
    counts = pe_ip(esecuri)
    return {"esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": suspecti(counts, prag)}

def e_brute_force(counts, ip, prag=10):
    """Sarcina 7. Spune daca o adresa e un atac brute force.

    Intoarce True daca adresa ip are cel putin prag esecuri in counts,
    altfel False. Foloseste counts.get(ip, 0), ca sa nu crape pentru o
    adresa care nu apare deloc.

    e_brute_force(Counter({"203.0.113.9": 13}), "203.0.113.9")  ->  True
    e_brute_force(acelasi, "198.51.100.7")                      ->  False
    e_brute_force(acelasi, "lipsa")                             ->  False
    """
    if counts.get(ip, 0) >= prag:
        return True
    return False

def utilizatori_tintiti(esecuri, ip):
    """Sarcina 8. Ce utilizatori a incercat o anumita adresa.

    Primeste lista de esecuri si o adresa. Intoarce MULTIMEA numelor de
    utilizator incercate DE la acea adresa (fara dubluri).

    Pentru atacator iese o multime cu mai multe nume (root, admin, ...);
    multimea arunca singura repetarile.
    """
    useri = set()
    for e in esecuri:
        if e["ip"] == ip:
            useri.add(e["user"])
    return useri


ORA = re.compile(r"(\d\d):(\d\d):(\d\d)")


def secunde(linie):
    m = ORA.search(linie)
    if m is None:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))


def esecuri_cu_ora(cale):
    esecuri = []
    try:
        with open(cale, encoding="utf-8") as f:
            for linie in f:
                r = esec(linie)
                t = secunde(linie)
                if r is not None and t is not None:
                    esecuri.append({"user": r[0], "ip": r[1], "t": t})
    except FileNotFoundError:
        print("Nu gasesc fisierul:", cale)
    return esecuri


def pe_ip_in_fereastra(esecuri, fereastra):
    if fereastra < 1:
        raise ValueError("fereastra invalida: %s (cel putin 1 secunda)" % fereastra)
    ore = {}
    for e in esecuri:
        ore.setdefault(e["ip"], []).append(e["t"])
    counts = Counter()
    for ip, lista in ore.items():
        maxim = 0
        for inceput in lista:
            n = 0
            for t in lista:
                if inceput <= t <= inceput + fereastra:
                    n += 1
            if n > maxim:
                maxim = n
        counts[ip] = maxim
    return counts


def top(counts, n):
    if n < 1:
        raise ValueError("top invalid: %s (cel putin 1)" % n)
    return {ip: k for ip, k in Counter(counts).most_common(n)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('log')
    p.add_argument('--prag', type=int, default=10)
    p.add_argument('--json', action='store_true')
    p.add_argument('--top', type=int)
    p.add_argument('--fereastra', type=int)
    a = p.parse_args()
    if a.fereastra is None:
        esecuri = citeste_esecuri(a.log)
        counts = pe_ip(esecuri)
    else:
        esecuri = esecuri_cu_ora(a.log)
        counts = pe_ip_in_fereastra(esecuri, a.fereastra)
    sus = suspecti(counts, a.prag)
    if a.top is None:
        adrese = dict(counts.most_common())
    else:
        adrese = top(counts, a.top)
    if a.json:
        print(json.dumps({'esecuri': len(esecuri),
                          'pe_ip': adrese,
                          'suspecti': sus}, indent=2))
        return
    print('Esecuri de autentificare:', len(esecuri))
    if a.fereastra is not None:
        print('Cele mai multe esecuri in %d secunde, pe adresa:' % a.fereastra)
    for ip, n in adrese.items():
        print('  %s: %d' % (ip, n))
    print('Suspecti (prag %d):' % a.prag)
    for ip, n in sus:
        print('  %s  (%d incercari)  BRUTE FORCE' % (ip, n))


if __name__ == '__main__':
    main()
