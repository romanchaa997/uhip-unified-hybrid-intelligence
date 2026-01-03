# UHIP Parallel Development Roadmap
## Two Independent Product Tracks: Nuclear Dashboard + Microgrid Simulator

### Overview
This document defines how to organize parallel development of two related but independently deployable products:
- **Track 1**: Public Nuclear Power Plant (NPP) Dashboard with real data integration
- **Track 2**: Microgrid Simulation System with NPP/SMR + Renewable Energy optimization

Both tracks share a common core library but develop along separate feature paths, with integration points defined by API contracts.

---

## Track 1: Nuclear Power Plant Dashboard

### Purpose
Public-facing dashboard showing real-time and historical data from Ukrainian nuclear power plants, emphasizing:
- Current operational state of reactor units
- Power generation metrics and grid support
- CO₂ avoidance calculations
- Public transparency and energy planning support

### Phase 1 (Sprint 1): Foundation
**Deliverables:**
- Data ingestion pipeline for one source (UA-energy API)
- Normalized data model (Plant, Unit, TimeSeries)
- Basic REST API: `/plants`, `/units/status`
- Frontend: Map view of NPP locations + basic unit status cards
- OpenAPI documentation with Python/JavaScript examples

**Team Focus**: Data engineering + Full-stack web dev
**Effort**: 2 weeks

### Phase 2 (Sprint 2): Core Features
**Deliverables:**
- Multi-source data ingestion (Міненерго, Енергоатом)
- CO₂ equivalent calculations and avoidance metrics
- Time-series power generation charts (24h, 7d, 30d views)
- Unit maneuvering/ramping data visualization
- Live demo deployment

**Team Focus**: Backend optimization + Frontend UX
**Effort**: 2 weeks

### Phase 3 (Sprint 3): Stability & Ecosystem
**Deliverables:**
- API v1.0 stabilization and complete OpenAPI spec
- Extended time-series backend (Postgres/TimescaleDB)
- Public data export (CSV, JSON)
- Documentation for external developers
- Set foundation for Microgrid simulator integration

**Team Focus**: DevOps + Documentation
**Effort**: 1.5 weeks

### Technology Stack
```
Backend: Python FastAPI + Postgres
Frontend: React + Recharts (power graphs) + Mapbox (location)
Data: Pandas + SQLAlchemy ORM
Deploy: Docker + GitHub Actions
```

### Key API Endpoints
```
GET  /plants               # All NPP plants
GET  /plants/{id}         # Single plant details
GET  /units?plant_id=X    # Units filtered by plant
GET  /units/{id}/status   # Current unit state
GET  /timeseries/{unit_id} # Power generation time-series
GET  /emissions/avoided   # CO₂ metrics
```

---

## Track 2: Microgrid Optimization Simulator

### Purpose
Powerful simulation & optimization tool for exploring microgrid configurations with:
- NPP/SMR as stable baseload source
- Variable renewable energy (solar/wind profiles)
- Energy storage systems (batteries, thermal)
- Multiple load profiles (city, industrial, data center)
- Economic and environmental optimization

### Phase 1 (Sprint 1): Prototype
**Deliverables:**
- Lightweight microgrid model (system.py) with configurable units
- Static load/renewable profiles (hourly Ukraine climate data)
- Simple hourly balance simulation (no optimization yet)
- Web form to configure scenario (SMR capacity, % renewables, battery size)
- Basic generation/consumption/storage level charts

**Team Focus**: Energy modeling + Python backend
**Effort**: 2 weeks

### Phase 2 (Sprint 2): Optimization Core
**Deliverables:**
- MILP formulation (Pyomo + OR-Tools solver)
- Scenario "City 200k + SMR" fully optimized
- Cost function (fuel, import penalty, CO₂ penalty)
- Unmet load and curtailed energy metrics
- Optimization convergence plots + sensitivity analysis

**Team Focus**: Operations Research + Algorithms
**Effort**: 2.5 weeks

### Phase 3 (Sprint 3): Presets & Reporting
**Deliverables:**
- 3+ preset scenarios ("City 200k", "Industrial park", "Decarbonization zone")
- Report generation (PDF with charts, optimization summary)
- Lightweight RL agent for demand forecasting (optional)
- Scenario comparison dashboard
- Export results (CSV, JSON) for further analysis

**Team Focus**: Scenario design + Report automation
**Effort**: 2 weeks

### Technology Stack
```
Core: Python (numpy, scipy, pandas)
Optimization: Pyomo + COIN-OR CBC solver (or OR-Tools)
Web Frontend: React + Plotly (optimization results)
Forecasting (optional): TensorFlow/PyTorch LSTM
Deploy: Docker + Celery for async optimization
```

### Key Simulation Entities
```python
class SMRUnit:
  capacity_mw: float
  min_load_pct: float
  ramp_rate_mw_per_h: float

class RenewableProfile:
  resource_type: 'solar' | 'wind'
  hourly_capacity_factor: [float]  # 0-1 for each hour

class Battery:
  capacity_mwh: float
  charge_rate_mw: float
  efficiency: float

class LoadProfile:
  profile_type: 'city' | 'industrial' | 'datacenter'
  hourly_demand_mw: [float]
```

---

## Shared Core Library (`core/`)

### Purpose
Single source of truth for data models, ensuring Dashboard and Simulator work with consistent entities.

### Structure
```
core/
├── models/
│   ├── plant.py          # Plant, Unit, Reactor entities
│   ├── timeseries.py     # TimeSeries, Measurement, MetricType
│   ├── emission.py       # CO₂ equivalents, avoided emissions
│   └── profiles.py       # LoadProfile, RenewableProfile for sim
├── api_schema.py         # Pydantic models for API I/O
├── db_models.py          # SQLAlchemy ORM for Postgres
├── config.py             # Shared configuration (data sources, DB conn)
├── utils/
│   ├── data_normalization.py
│   ├── emissions_calculator.py
│   └── time_utils.py
└── __init__.py
```

### Usage
```python
# Dashboard backend uses:
from core.models import Plant, Unit, TimeSeries
from core.api_schema import PlantResponse, UnitStatusResponse

# Microgrid simulator uses:
from core.models import LoadProfile, RenewableProfile
from core.utils import emissions_calculator
```

---

## Parallel Development Organization

### Repository Structure
```
uhip-unified-hybrid-intelligence/
├── core/                        # Shared library (no external deps beyond numpy, sqlalchemy)
│   ├── models/
│   ├── api_schema.py
│   └── utils/
├── services/
│   ├── dashboard-api/          # Track 1: Backend REST API
│   │   ├── main.py             # FastAPI app
│   │   ├── routers/
│   │   ├── db/                 # Postgres integration
│   │   └── data_ingestion/     # UA-energy, Міненерго connectors
│   ├── dashboard-ui/            # Track 1: React frontend
│   │   ├── src/pages/
│   │   ├── src/components/
│   │   └── src/api/            # Client SDK (auto-generated from OpenAPI?)
│   └── microgrid-sim/           # Track 2: Simulation engine
│       ├── simulator.py         # Core model + hourly balance
│       ├── optimizer.py         # MILP/LP solver
│       ├── web_api.py           # FastAPI for web UI
│       ├── scenarios/           # Preset configs
│       └── forecast/            # Optional RL/LSTM models
├── docker-compose.yml
├── requirements.txt             # Shared + all service dependencies
├── PROJECT_ROADMAP_PARALLEL_TRACKS.md
└── ...
```

### Team Organization
**Track 1 Team (Dashboard)**
- 1-2 Backend engineers (data pipeline, API)
- 1-2 Frontend engineers (React, visualization)
- 1 DevOps/Data engineer (DB setup, data validation)

**Track 2 Team (Simulator)**
- 1-2 Energy modeling engineers (Python, simulation)
- 1 Optimization specialist (MILP, solver tuning)
- 1 Web/backend engineer (FastAPI wrapper, async jobs)

**Shared Responsibility**
- 1 Architect (oversee core/ library, API contracts)
- 1 DevOps (CI/CD, Docker, deployment)

### Integration Contract
Both services depend on `core/` models and schemas:
1. **API Contract**: Defined in `core/api_schema.py` (Pydantic)
2. **Data Model Contract**: Defined in `core/models/` (SQLAlchemy + dataclasses)
3. **CI/CD**: `core/` changes trigger tests in both services
4. **Deployment**: Separate Docker containers, shared network for APIs

---

## Sprint Timeline

### Sprint 1 (Week 1-2): Parallel foundation
- **Dashboard**: Data ingestion (1 source) + basic API + map UI
- **Simulator**: Hourly balance model + scenario config form
- **Core**: Finalize shared models

### Sprint 2 (Week 3-4): Features
- **Dashboard**: Multi-source data + CO₂ metrics + power charts + live demo
- **Simulator**: MILP optimization + "City 200k" scenario
- **Core**: Stability, add emission utils

### Sprint 3 (Week 5-6.5): Polish
- **Dashboard**: API v1.0 stabilization + public export + ext. docs
- **Simulator**: Preset scenarios + PDF reports + comparison dashboard
- **Core**: Final review, release v1.0

---

## Key Interdependencies

| Dependency | Track | Reason | Mitigation |
|------------|-------|--------|------------|
| `core/models` | Both | Data consistency | Lock API early, version carefully |
| Dashboard API → Simulator | 2 uses 1 | Real NPP data for validation | Use mock data in Sprint 1, integrate later |
| Emissions calc | Both | Different use (reporting vs optimization) | Single `core.utils.emissions_calculator` |
| Load profiles | 2 → 1 (future) | Dashboard may show forecasts | Defined in `core/models`, shared repo |

---

## Success Metrics

### Track 1 (Dashboard)
- ✅ API response time < 200ms (p95)
- ✅ 99.5% data availability (uptime)
- ✅ >10k monthly active users on public dashboard
- ✅ OpenAPI spec auto-generated, SDKs available

### Track 2 (Simulator)
- ✅ Optimization converges in < 60s for hourly horizon
- ✅ Accuracy within 5% vs benchmark industrial solver
- ✅ Support 4+ concurrent simulations
- ✅ Preset scenarios validated by energy experts

### Both
- ✅ Zero data inconsistencies (core/ test coverage >90%)
- ✅ Deployment automated (GitHub Actions)
- ✅ Documentation >80% code coverage

---

## Next Steps

1. **Week 0** (Today):
   - Approve roadmap & team assignments
   - Scaffold `core/`, `services/dashboard-api`, `services/microgrid-sim` directories
   - Finalize Pydantic models for `core/models/`

2. **Week 1 Start**:
   - Dashboard team: Set up FastAPI, first data connector (UA-energy)
   - Simulator team: Build `simulator.py` hourly balance module
   - Both: Integrate `core/` into their services

3. **Weekly Syncs**:
   - Mondays: Architecture review (core/ changes, API updates)
   - Fridays: Integration test (cross-service contract validation)
