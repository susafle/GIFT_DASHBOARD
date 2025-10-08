# 🌊 GIFT Oceanographic Intelligence Platform

**A Business Intelligence Dashboard for Marine Science**

[![Status](https://img.shields.io/badge/status-in_development-yellow)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 Overview

The **GIFT Oceanographic Intelligence Platform** transforms raw oceanographic data from the Gibraltar Fixed Time Series (GIFT) Network into actionable insights through interactive dashboards, advanced analytics, and real-time monitoring.

### Key Features

✅ **Real-time Monitoring** - Live oceanographic parameter tracking
✅ **Interactive T-S Diagrams** - Water mass characterization
✅ **Geospatial Analysis** - Station mapping and spatial patterns
✅ **Temporal Trends** - Seasonal cycles and long-term changes
✅ **ML-Powered Clustering** - Automated water mass classification
✅ **Quality Control** - Automated outlier detection and validation
✅ **Multi-User Access** - Role-based permissions
✅ **Export & Reporting** - PDF, Excel, CSV downloads

---

## 🗂️ Project Structure

```
GIFT_EDA/panel/
│
├── ARCHITECTURE.md          # Detailed system architecture (THIS FILE)
├── README.md                # Quick start guide
├── requirements.txt         # Python dependencies
│
├── app/                     # Dashboard application
│   ├── main.py             # Entry point (Dash/Streamlit)
│   ├── config.py           # Configuration settings
│   ├── modules/            # Dashboard modules
│   │   ├── executive.py    # Executive dashboard
│   │   ├── campaigns.py    # Campaign management
│   │   ├── physical.py     # Physical oceanography (T-S diagrams)
│   │   ├── biogeochem.py   # Biogeochemistry
│   │   ├── climate_gas.py  # Greenhouse gases
│   │   ├── correlation.py  # Correlation analysis
│   │   ├── geospatial.py   # Maps and spatial analysis
│   │   ├── temporal.py     # Time series analysis
│   │   ├── clustering.py   # ML clustering
│   │   └── quality.py      # Data quality control
│   │
│   ├── components/         # Reusable UI components
│   │   ├── charts.py       # Chart templates
│   │   ├── tables.py       # Table components
│   │   └── filters.py      # Filter widgets
│   │
│   └── utils/              # Utility functions
│       ├── data_loader.py  # Data access layer
│       ├── stats.py        # Statistical functions
│       └── validators.py   # Data validation
│
├── data/                   # Data storage
│   ├── raw/               # Raw CSV files
│   ├── processed/         # Cleaned data
│   └── cache/             # Cached aggregates
│
├── database/              # Database scripts
│   ├── schema.sql         # PostgreSQL schema
│   ├── migrations/        # Database migrations
│   └── seeds/             # Sample data
│
├── tests/                 # Unit and integration tests
│   ├── test_modules.py
│   └── test_utils.py
│
├── docs/                  # Additional documentation
│   ├── user_guide.md
│   ├── api_reference.md
│   └── deployment.md
│
├── docker/                # Docker configurations
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── notebooks/             # Jupyter notebooks (exploratory)
    └── eda.ipynb          # Original EDA notebook
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 14+ (or Docker)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/GIFT_EDA.git
   cd GIFT_EDA/panel
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database (Docker):**
   ```bash
   docker-compose up -d postgres
   ```

5. **Load sample data:**
   ```bash
   python scripts/load_data.py --input ../data/GIFT_database_prepared.csv
   ```

6. **Run the dashboard:**
   ```bash
   python app/main.py
   ```

7. **Open browser:**
   Navigate to `http://localhost:8050`

---

## 📊 Dashboard Modules

### 1️⃣ Executive Dashboard
High-level KPIs and data status overview.

### 2️⃣ Campaign Management
Monitor research vessel activities and sampling coverage.

### 3️⃣ Physical Oceanography ⭐
**Flagship Module:** Interactive T-S diagrams, water mass classification, vertical profiles.

### 4️⃣ Biogeochemistry
Track nutrients, oxygen, chlorophyll, and organic matter.

### 5️⃣ Climate Gases
Analyze methane and nitrous oxide distributions.

### 6️⃣ Correlation Intelligence
Discover relationships between variables with interactive heatmaps.

### 7️⃣ Geospatial Analysis
Interactive maps showing station locations and spatial patterns.

### 8️⃣ Temporal Analysis
Seasonal cycles, trends, and forecasting.

### 9️⃣ Multivariate Clustering
PCA and K-means for water mass classification.

### 🔟 Data Quality Control
Outlier detection, missing data analysis, validation rules.

---

## 🛠️ Technology Stack

**Backend:**
- Dash (Plotly) / Streamlit
- FastAPI (REST API)
- PostgreSQL + TimescaleDB
- Redis (caching)

**Frontend:**
- Plotly (interactive charts)
- Folium (maps)
- Dash Bootstrap Components

**Data Science:**
- Pandas, NumPy, SciPy
- Scikit-learn (ML)
- Statsmodels (time series)

**DevOps:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)

---

## 📚 Documentation

- **[Architecture Guide](ARCHITECTURE.md)** - Comprehensive system design
- **[User Manual](docs/user_guide.md)** - How to use the dashboard
- **[API Reference](docs/api_reference.md)** - API endpoints documentation
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions

---

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👥 Team

**Project Lead:** [Your Name]
**Data Science:** [Team Member]
**Backend Development:** [Team Member]
**Oceanography Advisor:** [Team Member]

---

## 📧 Contact

**Email:** gift-dashboard@oceanography.org
**GitHub Issues:** https://github.com/yourusername/GIFT_EDA/issues
**Documentation:** https://gift-dashboard.readthedocs.io

---

## 🙏 Acknowledgments

- **GIFT Network** - Data providers
- **Spanish Institute of Oceanography (IEO)** - Research support
- **Plotly Team** - Excellent visualization library
- **Open Source Community** - Contributions and feedback

---

## 🗺️ Roadmap

### Phase 1 (Current) - Foundation ✅
- [x] Architecture design
- [x] Database schema
- [ ] Core modules implementation
- [ ] Docker setup

### Phase 2 - Core Features 🚧
- [ ] All TIER 2 modules
- [ ] User authentication
- [ ] API development

### Phase 3 - Advanced Analytics 📅
- [ ] ML clustering
- [ ] Time series forecasting
- [ ] Automated reporting

### Phase 4 - Production 🚀
- [ ] Cloud deployment
- [ ] Performance optimization
- [ ] Public release

---

## 📊 Current Status

**Development Progress:** 15%

| Module | Status |
|--------|--------|
| Architecture | ✅ Complete |
| Database Schema | ✅ Complete |
| Executive Dashboard | 🚧 In Progress |
| T-S Diagrams | 🚧 In Progress |
| Campaign Management | 📅 Planned |
| Biogeochemistry | 📅 Planned |
| Geospatial | 📅 Planned |
| ML Clustering | 📅 Planned |

---

**Last Updated:** October 2, 2025
**Version:** 0.1.0-alpha

---

⭐ **Star this repo if you find it useful!** ⭐
