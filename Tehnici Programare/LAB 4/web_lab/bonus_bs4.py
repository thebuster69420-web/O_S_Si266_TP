# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266
#
# Bonus: get_title() și extract_links() rescrise cu BeautifulSoup.
# Instalare: py -m pip install beautifulsoup4

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
    raise SystemExit(1)

import webtools


def get_title_bs4(html: str) -> str | None:
    """Returnează titlul paginii folosind BeautifulSoup, sau None dacă lipsește."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else None


def extract_links_bs4(html: str) -> list[str]:
    """Returnează toate legăturile href ale tag-urilor <a>, fără duplicate."""
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(a["href"] for a in soup.find_all("a", href=True)))


if __name__ == "__main__":
    html = requests.get(BASE_URL, timeout=TIMEOUT).text

    print("Titlu (manual):", webtools.get_title(html))
    print("Titlu (bs4):   ", get_title_bs4(html))
    print("Legături (regex):", len(webtools.extract_links(html)))
    print("Legături (bs4):  ", len(extract_links_bs4(html)))

# Comparație:
# - Mai scurt: get_title are 1–2 linii în loc de ~10; nu mai calculăm poziții
#   cu find() și feliere.
# - Mai sigur: BeautifulSoup înțelege HTML-ul real. Găsește <TITLE> cu
#   majuscule, <title> cu atribute, href scris cu ghilimele simple
#   (href='...') sau fără ghilimele, pe care regex-ul r'href="([^"]+)"' le
#   ratează. Regex-ul prinde însă și href-uri din <link> (CSS, favicon), nu
#   doar din <a>, de aceea numerele pot diferi.
