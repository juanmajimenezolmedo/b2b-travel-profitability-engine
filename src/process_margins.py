"""
process_margins.py
------------------
Reads the raw bookings CSV, calculates profit margins per booking,
and outputs a clean, enriched dataset ready for database loading.
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────

INPUT_FILE  = Path(__file__).parent.parent / "data" / "bookings_raw.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "bookings_processed.csv"

# ── Processing functions ───────────────────────────────────────────────────────

def calculate_margin(precio_venta: float, coste_neto: float) -> tuple[float, float]:
    """
    Calculates absolute margin and margin percentage.
    Returns (margen_absoluto, margen_pct).
    Raises ValueError if inputs are invalid.
    """
    if precio_venta <= 0:
        raise ValueError(f"Precio_Venta must be > 0, got {precio_venta}")
    if coste_neto < 0:
        raise ValueError(f"Coste_Neto must be >= 0, got {coste_neto}")
    if coste_neto > precio_venta:
        raise ValueError(f"Coste_Neto ({coste_neto}) cannot exceed Precio_Venta ({precio_venta})")

    margen_absoluto = round(precio_venta - coste_neto, 2)
    margen_pct      = round((margen_absoluto / precio_venta) * 100, 2)
    return margen_absoluto, margen_pct


def extract_month(fecha_str: str) -> str:
    """Extracts the month name from a YYYY-MM-DD date string."""
    dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    return dt.strftime("%B %Y")   # e.g. "March 2025"


def extract_quarter(fecha_str: str) -> str:
    """Extracts the quarter from a YYYY-MM-DD date string."""
    dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    quarter = (dt.month - 1) // 3 + 1
    return f"Q{quarter} {dt.year}"


def process_row(row: dict, row_num: int) -> dict | None:
    """
    Processes a single raw booking row.
    Returns enriched row or None if the row has unrecoverable errors.
    """
    try:
        precio_venta = float(row["Precio_Venta"])
        coste_neto   = float(row["Coste_Neto"])
        margen_abs, margen_pct = calculate_margin(precio_venta, coste_neto)

        return {
            "ID_Reserva":         row["ID_Reserva"].strip(),
            "Fecha":              row["Fecha"].strip(),
            "Mes":                extract_month(row["Fecha"].strip()),
            "Trimestre":          extract_quarter(row["Fecha"].strip()),
            "Agencia_B2B":        row["Agencia_B2B"].strip(),
            "Destino":            row["Destino"].strip(),
            "Proveedor_Servicio": row["Proveedor_Servicio"].strip(),
            "Precio_Venta":       precio_venta,
            "Coste_Neto":         coste_neto,
            "Margen_Absoluto":    margen_abs,
            "Margen_Pct":         margen_pct,
            "Estado":             row["Estado"].strip(),
        }

    except (ValueError, KeyError) as e:
        print(f"[process_margins] ⚠️  Skipping row {row_num} — {e}", file=sys.stderr)
        return None


def load_raw(filepath: Path) -> list[dict]:
    """Loads raw CSV file into a list of dicts."""
    if not filepath.exists():
        raise FileNotFoundError(
            f"Input file not found: {filepath}\n"
            "Run generate_data.py first."
        )
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_processed(data: list[dict], filepath: Path) -> None:
    """Saves the processed dataset to a CSV file."""
    if not data:
        raise ValueError("No data to save — all rows were skipped due to errors.")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "ID_Reserva", "Fecha", "Mes", "Trimestre", "Agencia_B2B",
        "Destino", "Proveedor_Servicio", "Precio_Venta", "Coste_Neto",
        "Margen_Absoluto", "Margen_Pct", "Estado",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# ── Summary stats ──────────────────────────────────────────────────────────────

def print_summary(data: list[dict]) -> None:
    """Prints a quick summary of the processed dataset."""
    confirmed = [r for r in data if r["Estado"] == "Confirmada"]
    cancelled = [r for r in data if r["Estado"] == "Cancelada"]

    total_sales  = sum(r["Precio_Venta"]  for r in confirmed)
    total_margin = sum(r["Margen_Absoluto"] for r in confirmed)
    avg_margin   = (total_margin / total_sales * 100) if total_sales else 0

    print(f"\n{'─'*50}")
    print(f"  PROCESSING SUMMARY")
    print(f"{'─'*50}")
    print(f"  Total bookings processed : {len(data)}")
    print(f"  Confirmed                : {len(confirmed)}")
    print(f"  Cancelled                : {len(cancelled)}")
    print(f"  Total sales (confirmed)  : €{total_sales:,.2f}")
    print(f"  Total margin (confirmed) : €{total_margin:,.2f}")
    print(f"  Avg margin %             : {avg_margin:.2f}%")
    print(f"{'─'*50}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"[process_margins] Loading raw data from: {INPUT_FILE}")
    raw_data = load_raw(INPUT_FILE)
    print(f"[process_margins] {len(raw_data)} rows loaded.")

    processed, skipped = [], 0
    for i, row in enumerate(raw_data, start=2):  # start=2 → header is row 1
        result = process_row(row, i)
        if result:
            processed.append(result)
        else:
            skipped += 1

    if skipped:
        print(f"[process_margins] ⚠️  {skipped} rows skipped due to errors.")

    save_processed(processed, OUTPUT_FILE)
    print(f"[process_margins] ✅ Processed data saved to: {OUTPUT_FILE}")
    print_summary(processed)


if __name__ == "__main__":
    main()
