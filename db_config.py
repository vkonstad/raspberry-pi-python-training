# Shared MySQL connection settings for the database examples.
# Defaults match a local MySQL set up with mysql_setup.sql.
# Override them with environment variables, never put real passwords in the code:
#   Windows (PowerShell):  $env:DB_HOST = "192.168.1.50"
#   Linux / Raspberry Pi:  export DB_HOST=192.168.1.50

import os

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', '3306')),
    'user': os.environ.get('DB_USER', 'labuser'),
    'password': os.environ.get('DB_PASSWORD', 'labpass'),   # local lab-only default
    'database': os.environ.get('DB_NAME', 'EmbeddedLab'),
}
