"""
load_database.py
----------------
Loads the processed bookings CSV into a SQLite database.
Creates the schema automatically if it doesn't exist.
"""

import csv
import sqlite3
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

INPUT_FILE = Path(__file__).parent.parent / "data" / "bookings_processed.csv"
DB_FILE    = Path(__file__).parent.parent / "data" / "analytics.db"

# ── Schema ─────────────────────────────────────────────────────────────────────

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bookings (
    ID_Reserva          TEXT PRIMARY KEY,
    Fecha               TEXT NOT NULL,
    Mes                 TEXT NOT NULL,
    Trimestre           TEXT NOT NULL,
    Agencia_B2B         TEXT NOT NULL,
    Destino             TEXT NOT NULL,
    Proveedor_Servicio  TEXT NOT NULL,
    Precio_Venta        REAL NOT NULL,
    Coste_Neto          REAL NOT NULL,
    Margen_Absoluto     REAL NOT NULL,
    Margen_Pct          REAL NOT NULL,
    Estado              TEXT NOT NULL
);
"""

INSERT_SQL = """
INSERT OR REPLACE INTO bookings (
    ID_Reserva, Fecha, Mes, Trimestre, Agencia_B2B, Destino,
    Proveedor_Servicio, Precio_Venta, Coste_Neto,
    Margen_Absoluto, Margen_Pct, Estado
) VALUES (
    :ID_Reserva, :Fecha, :Mes, :Trimestre, :Agencia_B2B, :Destino,
    :Proveedor_Servicio, :Precio_Venta, :Coste_Neto,
    :Margen_Absoluto, :Margen_Pct, :Estado
);
"""

# ── Database functions ─────────────────────────────────────────────────────────

def get_connection(db_path: Path) -> sqlite3.Connection:
    """Creates and returns a SQLite connection with row factory enabled."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Creates the bookings table if it doesn't exist."""
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()


def load_csv(filepath: Path) -> list[dict]:
    """Loads processed CSV into a list of dicts with correct types."""
    if not filepath.exists():
        raise FileNotFoundError(
            f"Processed file not found: {filepath}\n"
            "Run process_margins.py first."
        )
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["Precio_Venta"]     = float(row["Precio_Venta"])
            row["Coste_Neto"]       = float(row["Coste_Neto"])
            row["Margen_Absoluto"]  = float(row["Margen_Absoluto"])
            row["Margen_Pct"]       = float(row["Margen_Pct"])
            rows.append(row)
    return rows


def insert_bookings(conn: sqlite3.Connection, rows: list[dict]) -> int:
    """Inserts all booking rows into the database. Returns number of rows inserted."""
    inserted = 0
    errors   = 0
    with conn:
        for row in rows:
            try:
                conn.execute(INSERT_SQL, row)
                inserted += 1
            except sqlite3.Error as e:
                print(f"[load_database] ⚠️  Error inserting {row.get('ID_Reserva', '?')}: {e}",
                      file=sys.stderr)
                errors += 1
    if errors:
        print(f"[load_database] ⚠️  {errors} rows failed to insert.")
    return inserted


def print_verification(conn: sqlite3.Connection) -> None:
    """Runs quick verification queries and prints results."""
    total     = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    confirmed = conn.execute("SELECT COUNT(*) FROM bookings WHERE Estado='Confirmada'").fetchone()[0]
    avg_m     = conn.execute("SELECT AVG(Margen_Pct) FROM bookings WHERE Estado='Confirmada'").fetchone()[0]
    top_agency = conn.execute("""
        SELECT Agencia_B2B, ROUND(SUM(Margen_Absoluto), 2) AS total_margin
        FROM bookings WHERE Estado='Confirmada'
        GROUP BY Agencia_B2B
        ORDER BY total_margin DESC
        LIMIT 1
    """).fetchone()

    print(f"\n{'─'*50}")
    print(f"  DATABASE VERIFICATION")
    print(f"{'─'*50}")
    print(f"  Total rows in DB         : {total}")
    print(f"  Confirmed bookings       : {confirmed}")
    print(f"  Avg margin % (confirmed) : {avg_m:.2f}%")
    if top_agency:
        print(f"  Top agency by margin     : {top_agency[0]} (€{top_agency[1]:,.2f})")
    print(f"{'─'*50}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"[load_database] Connecting to: {DB_FILE}")
    conn = get_connection(DB_FILE)

    print(f"[load_database] Creating schema...")
    create_schema(conn)

    print(f"[load_database] Loading processed CSV from: {INPUT_FILE}")
    rows = load_csv(INPUT_FILE)
    print(f"[load_database] {len(rows)} rows to insert.")

    inserted = insert_bookings(conn, rows)
    print(f"[load_database] ✅ {inserted} rows inserted into database.")

    print_verification(conn)
    conn.close()


if __name__ == "__main__":
    main()
