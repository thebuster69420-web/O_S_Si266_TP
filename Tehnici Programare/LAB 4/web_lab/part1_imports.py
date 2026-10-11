# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Partea 1: Importuri (exercițiile 1–8)

import time

# ---------------------------------------------------------------------------
# Exercițiul 1. Primul import
# ---------------------------------------------------------------------------
print("=== Exercițiul 1 ===")
import requests
print("Versiunea requests:", requests.__version__)

import urllib.request
print("urllib.request importat:", urllib.request.__name__)

# De ce requests a avut nevoie de pip install, iar urllib nu?
# urllib face parte din biblioteca standard Python: vine instalat împreună
# cu Python. requests este o bibliotecă externă (scrisă de altă echipă),
# publicată pe PyPI, de aceea trebuie descărcată separat cu pip install.

# ---------------------------------------------------------------------------
# Exercițiul 2. Două stiluri de import
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 2 ===")
# Stilul 1: import requests -> scriem numele modulului în fața funcției
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cu import requests:", response.status_code)

time.sleep(1)

# Stilul 2: from requests import get -> folosim direct numele funcției
from requests import get
response = get(BASE_URL, timeout=TIMEOUT)
print("Cu from requests import get:", response.status_code)

# Avantajul lui "import requests": se vede clar de unde vine funcția
# (requests.get), iar numele nu intră în conflict cu alte funcții "get".
# Avantajul lui "from requests import get": codul e mai scurt, scriem doar
# get(...), util când folosim funcția de multe ori.

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 3. Alias-uri
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 3 ===")
import requests as rq
response = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cu alias rq:", response.status_code)

# Un alias face codul mai ușor de citit când e o convenție cunoscută de toți
# (de ex. import numpy as np, import pandas as pd) sau când numele modulului
# e foarte lung. Îl face mai greu de citit când alias-ul e inventat și
# neclar (ex. rq în loc de requests): cine citește codul nu știe imediat
# ce modul este.

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 4. Doar biblioteca standard
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 4 ===")
with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as raspuns:
    print("Status:", raspuns.status)
    corp = raspuns.read().decode("utf-8", errors="replace")  # bytes -> str
    print("Primele 200 de caractere:")
    print(corp[:200])

# ---------------------------------------------------------------------------
# Exercițiul 5. Priviți în interiorul unui modul
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 5 ===")
print(dir(requests))

# Trei nume alese din rezultat:
#   requests.get      -> funcție (o apelăm: requests.get(url))
#   requests.Session  -> clasă (din ea creăm obiecte: requests.Session())
#   requests.adapters -> modul (un fișier .py din interiorul pachetului)
print(type(requests.get), type(requests.Session), type(requests.adapters))

# ---------------------------------------------------------------------------
# Exercițiul 6. Citiți documentația
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 6 ===")
help(requests.get)
# În documentație, parametrul pentru timpul maxim de așteptare este
# "timeout" (apare în **kwargs, descris la requests.request).
time.sleep(1)
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cerere cu timeout =", TIMEOUT, "secunde ->", response.status_code)

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 7. Cronometrarea unei cereri
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 7 ===")
start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
durata = time.perf_counter() - start
print(f"Măsurat cu perf_counter: {durata:.3f} s")
print(f"response.elapsed:        {response.elapsed.total_seconds():.3f} s")
# perf_counter() măsoară tot timpul cererii, inclusiv descărcarea corpului.
# response.elapsed măsoară doar timpul de la trimiterea cererii până la
# sosirea antetelor răspunsului, de aceea de obicei e puțin mai mic.

# ---------------------------------------------------------------------------
# Exercițiul 8. Când un import eșuează
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 8 ===")
try:
    import bs4
    print("bs4 este instalat, versiunea", bs4.__version__)
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")

# Verificați-vă: modul, pachet, bibliotecă
# - Modul: un singur fișier .py (ex. time, json).
# - Pachet: un director cu mai multe module, care se importă împreună
#   (ex. urllib, care conține urllib.request, urllib.parse).
# - Bibliotecă: o colecție de module/pachete care rezolvă o problemă,
#   distribuită ca un tot (ex. requests, beautifulsoup4). Termenul e mai
#   general; o bibliotecă poate fi un singur modul sau mai multe pachete.
