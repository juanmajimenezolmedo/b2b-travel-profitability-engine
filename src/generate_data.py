"""
generate_data.py
----------------
Generates a simulated dataset of B2B travel agency bookings.
Produces a CSV file in the /data directory ready for processing.
"""

import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

TOTAL_BOOKINGS = 800
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "bookings_raw.csv"

# ── Master data (realistic B2B tourism sector) ────────────────────────────────

AGENCIES_B2B = [
    "Viajes El Corte Inglés",
    "Halcón Viajes",
    "Barceló Viajes",
    "Nautalia",
    "B The Travel Brand",
    "Globalia Corporate Travel",
    "Avoris Travel Group",
    "CWT Spain",
    "American Express GBT",
    "TravelPerk",
]

DESTINATIONS = [
    "Cancún, México",
    "Bali, Indonesia",
    "Dubai, EAU",
    "Nueva York, EEUU",
    "París, Francia",
    "Roma, Italia",
    "Bangkok, Tailandia",
    "Lisboa, Portugal",
    "Marrakech, Marruecos",
    "Ámsterdam, Países Bajos",
    "Tokio, Japón",
    "Buenos Aires, Argentina",
    "Phuket, Tailandia",
    "Atenas, Grecia",
    "Berlín, Alemania",
]

SERVICE_PROVIDERS = [
    "Amadeus Hotels",
    "Sabre Hospitality",
    "Hotelbeds",
    "W2M (Webjetlatam)",
    "TUI Musement",
    "Kuoni DMC",
    "Iberia (vuelos)",
    "Ryanair (vuelos)",
    "Avis (coches)",
    "MSC Cruceros",
]

STATUSES = ["Confirmada", "Confirmada", "Confirmada", "Cancelada"]  # 75% confirmed

# ── Pricing logic per destination (min_sale, max_sale, margin_range) ──────────

PRICING_CONFIG = {
    "Cancún, México":           (1200, 3500, (0.12, 0.28)),
    "Bali, Indonesia":          (1500, 4200, (0.10, 0.25)),
    "Dubai, EAU":               (1800, 5000, (0.15, 0.30)),
    "Nueva York, EEUU":         (1400, 4000, (0.12, 0.22)),
    "París, Francia":           (800,  2500, (0.10, 0.20)),
    "Roma, Italia":             (700,  2200, (0.10, 0.20)),
    "Bangkok, Tailandia":       (1100, 3200, (0.12, 0.26)),
    "Lisboa, Portugal":         (500,  1600, (0.08, 0.18)),
    "Marrakech, Marruecos":     (600,  1800, (0.12, 0.24)),
    "Ámsterdam, Países Bajos":  (700,  2000, (0.10, 0.20)),
    "Tokio, Japón":             (1800, 5500, (0.14, 0.28)),
    "Buenos Aires, Argentina":  (1300, 3800, (0.12, 0.24)),
    "Phuket, Tailandia":        (1200, 3400, (0.12, 0.26)),
    "Atenas, Grecia":           (700,  2200, (0.10, 0.22)),
    "Berlín, Alemania":         (600,  1900, (0.10, 0.20)),
}

# ── Helper functions ───────────────────────────────────────────────────────────

def random_date(start: datetime, end: datetime) -> datetime:
    """Returns a random date between start and end."""
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_booking() -> dict:
    """Generates a single booking record with realistic pricing."""
    destination = random.choice(DESTINATIONS)
    min_sale, max_sale, (min_margin, max_margin) = PRICING_CONFIG[destination]

    precio_venta = round(random.uniform(min_sale, max_sale), 2)
    margin_pct   = round(random.uniform(min_margin, max_margin), 4)
    coste_neto   = round(precio_venta * (1 - margin_pct), 2)
    status       = random.choice(STATUSES)

    return {
        "ID_Reserva":          str(uuid.uuid4())[:8].upper(),
        "Fecha":               random_date(START_DATE, END_DATE).strftime("%Y-%m-%d"),
        "Agencia_B2B":         random.choice(AGENCIES_B2B),
        "Destino":             destination,
        "Proveedor_Servicio":  random.choice(SERVICE_PROVIDERS),
        "Precio_Venta":        precio_venta,
        "Coste_Neto":          coste_neto,
        "Estado":              status,
    }


def generate_dataset(n: int = TOTAL_BOOKINGS) -> list[dict]:
    """Generates a full dataset of n bookings."""
    return [generate_booking() for _ in range(n)]


def save_to_csv(data: list[dict], filepath: Path) -> None:
    """Saves the dataset to a CSV file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["ID_Reserva", "Fecha", "Agencia_B2B", "Destino",
                  "Proveedor_Servicio", "Precio_Venta", "Coste_Neto", "Estado"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"[generate_data] Generating {TOTAL_BOOKINGS} bookings...")
    dataset = generate_dataset(TOTAL_BOOKINGS)
    save_to_csv(dataset, OUTPUT_FILE)
    print(f"[generate_data] ✅ Dataset saved to: {OUTPUT_FILE}")
    print(f"[generate_data]    Total records: {len(dataset)}")
    confirmed = sum(1 for b in dataset if b["Estado"] == "Confirmada")
    cancelled = sum(1 for b in dataset if b["Estado"] == "Cancelada")
    print(f"[generate_data]    Confirmed: {confirmed} | Cancelled: {cancelled}")


if __name__ == "__main__":
    main()
