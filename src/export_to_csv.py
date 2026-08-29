"""
export_to_csv.py
----------------
Exports structured data from SQLite to individual CSV files,
ready to be connected from Tableau Public without compatibility issues.

Format: semicolon-separated (;) with comma as decimal separator — European locale
compatible with Tableau Public on Spanish/European macOS systems.

Files generated in /data/tableau/:
  - bookings.csv         — full confirmed bookings detail
  - agency_summary.csv   — sales, margin and avg margin % per agency
  - monthly_trend.csv    — monthly evolution of sales and margin
  - destination.csv      — destination ranking by profitability
  - cancellations.csv    — cancellation rate per agency
"""

import sqlite3
import csv
import locale
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

DB_FILE    = Path(__file__).parent.parent / "data" / "analytics.db"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "tableau"

# ── Queries ────────────────────────────────────────────────────────────────────

EXPORTS = {
    "bookings": """
        SELECT ID_Reserva, Fecha, Mes, Trimestre, Agencia_B2B, Destino,
               Proveedor_Servicio, Precio_Venta, Coste_Neto,
               Margen_Absoluto, Margen_Pct, Estado
        FROM bookings
        WHERE Estado = 'Confirmada'
        ORDER BY Fecha ASC
    """,
    "agency_summary": """
        SELECT Agencia_B2B AS Agencia,
               COUNT(*) AS Num_Reservas,
               ROUND(SUM(Precio_Venta), 2) AS Total_Ventas,
               ROUND(SUM(Margen_Absoluto), 2) AS Total_Margen,
               ROUND(AVG(Margen_Pct), 2) AS Margen_Medio_Pct,
               ROUND(AVG(Precio_Venta), 2) AS Ticket_Medio
        FROM bookings WHERE Estado = 'Confirmada'
        GROUP BY Agencia_B2B ORDER BY Total_Margen DESC
    """,
    "monthly_trend": """
        SELECT Mes, Trimestre,
               COUNT(*) AS Num_Reservas,
               ROUND(SUM(Precio_Venta), 2) AS Total_Ventas,
               ROUND(SUM(Margen_Absoluto), 2) AS Total_Margen,
               ROUND(AVG(Margen_Pct), 2) AS Margen_Medio_Pct
        FROM bookings WHERE Estado = 'Confirmada'
        GROUP BY Mes, Trimestre ORDER BY MIN(Fecha) ASC
    """,
    "destination": """
        SELECT Destino,
               COUNT(*) AS Num_Reservas,
               ROUND(SUM(Precio_Venta), 2) AS Total_Ventas,
               ROUND(SUM(Margen_Absoluto), 2) AS Total_Margen,
               ROUND(AVG(Margen_Pct), 2) AS Margen_Medio_Pct
        FROM bookings WHERE Estado = 'Confirmada'
        GROUP BY Destino ORDER BY Total_Margen DESC
    """,
    "cancellations": """
        SELECT Agencia_B2B AS Agencia,
               COUNT(*) AS Total_Reservas,
               SUM(CASE WHEN Estado='Cancelada' THEN 1 ELSE 0 END) AS Canceladas,
               SUM(CASE WHEN Estado='Confirmada' THEN 1 ELSE 0 END) AS Confirmadas,
               ROUND(SUM(CASE WHEN Estado='Cancelada' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)
                   AS Tasa_Cancelacion_Pct
        FROM bookings
        GROUP BY Agencia_B2B ORDER BY Tasa_Cancelacion_Pct DESC
    """,
}

# ── Export functions ───────────────────────────────────────────────────────────

def format_value(value) -> str:
    """Formats a value for European locale CSV (comma as decimal separator)."""
    if isinstance(value, float):
        return str(value).replace(".", ",")
    return str(value) if value is not None else ""


def export_query_to_csv(cursor: sqlite3.Cursor, query: str, filepath: Path) -> int:
    """Runs a query and writes results to semicolon-separated CSV (European format)."""
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig adds BOM — helps Tableau detect encoding correctly
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        for row in rows:
            writer.writerow([format_value(v) for v in row])

    return len(rows)

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not DB_FILE.exists():
        raise FileNotFoundError(f"Database not found: {DB_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print(f"[export_to_csv] Exporting to: {OUTPUT_DIR}\n")

    for name, query in EXPORTS.items():
        filepath = OUTPUT_DIR / f"{name}.csv"
        count = export_query_to_csv(cursor, query, filepath)
        print(f"[export_to_csv] ✅ {name}.csv — {count} rows")

    conn.close()
    print(f"\n[export_to_csv] ✅ All CSV files exported to: {OUTPUT_DIR}")
    print(f"[export_to_csv]    Connect each file individually from Tableau Public.")


if __name__ == "__main__":
    main()
