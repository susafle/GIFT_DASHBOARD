# 🚀 How to Run the GIFT Oceanographic Dashboard

## 📋 Prerequisites

Before running the dashboard, ensure you have:
- Python 3.8 or higher installed
- Your data file located at: `../data/GIFT_database_prepared.csv`
- All image assets in: `app/assets/img/` (phys.jpg, bg.jpg)

## 🔧 Setup Instructions

### 1. Open Terminal
Navigate to the project directory:
```bash
cd "/Users/susanaflecha/Library/CloudStorage/Dropbox/Mac (2)/Documents/GitHub/GIFT_EDA/panel"
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt.

### 3. Install/Update Dependencies (if needed)
If this is your first time or if dependencies have changed:
```bash
pip install -r requirements.txt
```

## ▶️ Running the Dashboard

### Start the Streamlit App
```bash
streamlit run app/main.py --server.port 8501
```

The dashboard will automatically open in your default web browser at:
- **URL:** http://localhost:8501

## 🛑 Stopping the Dashboard

To stop the dashboard:
1. Go to the terminal where it's running
2. Press `Ctrl + C`
3. Deactivate the virtual environment (optional):
   ```bash
   deactivate
   ```

## 🔄 Troubleshooting

### Problem: Port 8501 is already in use
**Solution:** Kill existing Streamlit processes:
```bash
pkill -9 -f "streamlit run"
```
Then run the dashboard again.

### Problem: Module not found errors
**Solution:** Ensure virtual environment is activated and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Data not loading
**Solution:** Check that the data file exists:
```bash
ls -la ../data/GIFT_database_prepared.csv
```

### Problem: Images not displaying
**Solution:** Verify image files exist:
```bash
ls -la app/assets/img/
```

### Problem: Cache issues
**Solution:** Clear cache and restart:
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Clear Streamlit cache (if needed)
rm -rf .streamlit/cache

# Restart the dashboard
streamlit run app/main.py --server.port 8501
```

## 📁 Project Structure

```
panel/
├── app/
│   ├── main.py                 # Main application entry point
│   ├── assets/
│   │   └── img/                # Images (phys.jpg, bg.jpg)
│   ├── config/
│   │   └── config.yaml         # Configuration settings
│   ├── modules/                # Dashboard modules
│   │   ├── executive.py        # GIFT Data Overview
│   │   ├── physical.py         # Physical Oceanography & Biogeochemistry
│   │   └── temporal.py         # Temporal Analysis
│   ├── utils/                  # Utility functions
│   │   ├── data_loader.py
│   │   ├── processors.py
│   │   └── campaign_analytics.py
│   └── components/             # Reusable components
│       └── charts.py
├── data/
│   └── GIFT_database_prepared.csv  # Main dataset
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
└── HOW_TO_RUN.md              # This file
```

## 🌐 Dashboard Modules

Once running, you can access these modules:

1. **GIFT Data Overview** - Executive metrics and KPIs
2. **GIFT Stations Location** - Interactive geospatial map
3. **Physical Oceanography & Biogeochemistry** - T-S diagrams, water mass analysis
4. **Correlation Analysis** - Variable correlations and relationships
5. **Temporal Analysis** - Annual trends and seasonal patterns
6. **Data Quality** - Outlier detection and analysis
7. **Publications** - Scientific publications from GIFT Network
8. **About** - Project information and team

## 💡 Quick Start Command (All-in-One)

For a quick start, copy and paste this into your terminal:

```bash
cd "/Users/susanaflecha/Library/CloudStorage/Dropbox/Mac (2)/Documents/GitHub/GIFT_EDA/panel" && source venv/bin/activate && streamlit run app/main.py --server.port 8501
```

## 📧 Support

For issues or questions:
- **Author:** Dr. Susana Flecha
- **Email:** susana.flecha@csic.es
- **Principal Investigator:** Dr. I. Emma Huertas (emma.huertas@csic.es)

---

**Last Updated:** October 2, 2025
**Dashboard Version:** 1.0
**Python Version Required:** 3.8+
