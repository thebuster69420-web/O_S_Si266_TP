# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Partea 2: Metode și atribute ale obiectelor web (exercițiile 9–20)

import time
import requests

# ---------------------------------------------------------------------------
# Exercițiul 9. Elementele de bază ale răspunsului
# ---------------------------------------------------------------------------
print("=== Exercițiul 9 ===")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", response.status_code)  # atribut (valoare, fără paranteze)
print("ok:", response.ok)                    # atribut (True dacă status < 400)
print("url:", response.url)                  # atribut (URL-ul final)
print("encoding:", response.encoding)        # atribut (codificarea textului)

# ---------------------------------------------------------------------------
# Exercițiul 10. Tratarea erorilor cu o metodă
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 10 ===")
response.raise_for_status()  # metodă: nu face nimic dacă status-ul e 2xx/3xx
print("Pagina principală: nicio eroare")

time.sleep(1)
try:
    gresit = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    gresit.raise_for_status()  # aruncă HTTPError pentru 4xx / 5xx
    print("Pagina există (neașteptat)")
except requests.HTTPError as eroare:
    print("Pagina nu a fost găsită. Detalii:", eroare)

# ---------------------------------------------------------------------------
# Exercițiul 11. Toate antetele
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 11 ===")
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

# ---------------------------------------------------------------------------
# Exercițiul 12. Metode de dicționar
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 12 ===")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# Observație: și cu litere mici obținem aceeași valoare. response.headers nu
# este un dict obișnuit, ci un CaseInsensitiveDict: numele antetelor HTTP nu
# țin cont de majuscule, deci "Content-Type" și "content-type" sunt același
# antet. Într-un dict normal, a doua căutare ar fi returnat "lipsește".

# ---------------------------------------------------------------------------
# Exercițiul 13. Înlănțuirea metodelor de șir
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 13 ===")
aparitii = response.text.lower().count("cyber")
print("Cuvântul 'cyber' apare de", aparitii, "ori")
# Putem înlănțui pentru că .lower() returnează un nou șir (str), iar pe acel
# șir putem apela imediat altă metodă de șir, .count(). Fiecare metodă
# lucrează pe rezultatul celei dinaintea ei, de la stânga la dreapta.

# ---------------------------------------------------------------------------
# Exercițiul 14. Găsirea titlului
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 14 ===")
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>", start)
if html.find("<title>") != -1 and end != -1:
    titlu = html[start:end].strip()
    print("Titlu:", titlu)
else:
    print("Pagina nu are tag <title>")

# ---------------------------------------------------------------------------
# Exercițiul 15. Numărarea liniilor
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 15 ===")
lines = html.splitlines()
print("Număr de linii:", len(lines))
if lines:
    print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))

# ---------------------------------------------------------------------------
# Exercițiul 16. Verificarea HTTPS
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 16 ===")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 17. Urmărirea redirecționărilor
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 17 ===")
r_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
if r_http.history:
    for pas in r_http.history:
        print(pas.status_code, pas.url)
else:
    print("Nicio redirecționare")
print("URL final:", r_http.url)

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 18. HEAD versus GET
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 18 ===")
r_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
r_get = requests.get(BASE_URL, timeout=TIMEOUT)
print("HEAD -> len(content) =", len(r_head.content))
print("GET  -> len(content) =", len(r_get.content))
# HEAD cere serverului doar antetele, fără corp, deci content este gol (0).
# GET cere și corpul (codul HTML al paginii), deci content are mulți octeți.
# HEAD e util când vrem doar să verificăm dacă o pagină există sau ce antete
# are, fără să descărcăm toată pagina.

# ---------------------------------------------------------------------------
# Exercițiul 19. Cookie-uri
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 19 ===")
if len(r_get.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in r_get.cookies:
        print("Nume:", cookie.name, "| secure:", cookie.secure)

time.sleep(1)

# ---------------------------------------------------------------------------
# Exercițiul 20. Sesiuni
# ---------------------------------------------------------------------------
print("\n=== Exercițiul 20 ===")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Secrieru-Octavian"})
r_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
antete_primite = r_echo.json()["headers"]  # httpbin ne trimite înapoi antetele
print("User-Agent văzut de server:", antete_primite.get("User-Agent"))
if antete_primite.get("User-Agent") == "WebLab-Secrieru-Octavian":
    print("Confirmat: antetul personalizat a fost trimis")

# Verificați-vă: de ce response.text nu are paranteze, iar response.json() are?
# response.text este un atribut (de fapt o proprietate): o valoare gata
# pregătită, corpul ca șir de caractere. response.json() este o metodă: o
# acțiune care analizează (parsează) textul ca JSON și construiește din el un
# dicționar/listă Python. Acțiunea poate eșua (dacă textul nu e JSON valid),
# de aceea se apelează explicit, cu paranteze.
