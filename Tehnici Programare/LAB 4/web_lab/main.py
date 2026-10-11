# Laborator: funcții, metode și importuri pe web
# Student: Secrieru Octavian, SI-266
#
# main.py — programul care importă modulul propriu webtools (Partea 5).
# Rulare:  python main.py https://cybercor.org

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import argparse
import csv
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# Exercițiul 44. Importul întregului modul
# ---------------------------------------------------------------------------
import webtools

# ---------------------------------------------------------------------------
# Exercițiul 45. Importarea anumitor nume
# ---------------------------------------------------------------------------
from webtools import get_title, security_headers
# Dacă main.py ar avea și o funcție proprie numită get_title, definită DUPĂ
# acest import, ea ar înlocui (ar „acoperi”) funcția importată: numele
# get_title ar indica spre funcția din main.py, iar cea din webtools n-ar mai
# fi accesibilă prin numele scurt. Contează care definiție e ultima. Dacă
# funcția proprie ar fi definită ÎNAINTE de import, importul ar înlocui-o pe
# ea. Varianta webtools.get_title(...) rămâne mereu neambiguă, de aceea
# „import webtools” e mai sigur când există riscul de nume identice.

# ---------------------------------------------------------------------------
# Exercițiul 47. Constante de modul
# ---------------------------------------------------------------------------
from webtools import DEFAULT_HEADERS

# ---------------------------------------------------------------------------
# Exercițiul 46. Blocul main — explicație
# ---------------------------------------------------------------------------
# În webtools.py, autotestul stă sub  if __name__ == "__main__":
# Python setează variabila __name__ a fiecărui fișier:
#   - când rulăm direct  python webtools.py  -> __name__ == "__main__",
#     deci condiția e adevărată și autotestul rulează;
#   - când webtools e importat din main.py  -> __name__ == "webtools",
#     deci condiția e falsă și autotestul NU rulează.
# Astfel modulul se poate testa singur, dar nu afișează nimic în plus
# atunci când e folosit de alt program.


def save_csv(results: dict[str, int], filename: str = "report.csv") -> None:
    """Exercițiul 49: salvează rezultatul lui check_paths() în report.csv.

    Coloanele sunt path, status și checked_at (ora verificării, format ISO).
    """
    cale = webtools.FOLDER / filename
    checked_at = datetime.now().isoformat()
    with open(cale, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, checked_at])
    print("Salvat în", cale.name)


def main() -> None:
    """Citește URL-ul din linia de comandă și rulează exercițiile 44–50."""
    # -----------------------------------------------------------------------
    # Exercițiul 48. Argumente din linia de comandă
    # -----------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Raport despre un site web")
    parser.add_argument(
        "url",
        nargs="?",
        default=BASE_URL,
        help="adresa site-ului (implicit https://cybercor.org)",
    )
    args = parser.parse_args()
    url = args.url  # de aici folosim url, nu BASE_URL

    print("=== Exercițiul 44 ===")
    print("Titlu:", webtools.get_title(webtools.fetch(url).text))
    time.sleep(1)

    print("\n=== Exercițiul 45 ===")
    print("Titlu (nume importat direct):", get_title(webtools.fetch(url).text))
    time.sleep(1)
    print("Antete de securitate:", security_headers(url))
    time.sleep(1)

    print("\n=== Exercițiul 47 ===")
    print("DEFAULT_HEADERS:", DEFAULT_HEADERS)

    print("\n=== Exercițiul 49 ===")
    rezultate = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    print(rezultate)
    save_csv(rezultate)
    time.sleep(1)

    print("\n=== Exercițiul 50 ===")
    webtools.site_report(url)


if __name__ == "__main__":
    main()
