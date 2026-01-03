# UHIP Parallel Development Tracks
## Nuclear Power Plant Dashboard + Microgrid Simulator

**Project Structure**: Two parallel tracks sharing core models but developing separately for maximum team autonomy.

---

## 🚀 TRACK 1: PUBLIC NUCLEAR POWER PLANT (АЕС) DASHBOARD

### Objectives
- Ingest & normalize open energy data (UA-energy, Міненерго, Енергоатом)
- Unified data model: plant blocks, states, capacity, plan/actual, CO₂ equivalents
- Public REST/GraphQL API with OpenAPI docs
- Real-time dashboard: plant map, block status, power graphs, emissions avoided

### Sprint 1 Deliverables
- [ ] Ingest UA-energy data source
- [ ] Core API: `/plants`, `/units`, `/timeseries` endpoints
- [ ] Basic power generation chart
- [ ] Data normalization to unified schema

### Sprint 2 Deliverables
- [ ] CO₂ equivalent calculations
- [ ] Unit maneuver tracking
- [ ] Public demo dashboard
- [ ] Python/JS client examples

### Sprint 3 Deliverables
- [ ] API stabilization & documentation
- [ ] Multi-source integration (Міненерго, Енергоатом)
- [ ] Advanced emissions metrics

### Tech Stack
- **Backend**: FastAPI (Python) or Node.js Express
- **Database**: PostgreSQL + TimescaleDB (time-series)
- **Frontend**: React + D3.js charts
- **API**: OpenAPI/Swagger documentation
- **CI/CD**: GitHub Actions → Docker → AWS/Azure

---

## ⚡ TRACK 2: MICROGRID SIMULATOR (АЕС/SMR + RENEWABLES)

### Objectives
- Optimize nuclear/SMR + renewables (solar/wind) + battery storage system
- MILP/LP solver integration (Pyomo/OR-Tools)
- AI layer: RL agent or load/renewable forecasting model
- Web UI: configure scenarios, view generation/consumption/charge graphs
- Metrics: CO₂, unmet load, dump energy

### Sprint 1 Deliverables
- [ ] Toy microgrid model (static profiles, no optimization)
- [ ] Hourly balance graphs
- [ ] Basic UI config form (SMR %, renewables %, battery capacity)
- [ ] Load profile templates (city, industrial, data center)

### Sprint 2 Deliverables
- [ ] MILP/LP solver integration
- [ ] Scenario: "City 200k + SMR"
- [ ] Economic metrics (cost/CO₂)
- [ ] Optimization result visualization

### Sprint 3 Deliverables
- [ ] 3+ preset scenarios (industrial park, deoccupied territory)
- [ ] RL agent or ML forecast model
- [ ] Report export (PDF/CSV)
- [ ] Real-time simulation mode

### Tech Stack
- **Core**: Python (simulation + optimization)
- **Optimization**: Pyomo, OR-Tools, or Gurobi
- **AI/ML**: TensorFlow/PyTorch or scikit-learn
- **Frontend**: React or Vue.js
- **Data**: NumPy, Pandas, SQLAlchemy
- **Deployment**: Docker + Docker Compose

---

## 📦 SHARED CORE (Both Tracks Use)

### Directory: `core/`

```
core/
├── models/
│   ├── plant.py          # Plant, Unit, Block entities
│   ├── timeseries.py     # TimeSeries, Metric data
│   ├── emissions.py      # CO₂ equivalent, emissions calc
│   └── config.py         # Shared enums, constants
├── api_schema/
│   ├── plant_schema.json # OpenAPI plant endpoints
│   ├── unit_schema.json
│   └── timeseries_schema.json
├── sim_profiles/
│   ├── load_profiles.py  # City, Industrial, DataCenter templates
│   ├── renewable_profiles.py  # Solar, wind typical curves
│   └── battery_profiles.py    # Storage characteristics
└── utils/
    ├── normalization.py  # Data cleaning + unification
    ├── emissions.py      # CO₂ calculation helpers
    └── datautils.py
```

### Shared Entities
```python
# Plant: Ukrainian nuclear plants (VVER-440, VVER-1000, SMR prototypes)
class Plant:
  id: str
  name: str
  location: GeoPoint
  type: PlantType  # VVER440, VVER1000, SMR
  units: List[Unit]
  status: PlantStatus
  capacity_mw: float

# Unit: Individual reactor block
class Unit:
  id: str
  plant_id: str
  name: str
  capacity_mw: float
  generation_mw: float
  status: UnitStatus  # RUNNING, OFFLINE, MAINTENANCE, etc.
  ramp_rate_mw_per_min: float  # For simulator
  min_load_pct: float  # For simulator

# TimeSeries: Hourly metrics
class TimeSeries:
  id: str
  unit_id: str
  timestamp: datetime
  generation_mwh: float
  plan_mwh: float
  co2_kg_equiv: float
  status: str

# EmissionMetrics
class EmissionMetrics:
  avoided_co2_tonnes: float
  equivalent_cars_taken_off_road: int
  equivalent_trees_planted: int
```

---

## 🔄 PARALLEL EXECUTION PATTERN

### Directory Structure
```
uhip-unified-hybrid-intelligence/
├── core/                    # Shared models, schemas, profiles
├── services/
│   ├── dashboard-api/      # Track 1: FastAPI service
│   │   ├── app.py
│   │   ├── routers/
│   │   │   ├── plants.py   # GET /plants, /units, /timeseries
│   │   │   └── emissions.py
│   │   └── requirements.txt
│   ├── dashboard-ui/       # Track 1: React frontend
│   │   ├── src/
│   │   │   ├── components/PlantMap.jsx
│   │   │   ├── components/PowerChart.jsx
│   │   │   └── pages/Dashboard.jsx
│   │   └── package.json
│   ├── microgrid-sim/      # Track 2: Simulator service
│   │   ├── sim_model.py    # System model
│   │   ├── optimizer.py    # MILP/LP solver
│   │   ├── rl_agent.py     # Optional: RL layer
│   │   └── requirements.txt
│   └── microgrid-ui/       # Track 2: Simulator UI
│       ├── src/
│       │   ├── ConfigForm.jsx
│       │   ├── SimResults.jsx
│       │   └── pages/Simulator.jsx
│       └── package.json
├── PARALLEL-TRACKS.md      # THIS FILE
├── SPRINT-1.md
├── SPRINT-2.md
└── docker-compose.yml      # Local dev: all services
```

### API Contract (Core → Services)

**Track 1 & 2 share:**
```python
# Both import from core.models
from core.models import Plant, Unit, TimeSeries, EmissionMetrics
from core.sim_profiles import LoadProfile, RenewableProfile, BatteryProfile
```

**Track 1 Publishes:**
- REST API: `GET /plants`, `GET /plants/{id}/units`, `GET /timeseries`
- GraphQL: Query plants, units, emissions

**Track 2 Consumes & Extends:**
- Real plant data from Track 1 API (optional)  
- Uses core models for synthetic scenario generation
- Exports results as Track 1-compatible TimeSeries

---

## 📅 SPRINT PLANNING

### Sprint 1 (Week 1-2): MVP Parallel Start

**Track 1 Goals**
- ✅ Data ingestion pipeline for UA-energy
- ✅ Normalized Plant/Unit/TimeSeries models
- ✅ FastAPI with `/plants` endpoint
- ✅ Simple React chart of power generation

**Track 2 Goals**
- ✅ Static microgrid model (no optimization)
- ✅ Hourly balance simulation
- ✅ Config UI (SMR %, batteries, load type)
- ✅ Basic generation vs demand graph

**Blockers/Sync Points**
- Core models finalized by EOD Day 1
- Weekly sync: Wed 10am UTC (15 min)

### Sprint 2 (Week 3-4): Optimization + CO₂

**Track 1 Goals**
- ✅ CO₂ calculations + avoided emissions display
- ✅ Maneuver data from plants
- ✅ Public demo dashboard
- ✅ OpenAPI docs + Python/JS examples

**Track 2 Goals**
- ✅ MILP/LP solver (Pyomo)
- ✅ Scenario: "City 200k + 100MW SMR"
- ✅ Economic + environmental metrics
- ✅ Optimization chart (before/after balance)

**Blockers/Sync Points**
- API schema locked (Track 1 → Track 2)
- Integration test: Track 2 can read Track 1 TimeSeries format

### Sprint 3 (Week 5-6): Hardening + Features

**Track 1 Goals**
- ✅ Multi-source integration (3+ data sources)
- ✅ Historical data + forecasting
- ✅ API rate-limiting + caching
- ✅ Production deployment guide

**Track 2 Goals**
- ✅ 3-5 preset scenarios (industrial, residential, etc.)
- ✅ RL agent or ML load forecast
- ✅ Report export (PDF with charts)
- ✅ Real-time simulation UI

---

## 🔗 INTEGRATION POINTS

1. **Shared Models**: Both import `core.models.Plant`, `core.models.TimeSeries`
2. **Data Exchange**: Track 2 can optionally read Track 1 real plant data via API
3. **Profiles**: Track 2 uses `core.sim_profiles` for load/renewable templates
4. **Results Format**: Track 2 outputs same TimeSeries format as Track 1 ingest

---

## 🎯 Definition of Done (DoD)

### Track 1 DoD
- [ ] API endpoints have OpenAPI docs
- [ ] 90%+ test coverage (unit + integration)
- [ ] Data normalized to unified schema
- [ ] Dashboard loads real data live
- [ ] No data older than 1 hour
- [ ] CO₂ calculations validated against IPCC factors

### Track 2 DoD
- [ ] Optimizer produces feasible solution
- [ ] Unmet load < 2% in nominal scenarios
- [ ] CO₂/cost metrics match published studies
- [ ] ± 5% error on load forecast
- [ ] 10+ scenarios pre-configured
- [ ] Report export reproducible

---

## 📞 Communication

- **Weekly Sync**: Wednesday 10am UTC (Slack: #uhip-tracks)
- **PR Reviews**: 24h turnaround
- **Blocker Escalation**: Slack @romanchaa997 immediately
- **Shared Docs**: Notion (roadmap, decisions)

