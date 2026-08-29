# B2B-Rentabilitätsanalyse-Engine für Reisebüros

> Analyseengine zur Verarbeitung und Visualisierung der B2B-Rentabilität von Reisebüros innerhalb einer touristischen SaaS-Plattform.

🌐 **Auch verfügbar in:** [🇬🇧 English](README.md) · [🇪🇸 Español](README.es.md)

---

## Projektbeschreibung

Simulation eines analytischen Backend-Moduls für eine touristische B2B-SaaS-Plattform. Entwickelt zur Verarbeitung von Buchungsströmen mehrerer Reisebüros, zur Berechnung kommerzieller Margen und Leistungskennzahlen sowie zur Darstellung der Ergebnisse in einem interaktiven Dashboard.

Das Projekt demonstriert zuverlässigen, modularen Code für den produktionsnahen Einsatz — vergleichbar mit den Systemen, die für Plattformen wie **TravelWeb Services** entwickelt wurden.

---

## Funktionen

- 🔄 **Automatisierte Datenpipeline** — generiert und verarbeitet simulierte Buchungsdatensätze
- 📊 **Margenberechnungs-Engine** — berechnet den Nettogewinn pro Buchung, Agentur und Reiseziel
- 🏆 **B2B-Agentur-Ranking** — identifiziert die profitabelsten Agenturen (nicht nur nach Bruttovolumen)
- 📈 **Interaktives Dashboard** — visuelle KPIs aus der Perspektive eines Product Managers oder Commercial Directors
- 🛡️ **Fehlerbehandlung** — sauberer, stabiler Code für produktionsnahe Zuverlässigkeit

---

## Technologie-Stack

| Schicht | Technologie |
|---|---|
| Datengenerierung & -verarbeitung | Python |
| Datenspeicherung | SQLite |
| Visualisierung | *(demnächst verfügbar)* |

---

## Projektstruktur

```
b2b-travel-profitability-engine/
│
├── data/               # Generierte Datensätze (simulierte Buchungen)
├── src/                # Kernverarbeitungsskripte
│   ├── generate_data.py
│   ├── process_margins.py
│   └── load_database.py
├── dashboard/          # Interaktive Visualisierung
├── requirements.txt
└── README.md
```

---

## Erste Schritte

```bash
# Repository klonen
git clone git@github.com:juanmajimenezolmedo/b2b-travel-profitability-engine.git
cd b2b-travel-profitability-engine

# Abhängigkeiten installieren
pip install -r requirements.txt

# Daten generieren und Pipeline ausführen
python src/generate_data.py
python src/process_margins.py
python src/load_database.py
```

---

## Status

🚧 **In aktiver Entwicklung** — initiale Pipeline und Dashboard folgen in Kürze.

---

*Entwickelt von [Juanma Jiménez Olmedo](https://github.com/juanmajimenezolmedo)*
