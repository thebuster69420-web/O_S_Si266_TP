# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Partea 4: Alte module din biblioteca standard (exercițiile 35–43)

import hashlib
import json
import re
import socket
import ssl
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

# Directorul în care se află acest fișier (web_lab), ca headers.json să fie
# salvat aici indiferent din ce director rulăm scriptul.
FOLDER = Path(__file__).parent


# ---------------------------------------------------------------------------
# Exercițiul 35. Descompunerea unui URL
# ---------------------------------------------------------------------------
def show_url_parts(url: str) -> None:
    """Afișează componentele unui URL obținute cu urlparse()."""
    parti = urlparse(url)
    print("scheme:  ", parti.scheme)
    print("netloc:  ", parti.netloc)
    print("path:    ", parti.path)
    print("query:   ", parti.query)
    print("fragment:", parti.fragment)


# ---------------------------------------------------------------------------
# Exercițiul 36. Compunerea URL-urilor
# ---------------------------------------------------------------------------
def make_absolute(base: str, links: list[str]) -> list[str]:
    """Transformă legăturile relative din links în URL-uri complete, față de base."""
    return [urljoin(base, link) for link in links]


# ---------------------------------------------------------------------------
# Exercițiul 37. Extragerea legăturilor
# ---------------------------------------------------------------------------
def extract_links(html: str) -> list[str]:
    """Returnează toate valorile href="..." din html, fără duplicate.

    Ordinea din pagină se păstrează (dict.fromkeys elimină duplicatele
    fără să schimbe ordinea).
    """
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


# ---------------------------------------------------------------------------
# Exercițiul 38. Interne sau externe?
# ---------------------------------------------------------------------------
def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Împarte legăturile în (interne, externe) față de domain.

    Fiecare legătură e transformată întâi în URL complet cu urljoin(), apoi
    comparăm urlparse().netloc cu domeniul. Legăturile care nu sunt pagini
    web (mailto:, tel:, javascript:) sunt ignorate.
    """
    base = f"https://{domain}/"
    domeniu = domain.lower().removeprefix("www.")
    interne, externe = [], []
    for link in links:
        complet = urljoin(base, link)
        parti = urlparse(complet)
        if parti.scheme not in ("http", "https"):
            continue
        host = parti.netloc.lower().removeprefix("www.")
        if host == domeniu:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe


# ---------------------------------------------------------------------------
# Exercițiul 39. Propriile metode
# ---------------------------------------------------------------------------
class ImageFinder(HTMLParser):
    """Parser HTML care colectează atributul src al fiecărui tag <img>."""

    def __init__(self):
        """Inițializează parserul și lista goală de imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Apelată automat de HTMLParser pentru fiecare tag de deschidere.

        HTMLParser transformă deja numele tag-ului și al atributelor în
        litere mici, deci <IMG SRC=...> ajunge aici ca tag="img", "src".
        """
        if tag == "img":
            src = dict(attrs).get("src")
            if src:  # ignorăm <img> fără src
                self.images.append(src)


# ---------------------------------------------------------------------------
# Exercițiul 40. Amprenta paginii
# ---------------------------------------------------------------------------
def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 (hexazecimal) a conținutului paginii url."""
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


# ---------------------------------------------------------------------------
# Exercițiul 41. Salvarea în JSON
# ---------------------------------------------------------------------------
def save_headers(url: str, filename: str = "headers.json") -> Path:
    """Salvează antetele paginii url într-un fișier JSON și returnează calea lui."""
    response = requests.get(url, timeout=TIMEOUT)
    cale = FOLDER / filename
    with open(cale, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2, ensure_ascii=False)
    return cale


def load_headers(cale: Path) -> dict:
    """Încarcă antetele salvate anterior din fișierul JSON."""
    with open(cale, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------------------------
# Exercițiul 42. Interogare DNS
# ---------------------------------------------------------------------------
def resolve(hostname: str) -> str:
    """Returnează adresa IPv4 a domeniului hostname."""
    return socket.gethostbyname(hostname)


# ---------------------------------------------------------------------------
# Exercițiul 43. Expirarea certificatului
# ---------------------------------------------------------------------------
def cert_days_left(hostname: str) -> int:
    """Se conectează la portul 443 și returnează câte zile mai are certificatul."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])  # secunde de la 1970
    return int((expira - time.time()) // 86400)          # 86400 s = o zi


# ===========================================================================
# Apelarea funcțiilor
# ===========================================================================
if __name__ == "__main__":
    print("=== Exercițiul 35 ===")
    show_url_parts("https://cybercor.org/path?x=1#top")

    print("\n=== Exercițiul 36 ===")
    for link in make_absolute(BASE_URL, ["/about", "contact.html", "../index.html"]):
        print(link)

    print("\n=== Exercițiul 37 ===")
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    links = extract_links(response.text)
    print(len(links), "legături unice:")
    for link in links:
        print(" ", link)

    print("\n=== Exercițiul 38 ===")
    interne, externe = split_links(links, urlparse(BASE_URL).netloc)
    print("Interne:", len(interne))
    print("Externe:", len(externe))
    for link in externe:
        print(" ", link)

    print("\n=== Exercițiul 39 ===")
    # Pasul 1: testul pe HTML cunoscut
    test_html = """
    <html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fără src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    print(finder.images)
    assert finder.images == [
        "/logo.png",                            # imagine obișnuită
        "poza.jpg",                             # tag scris cu majuscule
        "https://cdn.example.com/banner.webp",  # tag care se închide singur
    ], "Parserul nu a găsit exact imaginile așteptate"
    print("Testul a trecut!")

    # Pasul 2: pagina reală (refolosim răspunsul din exercițiul 37)
    finder = ImageFinder()
    finder.feed(response.text)
    print(len(finder.images), "imagini găsite")
    for src in finder.images:
        print(" ", src)
    print("Verificare: '<img' apare de", response.text.lower().count("<img"), "ori în cod")
    # O listă goală nu e neapărat o greșeală: site-ul poate afișa imaginile
    # prin CSS (background-image) sau SVG, nu prin tag-uri <img>.
    time.sleep(1)

    print("\n=== Exercițiul 40 ===")
    amprenta1 = page_fingerprint(BASE_URL)
    time.sleep(1)
    amprenta2 = page_fingerprint(BASE_URL)
    print("Prima rulare: ", amprenta1)
    print("A doua rulare:", amprenta2)
    print("Identice:", amprenta1 == amprenta2)
    # Amprentele sunt identice dacă pagina nu s-a schimbat. Ar fi diferite
    # dacă s-a modificat conținutul paginii între cereri sau dacă pagina
    # conține ceva generat la fiecare încărcare (ora curentă, un token de
    # securitate, reclame, un număr aleator). Orice octet schimbat dă o
    # amprentă complet diferită.
    time.sleep(1)

    print("\n=== Exercițiul 41 ===")
    cale = save_headers(BASE_URL)
    print("Antete salvate în", cale)
    incarcate = load_headers(cale)
    print("Content-Type din fișier:", incarcate.get("Content-Type", "lipsește"))

    print("\n=== Exercițiul 42 ===")
    print("Adresa IP a cybercor.org:", resolve("cybercor.org"))

    print("\n=== Exercițiul 43 ===")
    print("Certificatul expiră peste", cert_days_left("cybercor.org"), "zile")

# Verificați-vă: în exercițiul 39, cine apelează handle_starttag()?
# Metoda feed() din clasa HTMLParser. Când îi dăm HTML cu finder.feed(...),
# HTMLParser citește textul și, de fiecare dată când întâlnește un tag de
# deschidere, apelează singur self.handle_starttag(tag, attrs). Noi doar am
# suprascris metoda ca să spunem CE să se întâmple atunci; CÂND să fie
# apelată decide clasa părinte.
