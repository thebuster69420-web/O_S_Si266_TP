# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266
#
# webtools.py — modulul propriu cu toate funcțiile reutilizabile (Partea 5).
# Se importă din main.py la fel cum importăm requests.

import json
import re
import socket
import ssl
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

TIMEOUT = 10  # secunde

# Exercițiul 47. Constantă de modul: antetele trimise la fiecare cerere
DEFAULT_HEADERS = {"User-Agent": "WebLab-Secrieru-Octavian"}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

# Directorul web_lab: aici se salvează report.json, oricare ar fi directorul
# din care se rulează programul.
FOLDER = Path(__file__).parent


# ---------------------------------------------------------------------------
# Funcții mutate din Partea 3 (exercițiul 44)
# ---------------------------------------------------------------------------
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă adresa url (cu DEFAULT_HEADERS) și returnează obiectul răspuns."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str | None:
    """Returnează textul dintre <title> și </title>, sau None dacă lipsește."""
    lower = html.lower()
    pos = lower.find("<title")
    if pos == -1:
        return None
    start = lower.find(">", pos) + 1
    end = lower.find("</title>", start)
    if end == -1:
        return None
    return html[start:end].strip()


def security_headers(url: str) -> dict[str, bool]:
    """Verifică cele 5 antete de securitate și returnează {antet: True/False}."""
    response = fetch(url)
    return {antet: antet in response.headers for antet in SECURITY_HEADERS}


def score_headers(results: dict[str, bool]) -> str:
    """Primește rezultatul lui security_headers() și returnează un scor ca "3/5"."""
    prezente = sum(1 for valoare in results.values() if valoare)
    return f"{prezente}/{len(results)}"


def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Verifică fiecare cale din paths și returnează {cale: cod_de_stare}."""
    base = base.rstrip("/")
    rezultate = {}
    for i, path in enumerate(paths):
        if i > 0:
            time.sleep(1)
        rezultate[path] = get_status(base + path)
    return rezultate


def fetch_robots(base: str) -> str | None:
    """Returnează textul fișierului /robots.txt, sau None dacă acesta lipsește."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Returnează lista valorilor Disallow: din robots.txt ([] pentru None)."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        linie = linie.strip()
        if linie.lower().startswith("disallow:"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:
                cai.append(valoare)
    return cai


# ---------------------------------------------------------------------------
# Funcții mutate din Partea 4
# ---------------------------------------------------------------------------
def extract_links(html: str) -> list[str]:
    """Returnează toate valorile href="..." din html, fără duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Împarte legăturile în (interne, externe) față de domain."""
    base = f"https://{domain}/"
    domeniu = domain.lower().removeprefix("www.")
    interne, externe = [], []
    for link in links:
        complet = urljoin(base, link)
        parti = urlparse(complet)
        if parti.scheme not in ("http", "https"):
            continue  # mailto:, tel:, javascript: nu sunt pagini web
        if parti.netloc.lower().removeprefix("www.") == domeniu:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe


def resolve(hostname: str) -> str:
    """Returnează adresa IPv4 a domeniului hostname."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Se conectează la portul 443 și returnează câte zile mai are certificatul."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expira - time.time()) // 86400)


# ---------------------------------------------------------------------------
# Funcție nouă pentru raport: lanțul de redirecționări
# ---------------------------------------------------------------------------
def redirect_chain(url: str) -> list[dict]:
    """Pornește de la varianta http:// a lui url și returnează redirecționările.

    Rezultatul e o listă de dicționare {"status": cod, "to": URL-ul următor}.
    Listă goală înseamnă că nu a existat nicio redirecționare.
    """
    parti = urlparse(url)
    http_url = "http://" + parti.netloc + parti.path
    response = fetch(http_url)
    lant = []
    pasi = response.history + [response]
    for curent, urmator in zip(pasi, pasi[1:]):
        lant.append({"status": curent.status_code, "to": urmator.url})
    return lant


# ---------------------------------------------------------------------------
# Exercițiul 50. Proiect final: raportul site-ului
# ---------------------------------------------------------------------------
def site_report(url: str, filename: str = "report.json") -> dict:
    """Colectează informații despre site, le afișează și le salvează în JSON.

    Raportul conține: codul de stare și URL-ul final, titlul, adresa IP,
    redirecționările de la http://, scorul antetelor de securitate, zilele
    rămase până la expirarea certificatului, numărul de legături interne și
    externe și căile interzise din robots.txt. Returnează raportul ca dicționar.
    """
    hostname = urlparse(url).hostname

    # 1. Codul de stare și URL-ul final + 2. Titlul (o singură cerere)
    response = fetch(url)
    html = response.text
    time.sleep(1)

    # 3. Adresa IP (DNS, nu e cerere HTTP)
    ip = resolve(hostname)

    # 4. Lanțul de redirecționări pornind de la http://
    lant = redirect_chain(url)
    time.sleep(1)

    # 5. Scorul antetelor de securitate
    antete = security_headers(url)
    time.sleep(1)

    # 6. Zilele rămase până la expirarea certificatului
    zile = cert_days_left(hostname)

    # 7. Legături interne și externe (din HTML-ul descărcat la pasul 1)
    interne, externe = split_links(extract_links(html), urlparse(response.url).netloc)

    # 8. Căile interzise din robots.txt
    cai = disallowed_paths(fetch_robots(url))

    raport = {
        "url": url,
        "status_code": response.status_code,
        "final_url": response.url,
        "title": get_title(html),
        "ip_address": ip,
        "redirects": lant,
        "security_headers": antete,
        "security_score": score_headers(antete),
        "cert_days_left": zile,
        "internal_links": len(interne),
        "external_links": len(externe),
        "disallowed_paths": cai,
    }

    # Afișarea
    if lant:
        text_redir = ", ".join(f"{pas['status']} -> {pas['to']}" for pas in lant)
    else:
        text_redir = "niciuna"
    print(f"=== Raport site: {url} ===")
    print("Cod de stare:", response.status_code)
    print("URL final:", response.url)
    print("Titlu:", raport["title"] or "fără titlu")
    print("Adresă IP:", ip)
    print("Redirecționări:", text_redir)
    print("Scor securitate:", raport["security_score"])
    print(f"Certificat: {zile} de zile rămase")
    print(f"Legături: {len(interne)} interne, {len(externe)} externe")
    print("Căi interzise:", ", ".join(cai) if cai else "niciuna")

    # Salvarea
    cale = FOLDER / filename
    with open(cale, "w", encoding="utf-8") as file:
        json.dump(raport, file, indent=2, ensure_ascii=False)
    print("Salvat în", cale.name)

    return raport


# ---------------------------------------------------------------------------
# Exercițiul 46. Blocul main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
