# Motor de Análisis de Rentabilidad B2B para Agencias de Viajes

> Motor analítico para procesar y visualizar la rentabilidad de agencias de viajes B2B dentro de una plataforma SaaS turística.

🌐 **También disponible en:** [🇬🇧 English](README.md) · [🇩🇪 Deutsch](README.de.md)

[![Dashboard en Vivo](https://img.shields.io/badge/Dashboard%20en%20Vivo-Tableau%20Public-blue?logo=tableau)](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)

---

## Descripción

Simulación de un módulo analítico backend para una plataforma SaaS turística B2B. Diseñado para procesar el flujo de reservas de múltiples agencias de viajes, calcular márgenes comerciales e indicadores de rendimiento, y mostrar los resultados a través de un panel de control interactivo.

Desarrollado para demostrar un código modular y fiable, apto para operativas diarias reales — del mismo tipo que los sistemas construidos para plataformas como **TravelWeb Services**.

---

## Funcionalidades

- 🔄 **Pipeline de datos automatizado** — genera y procesa datasets simulados de reservas
- 📊 **Motor de cálculo de márgenes** — calcula el beneficio neto por reserva, agencia y destino
- 🏆 **Ranking de agencias B2B** — identifica a los mejores por rentabilidad (no solo por volumen bruto)
- 📈 **Dashboard interactivo** — KPIs visuales desde la perspectiva de un Product Manager o Director Comercial
- 🛡️ **Manejo de errores** — código limpio y estable, diseñado para fiabilidad en producción

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Generación y procesamiento de datos | Python |
| Almacenamiento | SQLite |
| Visualización | *(próximamente)* |

---

## Estructura del Proyecto

```
b2b-travel-profitability-engine/
│
├── data/               # Datasets generados (reservas simuladas)
├── src/                # Scripts de procesamiento
│   ├── generate_data.py
│   ├── process_margins.py
│   └── load_database.py
├── dashboard/          # Visualización interactiva
├── requirements.txt
└── README.md
```

---

## Cómo ejecutarlo

```bash
# Clonar el repositorio
git clone git@github.com:juanmajimenezolmedo/b2b-travel-profitability-engine.git
cd b2b-travel-profitability-engine

# Instalar dependencias
pip install -r requirements.txt

# Generar datos y ejecutar el pipeline
python src/generate_data.py
python src/process_margins.py
python src/load_database.py
```

---

## Estado

✅ **Completado** — pipeline, base de datos y dashboard interactivo totalmente operativos.

🔗 **[Ver Dashboard en Vivo →](https://public.tableau.com/app/profile/juanma.jim.nez/viz/B2BTravelProfitabilityDashboard2025/Dashboard1)**

---

*Desarrollado por [Juanma Jiménez Olmedo](https://github.com/juanmajimenezolmedo)*
