# 🚀 GIFT Intelligence Platform - Quick Start Guide

## 🌊 Welcome!

This guide will help you get the GIFT Oceanographic Intelligence Platform running in **5 minutes**.

---

## 📋 Prerequisites

- **Python 3.9+** installed
- **Git** installed (optional)
- **Terminal/Command Line** access

---

## 🛠️ Installation

### Option 1: Automated Setup (Recommended) 🎯

**macOS/Linux:**
```bash
cd panel
./run_dashboard.sh
```

**Windows:**
```bash
cd panel
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

### Option 2: Manual Setup

1. **Navigate to panel directory:**
   ```bash
   cd GIFT_EDA/panel
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

4. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Verify data file exists:**
   ```bash
   ls ../data/GIFT_database_prepared.csv
   ```

6. **Run the dashboard:**
   ```bash
   streamlit run app/main.py
   ```

7. **Open browser:**
   Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
panel/
├── app/
│   ├── main.py                  # 🎯 Main application entry point
│   ├── config/
│   │   └── config.yaml          # Configuration settings
│   ├── modules/                 # Dashboard modules
│   │   ├── executive.py         # Executive dashboard
│   │   └── physical.py          # Physical oceanography (T-S diagrams)
│   ├── components/
│   │   └── charts.py            # Reusable chart components
│   └── utils/                   # Core logic layers
│       ├── data_loader.py       # 💾 Data Storage Layer
│       ├── processors.py        # 📊 Data Processing Layer
│       └── analytics.py         # 🧠 Business Logic Layer
├── data/                        # Data directories
├── requirements.txt             # Python dependencies
└── run_dashboard.sh             # Startup script
```

---

## 🎯 Architecture Overview

The dashboard follows a **4-tier architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│  📱 PRESENTATION LAYER (Streamlit UI + Modules)                 │
├─────────────────────────────────────────────────────────────────┤
│  🧠 BUSINESS LOGIC LAYER (Analytics & ML)                       │
├─────────────────────────────────────────────────────────────────┤
│  📊 DATA PROCESSING LAYER (Transformations & Filtering)         │
├─────────────────────────────────────────────────────────────────┤
│  💾 DATA STORAGE LAYER (Data Loading & Caching)                 │
└─────────────────────────────────────────────────────────────────┘
```

**Layer Responsibilities:**

1. **Presentation Layer** (`app/main.py`, `app/modules/*`)
   - User interface
   - Navigation
   - Module rendering

2. **Business Logic Layer** (`app/utils/analytics.py`)
   - Oceanographic analysis
   - Machine learning
   - Statistical calculations

3. **Data Processing Layer** (`app/utils/processors.py`)
   - Data transformations
   - Filtering & validation
   - Water mass classification

4. **Data Storage Layer** (`app/utils/data_loader.py`)
   - Data loading from CSV
   - Caching with Streamlit
   - Configuration management

---

## 🎨 Features Overview

### ✅ Implemented Modules

#### 1️⃣ **Executive Overview** 📊
- Key performance indicators (KPIs)
- Data completeness metrics
- Water mass distribution
- Environmental parameter summary
- Alert notifications

#### 2️⃣ **Physical Oceanography** 🌡️ ⭐ **FLAGSHIP**
- **Single Variable T-S Diagrams**
  - Interactive temperature-salinity plots
  - Color-coding by any variable
  - Multiple colorscale options
- **Multi-Variable T-S Diagrams**
  - 4-panel comparison views
  - Simultaneous visualization of multiple parameters
- **Water Mass Analysis**
  - Automated classification (Atlantic/Mediterranean/Mixed)
  - Property statistics per water mass
  - Classification scatter plots
- **Vertical Profiles**
  - Depth vs. variable plots
  - Gradient calculations

### 🚧 Planned Modules (Under Development)

3️⃣ **Biogeochemistry** 🧪
4️⃣ **Correlation Analysis** 🔗
5️⃣ **Geospatial Analysis** 🗺️
6️⃣ **Temporal Analysis** 📅
7️⃣ **Data Quality Control** ✅

---

## 🧭 Navigation Guide

### Sidebar Menu

- **Executive Overview**: High-level dashboard with KPIs
- **Physical Oceanography**: T-S diagrams and water mass analysis
- **Other Modules**: Placeholders for future development

### Interactive Controls

- **Sidebar**: Module-specific filters and settings
- **Selectboxes**: Choose variables for analysis
- **Multiselect**: Compare multiple variables
- **Expanders**: Collapsible sections for details

---

## 📊 Using T-S Diagrams

### Single Variable T-S Diagram

1. Navigate to **Physical Oceanography**
2. Select "T-S Diagram (Single Variable)"
3. Choose a variable for color-coding (e.g., "DISSOLVED OXYGEN")
4. Select a colorscale (e.g., "Viridis")
5. Explore interactive plot:
   - **Hover**: View exact values
   - **Zoom**: Click and drag
   - **Pan**: Hold shift + drag
   - **Reset**: Double-click

### Multi-Variable T-S Diagrams

1. Select "Multi-Variable T-S Diagrams"
2. Choose up to 4 variables for comparison
3. View 2×2 grid of T-S diagrams
4. Compare patterns across variables

### Water Mass Analysis

1. Select "Water Mass Analysis"
2. View automatic classification results
3. Explore water mass properties
4. Analyze T-S diagram color-coded by water mass

---

## 🐛 Troubleshooting

### Issue: "Data file not found"

**Solution:**
Ensure `GIFT_database_prepared.csv` exists at:
```
GIFT_EDA/data/GIFT_database_prepared.csv
```

### Issue: "Module not found" errors

**Solution:**
Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Port already in use

**Solution:**
Stop other Streamlit instances or use different port:
```bash
streamlit run app/main.py --server.port 8502
```

### Issue: Slow loading

**Solution:**
- Check data file size
- Clear Streamlit cache: Press "C" in dashboard
- Restart dashboard

---

## 🎯 Quick Tips

1. **Use sidebar filters** to customize views
2. **Hover over charts** for detailed information
3. **Check "About" page** for documentation
4. **Explore interactivity**: zoom, pan, hover on all plots
5. **Watch for alerts** in Executive Overview

---

## 📚 Next Steps

1. ✅ Explore Executive Overview
2. ✅ Create T-S diagrams in Physical Oceanography
3. ✅ Analyze water mass classifications
4. ✅ Check data quality metrics
5. 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
6. 🛠️ Wait for additional modules (coming soon!)

---

## 💡 Key Concepts

### T-S Diagram (Temperature-Salinity)
- **Purpose**: Identify and characterize water masses
- **X-axis**: Salinity (PSS-78)
- **Y-axis**: Temperature (°C, ITS-90)
- **Color**: Third variable (e.g., oxygen, nutrients)
- **Interpretation**: Different water masses occupy distinct regions

### Water Masses in Strait of Gibraltar

1. **Atlantic Water**
   - Lower salinity (<37)
   - Lower temperature
   - Flows eastward (surface)

2. **Mediterranean Water**
   - Higher salinity (>38)
   - Higher temperature
   - Flows westward (deep)

3. **Mixed Water**
   - Intermediate properties
   - Active mixing zone

---

## 📧 Support

- **Documentation**: [ARCHITECTURE.md](ARCHITECTURE.md), [README.md](README.md)
- **Issues**: GitHub Issues
- **Email**: gift-dashboard@oceanography.org

---

## 🎉 You're Ready!

The GIFT Intelligence Platform is now running. Explore the data, create visualizations, and discover oceanographic insights!

**Dashboard URL:** http://localhost:8501

---

**Version:** 1.0.0
**Last Updated:** October 2025
