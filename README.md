Some entry-level examples towards understanding python, with raspberry pi as a target.

Static IP settings on raspberry pi included (`static on pi.txt`).

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
| 10 | `Example 10 - MySQL.py` | databases (needs a local MySQL, below) |
| 11 | `Example 11a/11b - Socket ...` | TCP client / server |

## MySQL for example 10 and the streamlit dashboard

Install MySQL (or MariaDB) on your machine, then create the lab database and user:

```
mysql -u root -p < mysql_setup.sql
```

Connection settings live in `db_config.py` and can be overridden with the environment
variables `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
Do not commit real passwords to the repository.
