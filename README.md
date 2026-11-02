Some entry-level examples towards understanding python, with raspberry pi as a target.

Static IP settings on raspberry pi included (`static on pi.txt`).

New to Linux? See the one-page `Linux cheat sheet.md` (SSH, files, permissions, packages, systemd, network).
When you are ready, `Linux lab.md` is a 30 minute hands-on exercise (apt, htop, stress-ng) done entirely in the console.

## Setup

```
python -m venv .venv
.venv\Scripts\activate          (Windows)   |   source .venv/bin/activate   (Linux / Raspberry Pi)
pip install -r requirements.txt
```

`Example 01` explains what this does and checks that your environment is set up correctly.

## Order of the simple (non-hardware) examples

| # | File | Topic |
|---|------|-------|
| 00 | `Example 00 - Hello.py` | Python works on my machine |
| 01 | `Example 01 - Virtual Environment.py` | venv, pip, requirements.txt |
| 02 | `Example 02 - Basic Input.py` | input, loops, exceptions |
| 03 | `Example 03 - Arguments.py` | command-line arguments |
| 04 | `Example 04 - Lists and Dictionaries.py` | the core data structures |
| 05 | `Example 05 - JSON and CSV.py` | saving and loading data |
| 06 | `Example 06 - Simple Tables.py` | reading tables with pandas, plots |
| 07 | `Example 07 - Simple timing.py` | functions, measuring time |
| 08 | `Example 08 - Simple Threading.py` | threads |
| 09 | `Example 09 - Pandas.py` | vectorized vs row-by-row processing |
| 10 | `Example 10 - MySQL.py` | databases (needs the MariaDB container, below) |
| 11 | `Example 11a/11b - Socket ...` | TCP client / server |
| 12 | `Example 12 - CPU Temperature to SQLite.py` | SQLite, runs on the Pi only; used by the cron / systemd tasks of the Linux lab |

## MariaDB (in Docker) for example 10 and the streamlit dashboard

The database runs in a ready-made container, so nothing is installed on your machine except Docker
(Docker Desktop on Windows/macOS, or `docker.io` / Docker Engine on Linux).

Start it, from the folder of this repository:

```
docker compose up -d
```

The first start downloads the image and creates the database `EmbeddedLab` with the user `labuser`
(see `docker-compose.yml`). Check that it is running and healthy:

```
docker compose ps
```

Useful commands:

```
docker compose logs mariadb                                        # what the database says
docker exec -it embedded-lab-db mariadb -ulabuser -plabpass EmbeddedLab   # SQL console, try: SHOW TABLES; SELECT * FROM Sensor;
docker compose down                                                # stop it (your data is kept)
docker compose down -v                                             # stop it and delete the data
```

Connection settings live in `db_config.py`, the defaults match the container
(`localhost`, port `3306`, `labuser`, `labpass`, `EmbeddedLab`). Override them with the environment
variables `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, e.g. to connect to a database on another machine.
The passwords in `docker-compose.yml` are for this lab only. Do not commit real passwords to the repository.
