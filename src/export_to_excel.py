"""
export_to_excel.py
------------------
Reads the SQLite database and exports structured sheets to an Excel file
ready to be connected directly from Tableau Public.

Sheets generated:
  1. Bookings       — full detail (all confirmed bookings)
  2. Agency_Summary — total sales, margin and avg margin % per agency
  3. Monthly_Trend  — monthly evolution of sales and margin
  4. Destination    — ranking of destinations by margin
  5. Cancellations  — cancellation rate per agency
"""

import sqlite3
import pandas as pd
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

DB_FILE      = Path(__file__).parent.parent / "data" / "analytics.db"
OUTPUT_FILE  = Path(__file__).parent.parent / "data" / "tableau_export.xlsx"

# ── Database connection ────────────────────────────────────────────────────────

def get_dataframe(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    """Executes a SQL query and returns the result as a DataFrame."""
    return pd.read_sql_query(query, conn)

# ── Queries ────────────────────────────────────────────────────────────────────

QUERY_BOOKINGS = """
    SELECT
        ID_Reserva,
        Fecha,
        Mes,
        Trimestre,
        Agencia_B2B,
        Destino,
        Proveedor_Servicio,
        Precio_Venta,
        Coste_Neto,
        Margen_Absoluto,
        Margen_Pct,
        Estado
    FROM bookings
    WHERE Estado = 'Confirmada'
    ORDER BY Fecha ASC
"""

QUERY_AGENCY_SUMMARY = """
    SELECT
        Agencia_B2B                             AS Agencia,
        COUNT(*)                                AS Num_Reservas,
        ROUND(SUM(Precio_Venta), 2)             AS Total_Ventas,
        ROUND(SUM(Margen_Absoluto), 2)          AS Total_Margen,
        ROUND(AVG(Margen_Pct), 2)               AS Margen_Medio_Pct,
        ROUND(AVG(Precio_Venta), 2)             AS Ticket_Medio
    FROM bookings
    WHERE Estado = 'Confirmada'
    GROUP BY Agencia_B2B
    ORDER BY Total_Margen DESC
"""

QUERY_MONTHLY_TREND = """
    SELECT
        Fecha,
        Mes,
        Trimestre,
        COUNT(*)                                AS Num_Reservas,
        ROUND(SUM(Precio_Venta), 2)             AS Total_Ventas,
        ROUND(SUM(Margen_Absoluto), 2)          AS Total_Margen,
        ROUND(AVG(Margen_Pct), 2)               AS Margen_Medio_Pct
    FROM bookings
    WHERE Estado = 'Confirmada'
    GROUP BY Mes, Trimestre
    ORDER BY MIN(Fecha) ASC
"""

QUERY_DESTINATION = """
    SELECT
        Destino,
        COUNT(*)                                AS Num_Reservas,
        ROUND(SUM(Precio_Venta), 2)             AS Total_Ventas,
        ROUND(SUM(Margen_Absoluto), 2)          AS Total_Margen,
        ROUND(AVG(Margen_Pct), 2)               AS Margen_Medio_Pct
    FROM bookings
    WHERE Estado = 'Confirmada'
    GROUP BY Destino
    ORDER BY Total_Margen DESC
"""

QUERY_CANCELLATIONS = """
    SELECT
        Agencia_B2B                             AS Agencia,
        COUNT(*)                                AS Total_Reservas,
        SUM(CASE WHEN Estado = 'Cancelada' THEN 1 ELSE 0 END)  AS Canceladas,
        SUM(CASE WHEN Estado = 'Confirmada' THEN 1 ELSE 0 END) AS Confirmadas,
        ROUND(
            SUM(CASE WHEN Estado = 'Cancelada' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
        )                                       AS Tasa_Cancelacion_Pct
    FROM bookings
    GROUP BY Agencia_B2B
    ORDER BY Tasa_Cancelacion_Pct DESC
"""

# ── Excel export ───────────────────────────────────────────────────────────────

def export_to_excel(conn: sqlite3.Connection, output_path: Path) -> None:
    """Runs all queries and writes results to a multi-sheet Excel file."""

    sheets = {
        "Bookings":        QUERY_BOOKINGS,
        "Agency_Summary":  QUERY_AGENCY_SUMMARY,
        "Monthly_Trend":   QUERY_MONTHLY_TREND,
        "Destination":     QUERY_DESTINATION,
        "Cancellations":   QUERY_CANCELLATIONS,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, query in sheets.items():
            df = get_dataframe(conn, query)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"[export] ✅ Sheet '{sheet_name}' — {len(df)} rows")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_FILE}\n"
            "Run generate_data.py → process_margins.py → load_database.py first."
        )

    print(f"[export_to_excel] Connecting to: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)

    print(f"[export_to_excel] Exporting to: {OUTPUT_FILE}\n")
    export_to_excel(conn, OUTPUT_FILE)
    conn.close()

    size_kb = round(OUTPUT_FILE.stat().st_size / 1024, 1)
    print(f"\n[export_to_excel] ✅ Export complete — {OUTPUT_FILE.name} ({size_kb} KB)")
    print(f"[export_to_excel]    Open this file in Tableau Public to connect your data.")


if __name__ == "__main__":
    main()
