# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Partea 3: Scrierea propriilor funcții (exercițiile 21–34)

import time
import requests


# ---------------------------------------------------------------------------
# Exercițiul 21 + 23. fetch() cu parametru implicit
# ---------------------------------------------------------------------------
def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Descarcă adresa url și returnează obiectul răspuns.

    timeout are valoarea implicită 10 secunde (exercițiul 23).
    """
    return requests.get(url, timeout=timeout)


# ---------------------------------------------------------------------------
# Exercițiul 22. Returnarea unei singure valori
# ---------------------------------------------------------------------------
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


# ---------------------------------------------------------------------------
# Exercițiul 24 + 25. get_title() cu docstring
# ---------------------------------------------------------------------------
def get_title(html: str) -> str | None:
    """Returnează titlul paginii din codul HTML primit.

    Caută textul dintre <title> și </title>, îl curăță de spații și îl
    returnează. Dacă pagina nu are titlu, returnează None.
    Funcția nu face nicio cerere de rețea: primește HTML-ul gata descărcat.
    """
    lower = html.lower()  # ca să găsim și <TITLE> scris cu majuscule
    pos = lower.find("<title")
    if pos == -1:
        return None
    start = lower.find(">", pos) + 1  # sare și peste eventuale atribute
    end = lower.find("</title>", start)
    if end == -1:
        return None
    return html[start:end].strip()


# ---------------------------------------------------------------------------
# Exercițiul 27. Fără opriri neașteptate
# ---------------------------------------------------------------------------
def page_exists(url: str) -> bool:
    """Returnează True dacă pagina răspunde cu un cod sub 400, altfel False.

    Orice eroare de rețea (domeniu inexistent, timeout etc.) dă False.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code < 400
    except requests.RequestException:
        return False


# ---------------------------------------------------------------------------
# Exercițiul 28. Returnarea unui dicționar
# ---------------------------------------------------------------------------
def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Verifică fiecare cale din paths și returnează {cale: cod_de_stare}."""
    rezultate = {}
    for i, path in enumerate(paths):
        if i > 0:
            time.sleep(1)  # pauză între cereri repetate
        rezultate[path] = get_status(base + path)
    return rezultate


# ---------------------------------------------------------------------------
# Exercițiul 29. Argumente cu nume
# ---------------------------------------------------------------------------
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea antetului name pentru url, sau default dacă lipsește."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)


# ---------------------------------------------------------------------------
# Exercițiul 30. Antete de securitate
# ---------------------------------------------------------------------------
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def security_headers(url: str) -> dict[str, bool]:
    """Verifică cele 5 antete de securitate și returnează {antet: True/False}."""
    response = requests.get(url, timeout=TIMEOUT)
    return {antet: antet in response.headers for antet in SECURITY_HEADERS}


# ---------------------------------------------------------------------------
# Exercițiul 31. Funcții care apelează funcții
# ---------------------------------------------------------------------------
def score_headers(results: dict[str, bool]) -> str:
    """Primește rezultatul lui security_headers() și returnează un scor ca "3/5"."""
    prezente = sum(1 for valoare in results.values() if valoare)
    return f"{prezente}/{len(results)}"


# ---------------------------------------------------------------------------
# Exercițiul 32. Două funcții, o sarcină
# ---------------------------------------------------------------------------
def fetch_robots(base: str) -> str | None:
    """Returnează textul fișierului /robots.txt, sau None dacă acesta lipsește."""
    try:
        response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Returnează lista valorilor Disallow: din textul robots.txt.

    Dacă primește None (robots.txt lipsește), returnează o listă goală.
    """
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        linie = linie.strip()
        if linie.lower().startswith("disallow:"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:  # "Disallow:" gol înseamnă "totul e permis"
                cai.append(valoare)
    return cai


# ---------------------------------------------------------------------------
# Exercițiul 33. Oricâte argumente
# ---------------------------------------------------------------------------
def response_times(*urls: str) -> dict[str, float]:
    """Măsoară cât durează cererea către fiecare url; returnează {url: secunde}.

    *urls adună toate argumentele poziționale într-un tuplu.
    """
    timpi = {}
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(1)
        start = time.perf_counter()
        requests.get(url, timeout=TIMEOUT)
        timpi[url] = round(time.perf_counter() - start, 3)
    return timpi


# ---------------------------------------------------------------------------
# Exercițiul 34. Argumente cu nume colectate
# ---------------------------------------------------------------------------
def log(message: str, **details) -> None:
    """Afișează mesajul urmat de fiecare detaliu, în forma nume=valoare.

    **details adună toate argumentele cu nume într-un dicționar.
    """
    parti = [message] + [f"{nume}={valoare}" for nume, valoare in details.items()]
    print(" | ".join(parti))


# ===========================================================================
# Apelarea funcțiilor
# ===========================================================================
if __name__ == "__main__":
    print("=== Exercițiul 21 ===")
    response = fetch(BASE_URL)
    print("Cod de stare:", response.status_code)
    time.sleep(1)

    print("\n=== Exercițiul 22 ===")
    for path in ["/", "/robots.txt", "/sitemap.xml"]:
        print(path, "->", get_status(BASE_URL + path))
        time.sleep(1)

    print("\n=== Exercițiul 23 ===")
    print("Cu timeout implicit (10):", fetch(BASE_URL).status_code)
    time.sleep(1)
    print("Cu timeout=3:", fetch(BASE_URL, timeout=3).status_code)
    time.sleep(1)

    print("\n=== Exercițiul 24 ===")
    print("Titlu:", get_title(response.text))  # refolosim HTML-ul deja descărcat

    print("\n=== Exercițiul 25 ===")
    help(get_title)

    print("\n=== Exercițiul 26 ===")
    try:
        get_status(123)
    except Exception as eroare:
        print("Eroare:", type(eroare).__name__, "-", eroare)
    # Adnotările de tip NU opresc programul: Python nu le verifică la rulare.
    # Apelul get_status(123) pornește normal; eroarea apare abia în
    # requests.get(), pentru că "123" nu este un URL valid (lipsește
    # http:// sau https://). Adnotările servesc ca documentație și pentru
    # unelte precum editorul (VS Code) sau mypy, care avertizează înainte
    # de rulare.
    time.sleep(1)

    print("\n=== Exercițiul 27 ===")
    print(BASE_URL, "->", page_exists(BASE_URL))
    time.sleep(1)
    print("domeniu inexistent ->", page_exists("https://this-domain-does-not-exist.invalid"))
    time.sleep(1)

    print("\n=== Exercițiul 28 ===")
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))
    time.sleep(1)

    print("\n=== Exercițiul 29 ===")
    print("Server:", get_header(BASE_URL, name="Server"))
    time.sleep(1)
    print("X-Inventat:", get_header(BASE_URL, name="X-Inventat", default="nu există"))
    time.sleep(1)

    print("\n=== Exercițiul 30 ===")
    rezultate = security_headers(BASE_URL)
    for antet, prezent in rezultate.items():
        print(f"{antet}: {prezent}")
    time.sleep(1)

    print("\n=== Exercițiul 31 ===")
    print("Scor securitate:", score_headers(security_headers(BASE_URL)))
    time.sleep(1)

    print("\n=== Exercițiul 32 ===")
    robots = fetch_robots(BASE_URL)
    print("Căi interzise:", disallowed_paths(robots))
    print("Cu None:", disallowed_paths(None))  # trebuie să dea [] fără eroare
    time.sleep(1)

    print("\n=== Exercițiul 33 ===")
    print(response_times(BASE_URL, BASE_URL + "/robots.txt"))

    print("\n=== Exercițiul 34 ===")
    log("verificat", url=BASE_URL, status=200)

# Verificați-vă: print() în funcție versus return
# print() doar afișează valoarea pe ecran; după aceea valoarea se pierde, iar
# funcția returnează None. return trimite valoarea înapoi celui care a apelat
# funcția, care o poate salva într-o variabilă, o poate folosi în calcule sau
# o poate da altei funcții (ex. score_headers(security_headers(url))).
# De aceea funcțiile reutilizabile returnează valori, iar afișarea o face
# codul care le apelează.
