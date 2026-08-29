# B2B Travel Profitability Engine

> Analytical engine to process and visualize B2B travel agency profitability within a SaaS tourism platform.

🌐 **Also available in:** [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md)

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Tableau%20Public-blue?logo=tableau)](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)

---

## I. Overview

Simulation of a backend analytics module for a B2B tourism SaaS platform. Designed to process booking flows from multiple travel agencies, calculate commercial margins and performance indicators, and display results through an interactive dashboard.

Built to demonstrate reliable, modular code capable of running in real daily operations — mirroring the kind of systems developed for platforms like **TravelWeb Services**.

---

## II. Features

1) **Automated data pipeline** — generates and processes simulated booking datasets
2)  **Margin calculation engine** — computes net profit per booking, agency and destination
3) **B2B agency ranking** — identifies top performers by profitability (not just gross volume)
4) **Interactive dashboard** — visual KPIs for a Product Manager or Commercial Director perspective
5) **Error handling** — clean, stable code designed for production-like reliability

---

## III. Tech Stack

| Layer | Technology |
|---|---|
| Data generation & processing | Python |
| Storage | SQLite |
| Visualization | *(coming soon)* |

---

## IV. Project Structure

```
b2b-travel-profitability-engine/
│
├── data/               # Generated datasets (mock bookings)
├── src/                # Core processing scripts
│   ├── generate_data.py
│   ├── process_margins.py
│   └── load_database.py
├── dashboard/          # Interactive visualization
├── requirements.txt
└── README.md
```

---

## V. Getting Started

```bash
# Clone the repository
git clone git@github.com:juanmajimenezolmedo/b2b-travel-profitability-engine.git
cd b2b-travel-profitability-engine

# Install dependencies
pip install -r requirements.txt

# Generate mock data and run the pipeline
python src/generate_data.py
python src/process_margins.py
python src/load_database.py
```

---

## VI. Status

**Completed** — pipeline, database and interactive dashboard fully operational.

🔗 **[View Live Dashboard →](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)**

---

*Developed by [Juanma Jiménez Olmedo](https://github.com/juanmajimenezolmedo)*
