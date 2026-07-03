# 🌿 GreenAlpha — Carbon Intelligence Platform

**AI-powered carbon footprint calculator with sub-500ms response time.**

GreenAlpha turns carbon accounting from a weeks-long analysis exercise into a real-time API call. It combines an IPCC 2021 compliant calculation engine with supply chain optimization and carbon market analytics, served by a FastAPI backend with three web dashboards.

> **The full application lives in [`GREENALPHA/`](GREENALPHA/).** See [`GREENALPHA/README.md`](GREENALPHA/README.md) for complete documentation, API examples, and demo walkthroughs.

## What it does

- **Carbon footprint calculation** — commodity + origin + destination + transport mode in, kg CO₂e out, typically in ~45 ms
- **Supplier recommendations** — ranked suppliers balancing cost against carbon footprint
- **Carbon tax assessment and arbitrage analytics** — price gap analysis across regional carbon credit markets
- **ESG scoring and transport optimization** — dedicated engines in [`GREENALPHA/api/core/`](GREENALPHA/api/core/)
- **Three frontends** — executive dashboard, interactive analytics platform, one-click calculator

## Key numbers

| Metric | Result |
|--------|--------|
| Response time | ~45 ms average (target: under 500 ms) |
| Emission dataset | 18,646+ records covering 1751–2017 |
| Country coverage | 222 countries |
| Methodology | IPCC 2021 |
| Test suite | 54 test functions across 9 modules in [`GREENALPHA/tests/`](GREENALPHA/tests/) |

## Tech stack

FastAPI on Python 3.11, Redis caching, SQLAlchemy with PostgreSQL, Pandas / NumPy / scikit-learn for the data layer, Chart.js / D3.js / Plotly on the frontends, Docker + docker-compose for deployment, GitHub Actions for CI.

## Quick start

```bash
git clone https://github.com/419vive/greenalpha-carbon-intelligence.git
cd greenalpha-carbon-intelligence/GREENALPHA

# Option 1: Docker
docker-compose up --build

# Option 2: local development
pip install -r requirements.txt
cd api && python main.py
```

Then open http://localhost:8000 — interactive API docs at `/docs`.

## Repository layout

```
GREENALPHA/              # The application
├── api/
│   ├── core/            # Carbon engine, arbitrage, ESG scoring, tax assessment,
│   │                    # supplier recommender, transport optimizer, caching
│   ├── main.py          # FastAPI entrypoint
│   └── ...              # Dashboards, demos, benchmark scripts
├── tests/               # pytest suite
├── docker-compose.yml   # One-command launch
├── Dockerfile
└── README.md            # Full project documentation
```

Top-level `src/`, `notebooks/`, and pipeline scripts are scaffolding from an earlier ML experiment and are not part of the GreenAlpha application.
