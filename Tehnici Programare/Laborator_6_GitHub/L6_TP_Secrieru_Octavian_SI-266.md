# Laboratorul 6. GitHub, pas cu pas

Disciplina: Tehnici de programare  
A efectuat: st. gr. SI-266 Secrieru Octavian  
A verificat: asistent universitar Cristian Gonceari

## Date

| | |
|---|---|
| Nume complet | Secrieru Octavian |
| Grupa | SI-266 |
| Username GitHub | thebuster69420-web |
| Depozitul exercitiu-git | https://github.com/thebuster69420-web/exercitiu-git |
| Depozitul exercitiu-2 | https://github.com/thebuster69420-web/exercitiu-2 |

## Ce am exersat la fiecare pas

- **A1. Contul GitHub.** Am intrat în contul meu GitHub și mi-am notat numele de utilizator, care apare în toate linkurile depozitelor mele.
- **A2. Git pe calculator.** Am verificat cu `git --version` că git este instalat și m-am prezentat cu `git config --global` (nume, e-mail, ramura implicită `main` și `pull.rebase false`).
- **A3. Primul depozit, creat pe GitHub.** Am creat pe GitHub depozitul public `exercitiu-git`, cu fișierul README.md bifat de la creare.
- **A4. git clone.** Am adus depozitul pe calculator cu `git clone` și am dat toate comenzile următoare din folderul `exercitiu-git`.
- **A5. status, add, commit.** Am creat și rulat `salut.py`, am văzut cu `git status` cum fișierul trece din „untracked” în „to be committed” după `git add` și l-am salvat în istorie cu `git commit`.
- **A6. git push.** Am trimis commit-ul pe GitHub cu `git push`, autentificându-mă prin browser la prima trimitere.
- **A7. git pull.** Am adăugat un rând în README.md direct pe GitHub și am adus schimbarea pe calculator cu `git pull`.
- **A8. .gitignore.** Am creat mediul virtual `.venv` și fișierul `.gitignore` cu `.venv/` și `__pycache__/`, ca acestea să nu ajungă pe GitHub.
- **A9. log și diff.** Am citit istoria cu `git log --oneline`, am văzut cu `git diff` un rând nou din `salut.py`, apoi l-am anulat cu `git restore`.
- **A10. Al doilea depozit, pornit de pe calculator.** Am pornit `exercitiu-2` local cu `git init`, l-am legat de GitHub cu `git remote add origin` și l-am trimis cu `git push -u origin main`.

## Verificarea finală (A11)

- `exercitiu-git` este Public și conține README.md, salut.py și .gitignore, cu 4 commit-uri: Initial commit, Adaug salut.py, Update README.md, Ignor mediul virtual.
- `exercitiu-2` este Public și conține README.md, trimis pe GitHub cu `git push -u origin main`.

Sursă: fișa Laboratorului 6, „GitHub, pas cu pas”.
