# B2B-Rentabilitätsanalyse-Engine für Reisebüros

> Analyseengine zur Verarbeitung und Visualisierung der B2B-Rentabilität von Reisebüros innerhalb einer touristischen SaaS-Plattform.

🌐 **Auch verfügbar in:** [🇬🇧 English](README.md) · [🇪🇸 Español](README.es.md)

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Tableau%20Public-blue?logo=tableau)](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)

---

## I. Projektbeschreibung

Simulation eines analytischen Backend-Moduls für eine touristische B2B-SaaS-Plattform. Entwickelt zur Verarbeitung von Buchungsströmen mehrerer Reisebüros, zur Berechnung kommerzieller Margen und Leistungskennzahlen sowie zur Darstellung der Ergebnisse in einem interaktiven Dashboard.

Das Projekt demonstriert zuverlässigen, modularen Code für den produktionsnahen Einsatz — vergleichbar mit den Systemen, die für Plattformen wie **TravelWeb Services** entwickelt wurden.

---

## II. Funktionen

1) **Automatisierte Datenpipeline** — generiert und verarbeitet simulierte Buchungsdatensätze
2) **Margenberechnungs-Engine** — berechnet den Nettogewinn pro Buchung, Agentur und Reiseziel
3) **B2B-Agentur-Ranking** — identifiziert die profitabelsten Agenturen (nicht nur nach Bruttovolumen)
4) **Interaktives Dashboard** — visuelle KPIs aus der Perspektive eines Product Managers oder Commercial Directors
5) **Fehlerbehandlung** — sauberer, stabiler Code für produktionsnahe Zuverlässigkeit

---

## III. Technologie-Stack

| Schicht | Technologie |
|---|---|
| Datengenerierung & -verarbeitung | Python |
| Datenspeicherung | SQLite |
| Visualisierung | *(demnächst verfügbar)* |

---

## IV. Projektstruktur

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

## V. Erste Schritte

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

## VI. Status

**Abgeschlossen** — Pipeline, Datenbank und interaktives Dashboard vollständig betriebsbereit.

🔗 **[Live Dashboard ansehen →](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)**

---

*Entwickelt von [Juanma Jiménez Olmedo](https://github.com/juanmajimenezolmedo)*
