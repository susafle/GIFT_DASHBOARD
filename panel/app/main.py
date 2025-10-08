"""
GIFT Oceanographic Intelligence Platform
MAIN APPLICATION

Streamlit dashboard with 4-tier architecture:
├── PRESENTATION LAYER (this file + modules)
├── BUSINESS LOGIC LAYER (utils/analytics.py)
├── DATA PROCESSING LAYER (utils/processors.py)
└── DATA STORAGE LAYER (utils/data_loader.py)
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add utils to path
sys.path.append(str(Path(__file__).parent))

# Import modules
from modules import executive, physical, temporal


# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="GIFT Intelligence Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="auto",  # Auto-collapse on mobile
    menu_items={
        'Get Help': 'https://github.com/susafle/GIFT_DASHBOARD',
        'Report a bug': 'https://github.com/susafle/GIFT_DASHBOARD/issues',
        'About': """
        # GIFT Oceanographic Intelligence Platform

        **Version:** 1.0.0

        A Business Intelligence Dashboard for marine science, transforming
        oceanographic data from the Gibraltar Fixed Time Series (GIFT) Network
        into actionable insights.

        **Developed by:** Data Science & Oceanography Team
        """
    }
)

# Mobile viewport meta tag
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
""", unsafe_allow_html=True)


# ===== CUSTOM CSS STYLING =====
def load_custom_css():
    """Apply custom CSS styling with mobile responsiveness"""
    st.markdown("""
        <style>
        /* Mobile-first responsive design */
        @media (max-width: 768px) {
            /* Adjust main title for mobile */
            .main-title {
                padding: 30px 15px !important;
            }

            .main-title h1 {
                font-size: 1.5rem !important;
            }

            .main-title p {
                font-size: 0.9rem !important;
            }

            /* Make metrics stack vertically on mobile */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
            }

            /* Adjust sidebar for mobile */
            section[data-testid="stSidebar"] {
                width: 100% !important;
            }

            /* Make images responsive */
            img {
                max-width: 100% !important;
                height: auto !important;
            }

            /* Adjust plot sizes */
            div[data-testid="stPlotlyChart"] {
                width: 100% !important;
            }

            /* Footer badges for mobile */
            .footer-badges img {
                width: 100% !important;
                max-width: 200px !important;
                margin: 5px 0 !important;
            }
        }

        /* Tablet adjustments */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main-title h1 {
                font-size: 2rem !important;
            }
        }

        /* Main title styling with background image */
        .main-title {
            background: linear-gradient(135deg, rgba(30, 60, 114, 0.85) 0%, rgba(42, 82, 152, 0.85) 25%, rgba(102, 126, 234, 0.85) 75%, rgba(118, 75, 162, 0.85) 100%),
                        url('data:image/jpeg;base64,/9j/4AAQSkZJRg...') center/cover;
            padding: 50px 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: relative;
            backdrop-filter: blur(2px);
        }

        .main-title h1 {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            font-size: 2.5rem;
            font-weight: 700;
        }

        .main-title p {
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }

        /* Metric cards */
        div[data-testid="metric-container"] {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #1e3c72;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #34495e;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Headers */
        h1, h2, h3 {
            color: #1e3c72;
        }

        /* Make all images responsive */
        img {
            max-width: 100%;
            height: auto;
        }

        /* Responsive tables */
        table {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }

        /* Info boxes */
        .stAlert {
            border-radius: 8px;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border-radius: 8px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #1e3c72;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
        }

        .stButton>button:hover {
            background-color: #2a5298;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
        }

        /* Module header with floating image */
        .module-header {
            position: relative;
            padding: 20px;
            margin-bottom: 20px;
        }

        .module-image-float {
            float: right;
            margin: 0 0 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            max-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)


# ===== HEADER =====
def render_header():
    """Render main header with background image"""
    import base64
    from pathlib import Path

    # Try to load and encode the background image
    try:
        # Support both local and Streamlit Cloud paths
        img_path = Path("panel/app/assets/img/panel.jpg")
        if not img_path.exists():
            img_path = Path("app/assets/img/panel.jpg")

        if img_path.exists():
            with open(img_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()

            st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(30, 60, 114, 0.3) 0%, rgba(42, 82, 152, 0.3) 25%, rgba(102, 126, 234, 0.3) 75%, rgba(118, 75, 162, 0.3) 100%),
                                url('data:image/jpeg;base64,{img_data}');
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center 75%;
                    background-blend-mode: overlay;
                    padding: 30px 30px 120px 30px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    min-height: 350px;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;
                    align-items: center;
                ">
                    <h1 style="color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9); font-size: 2.5rem; font-weight: 700; margin: 0;">
                        GIFT Oceanographic Intelligence Platform
                    </h1>
                    <p style="font-size: 18px; margin: 12px 0 0 0; text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.9);">
                        Gibraltar Fixed Time Series - Marine Science Dashboard
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback if image not found
            st.markdown("""
                <div class="main-title">
                    <h1>🌊 GIFT Oceanographic Intelligence Platform</h1>
                    <p style="font-size: 18px; margin: 0;">Gibraltar Fixed Time Series - Marine Science Dashboard</p>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback on error
        st.markdown("""
            <div class="main-title">
                <h1>🌊 GIFT Oceanographic Intelligence Platform</h1>
                <p style="font-size: 18px; margin: 0;">Gibraltar Fixed Time Series - Marine Science Dashboard</p>
            </div>
        """, unsafe_allow_html=True)


# ===== SIDEBAR NAVIGATION =====
def render_sidebar():
    """Render sidebar with navigation menu"""
    with st.sidebar:
        try:
            # Try Streamlit Cloud path first, then local path
            logo_path = "panel/app/assets/img/logo.png"
            if not Path(logo_path).exists():
                logo_path = "app/assets/img/logo.png"
            st.image(logo_path, use_container_width=True)
        except:
            st.markdown("### 🌊 GIFT Network")

        st.markdown("---")

        selected = option_menu(
            menu_title="Navigation",
            options=[
                "GIFT Stations Location",
                "GIFT Data Overview",
                "Physical Oceanography & Biogeochemistry",
                "Correlation Analysis",
                "Temporal Analysis",
                "Data Quality",
                "Publications",
                "About"
            ],
            icons=[
                "globe",
                "speedometer2",
                "thermometer-half",
                "diagram-3",
                "calendar3",
                "check-circle",
                "book",
                "info-circle"
            ],
            menu_icon="menu-app",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#34495e"},
                "icon": {"color": "#ffffff", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "2px",
                    "color": "#ffffff",
                    "--hover-color": "#4a5f7f",
                },
                "nav-link-selected": {"background-color": "#1e3c72", "color": "white"},
                "menu-title": {"color": "#ffffff"},
                "menu-icon": {"color": "#ffffff"}
            }
        )

        st.markdown("---")

        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        try:
            from utils.data_loader import load_gift_data, get_data_summary
            df = load_gift_data()
            summary = get_data_summary(df)

            st.metric("Observations", f"{summary['total_observations']:,}")
            st.metric("Vessels", summary['vessels'])
            st.metric("Campaigns", summary['campaigns'])
        except Exception as e:
            st.info("Loading data...")

        st.markdown("---")

        # Author Info
        st.markdown("""
            <div style='text-align: center; color: #ffffff; font-size: 14px; padding: 10px;'>
                <p style='margin-bottom: 8px;'><strong>Dashboard by:</strong></p>
                <p style='margin: 5px 0;'><strong>Susana Flecha</strong></p>
            </div>
        """, unsafe_allow_html=True)

        # Social links with icons
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div style='text-align: center;'>
                    <a href='https://github.com/susafle' target='_blank' style='text-decoration: none;'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#ffffff" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                    </a>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div style='text-align: center;'>
                    <a href='https://www.linkedin.com/in/susana-flecha-b5b05a44/' target='_blank' style='text-decoration: none;'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#ffffff" viewBox="0 0 16 16">
                            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                        </svg>
                    </a>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div style='text-align: center;'>
                    <a href='https://orcid.org/0000-0003-2826-5820' target='_blank' style='text-decoration: none;'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#ffffff" viewBox="0 0 256 256">
                            <path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/>
                            <path fill="#000000" d="M86.3 186.2H70.9V79.1h15.4v107.1zM108.9 79.1h41.6c39.6 0 57 28.3 57 53.6 0 27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7C191.7 111.2 178 93 148 93h-23.7v79.4zM71.6 54.5c0-5.2 4.2-9.3 9.4-9.3 5.1 0 9.3 4.1 9.3 9.3 0 5.1-4.2 9.3-9.3 9.3-5.2 0-9.4-4.2-9.4-9.3z"/>
                        </svg>
                    </a>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Footer
        st.markdown("""
            <div style='text-align: center; color: #b0b0b0; font-size: 12px;'>
                <p><strong>GIFT Network</strong></p>
                <p>Version 1.0.0</p>
                <p>© 2025</p>
            </div>
        """, unsafe_allow_html=True)

        return selected


# ===== MAIN CONTENT ROUTER =====
def render_main_content(selected_module):
    """Route to selected module"""

    if selected_module == "GIFT Data Overview":
        executive.render_executive_dashboard()

    elif selected_module == "Physical Oceanography & Biogeochemistry":
        physical.render_physical_oceanography()

    elif selected_module == "Publications":
        st.title("📚 Publications")
        st.markdown("### Scientific Publications from GIFT Network")

        st.markdown("---")

        # Publications list (from most recent to oldest)
        publications = [
            {
                "year": 2024,
                "authors": "Lange, N. et al.",
                "title": "Synthesis Product for Ocean Time Series (SPOTS) -- a ship-based biogeochemical pilot",
                "journal": "Earth Syst Sci Data",
                "volume": "16",
                "pages": "1901–1931",
                "doi": "10.5194/essd-16-1901-2024"
            },
            {
                "year": 2021,
                "authors": "García-Lafuente, J. et al.",
                "title": "Hotter and Weaker Mediterranean Outflow as a Response to Basin-Wide Alterations",
                "journal": "Frontiers in Marine Science",
                "volume": "",
                "pages": "",
                "doi": "10.3389/fmars.2021.613444"
            },
            {
                "year": 2020,
                "authors": "Álvarez-Salgado, X. A., Otero, J., Flecha, S. & Huertas, I. E.",
                "title": "Seasonality of Dissolved Organic Carbon Exchange Across the Strait of Gibraltar",
                "journal": "Geophys Res Lett",
                "volume": "47",
                "pages": "",
                "doi": ""
            },
            {
                "year": 2019,
                "authors": "Flecha, S., Pérez, F. F., Murata, A., Makaoui, A. & Huertas, I. E.",
                "title": "Decadal acidification in Atlantic and Mediterranean water masses exchanging at the Strait of Gibraltar",
                "journal": "Sci Rep",
                "volume": "9",
                "pages": "1–11",
                "doi": "10.1038/s41598-019-45321-x"
            },
            {
                "year": 2016,
                "authors": "Carracedo, L. I., Pardo, P. C., Flecha, S. & Pérez, F. F.",
                "title": "On the mediterranean water composition",
                "journal": "J Phys Oceanogr",
                "volume": "46",
                "pages": "1339–1358",
                "doi": ""
            },
            {
                "year": 2015,
                "authors": "de la Paz, M., Huertas, I. E., Flecha, S., Ríos, A. F. & Pérez, F. F.",
                "title": "Nitrous oxide and methane in Atlantic and Mediterranean waters in the Strait of Gibraltar: Air-sea fluxes and inter-basin exchange",
                "journal": "Prog Oceanogr",
                "volume": "138",
                "pages": "18–31",
                "doi": ""
            },
            {
                "year": 2015,
                "authors": "Flecha, S. et al.",
                "title": "Trends of pH decrease in the Mediterranean Sea through high frequency observational data: Indication of ocean acidification in the basin",
                "journal": "Sci Rep",
                "volume": "5",
                "pages": "1–8",
                "doi": "10.1038/srep16770"
            },
            {
                "year": 2012,
                "authors": "Navarro, G. et al.",
                "title": "Seasonal-to-interannual variability of chlorophyll-a bloom timing associated with physical forcing in the Gulf of Cádiz",
                "journal": "Advances in Space Research",
                "volume": "50",
                "pages": "1164–1172",
                "doi": ""
            },
            {
                "year": 2012,
                "authors": "Flecha, S. et al.",
                "title": "Anthropogenic carbon inventory in the Gulf of Cádiz",
                "journal": "Journal of Marine Systems",
                "volume": "92",
                "pages": "67–75",
                "doi": ""
            },
            {
                "year": 2009,
                "authors": "Vázquez, A., Flecha, S., Bruno, M., Macías, D. & Navarro, G.",
                "title": "Internal waves and short-scale distribution patterns of chlorophyll in the Strait of Gibraltar and Alborán Sea",
                "journal": "Geophys Res Lett",
                "volume": "36",
                "pages": "",
                "doi": ""
            }
        ]

        # Display publications
        for idx, pub in enumerate(publications, 1):
            with st.container():
                st.markdown(f"#### {idx}. {pub['title']}")
                st.markdown(f"**Authors:** {pub['authors']}")

                citation_parts = [pub['journal']]
                if pub['volume']:
                    citation_parts.append(f"{pub['volume']}")
                if pub['pages']:
                    citation_parts.append(f"{pub['pages']}")
                citation_parts.append(f"({pub['year']})")

                st.markdown(f"**Citation:** {', '.join(citation_parts)}")

                if pub['doi']:
                    st.markdown(f"**DOI:** [{pub['doi']}](https://doi.org/{pub['doi']})")

                st.markdown("---")

    elif selected_module == "Correlation Analysis":
        st.title("🔗 Correlation Analysis")
        st.markdown("### Variable Correlations & Relationships")

        # Load data
        from utils.data_loader import get_data_loader
        loader = get_data_loader()
        df = loader.load_data()
        custom_colors = loader.get_custom_palette()

        if df.empty:
            st.error("❌ No data available")
        else:
            # Get available variables (same filtering as Temporal Analysis)
            exclude_vars = loader.get_exclude_vars()
            available_vars = [col for col in loader.get_filtered_numerical_cols(df)
                              if col not in exclude_vars]

            if not available_vars:
                st.error("❌ No variables available for analysis")
            else:
                # Variable selection for correlation analysis
                st.markdown("#### Select Variables for Correlation Analysis")

                col1, col2 = st.columns(2)
                with col1:
                    min_vars = st.slider("Minimum number of variables", 2, len(available_vars), 5)
                with col2:
                    max_vars = st.slider("Maximum number of variables", min_vars, len(available_vars), min(10, len(available_vars)))

                selected_vars = st.multiselect(
                    "Select variables to include in correlation analysis",
                    available_vars,
                    default=available_vars[:min(10, len(available_vars))],
                    help="Choose oceanographic variables to analyze correlations"
                )

                if len(selected_vars) < 2:
                    st.warning("⚠️ Please select at least 2 variables for correlation analysis")
                else:
                    # Calculate correlation matrix
                    corr_data = df[selected_vars].dropna()

                    if len(corr_data) < 3:
                        st.warning("⚠️ Insufficient data for correlation analysis")
                    else:
                        # Calculate Pearson correlation
                        corr_matrix = corr_data.corr()

                        # Display correlation statistics
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Variables Analyzed", len(selected_vars))
                        with col2:
                            st.metric("Valid Observations", len(corr_data))
                        with col3:
                            max_corr = corr_matrix.where(~np.eye(len(corr_matrix), dtype=bool)).abs().max().max()
                            st.metric("Max Correlation", f"{max_corr:.3f}")

                        st.markdown("---")

                        # Create interactive heatmap
                        import plotly.graph_objects as go

                        fig = go.Figure(data=go.Heatmap(
                            z=corr_matrix.values,
                            x=corr_matrix.columns,
                            y=corr_matrix.columns,
                            colorscale='RdBu_r',  # Red-Blue reversed (red for positive, blue for negative)
                            zmid=0,  # Center colorscale at 0
                            zmin=-1,
                            zmax=1,
                            text=corr_matrix.values,
                            texttemplate='%{text:.2f}',
                            textfont={"size": 10},
                            colorbar=dict(
                                title="Correlation",
                                tickmode="linear",
                                tick0=-1,
                                dtick=0.5
                            ),
                            hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
                        ))

                        fig.update_layout(
                            title="Pearson Correlation Heatmap",
                            xaxis_title="",
                            yaxis_title="",
                            height=max(500, len(selected_vars) * 40),
                            xaxis=dict(tickangle=-45),
                            yaxis=dict(autorange="reversed")
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        # Display strongest correlations
                        st.markdown("---")
                        st.subheader("📊 Strongest Correlations")

                        # Get correlation pairs (excluding diagonal)
                        corr_pairs = []
                        for i in range(len(corr_matrix)):
                            for j in range(i+1, len(corr_matrix)):
                                corr_pairs.append({
                                    'Variable 1': corr_matrix.index[i],
                                    'Variable 2': corr_matrix.columns[j],
                                    'Correlation': corr_matrix.iloc[i, j],
                                    'Abs Correlation': abs(corr_matrix.iloc[i, j])
                                })

                        corr_df = pd.DataFrame(corr_pairs)
                        corr_df = corr_df.sort_values('Abs Correlation', ascending=False).head(10)
                        corr_df = corr_df[['Variable 1', 'Variable 2', 'Correlation']]
                        corr_df['Correlation'] = corr_df['Correlation'].round(3)

                        st.dataframe(corr_df, use_container_width=True, hide_index=True)

    elif selected_module == "GIFT Stations Location":
        st.title("🗺️ GIFT Stations Location")
        st.markdown("### Station Locations & Spatial Distribution")

        # Load data
        from utils.data_loader import load_gift_data
        df = load_gift_data()

        if df.empty:
            st.error("❌ No data available")
        elif 'LATITUDE' not in df.columns or 'LONGITUDE' not in df.columns:
            st.error("❌ Latitude and Longitude columns not found")
        else:
            # Remove rows with missing coordinates
            map_data = df[['LATITUDE', 'LONGITUDE', 'STATION-ID']].dropna()

            if len(map_data) == 0:
                st.warning("⚠️ No valid coordinate data available")
            else:
                # Get unique stations
                stations = map_data.groupby('STATION-ID').agg({
                    'LATITUDE': 'mean',
                    'LONGITUDE': 'mean'
                }).reset_index()

                # Count measurements per station
                station_counts = df.groupby('STATION-ID').size().reset_index(name='measurements')
                stations = stations.merge(station_counts, on='STATION-ID', how='left')

                # Display map statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Stations", len(stations))
                with col2:
                    st.metric("Total Measurements", len(map_data))
                with col3:
                    avg_per_station = len(map_data) / len(stations) if len(stations) > 0 else 0
                    st.metric("Avg. Measurements/Station", f"{avg_per_station:.1f}")

                st.markdown("---")

                # Create interactive map using plotly
                import plotly.graph_objects as go

                fig = go.Figure()

                # Add station markers
                fig.add_trace(go.Scattergeo(
                    lon=stations['LONGITUDE'],
                    lat=stations['LATITUDE'],
                    text=stations['STATION-ID'],
                    customdata=stations['measurements'],
                    mode='markers',
                    marker=dict(
                        size=stations['measurements'] / stations['measurements'].max() * 30 + 10,
                        color=stations['measurements'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Measurements"),
                        line=dict(width=1, color='white')
                    ),
                    hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<br>Measurements: %{customdata}<extra></extra>'
                ))

                # Calculate map center and zoom
                center_lat = stations['LATITUDE'].mean()
                center_lon = stations['LONGITUDE'].mean()

                fig.update_layout(
                    title="GIFT Network Sampling Stations",
                    geo=dict(
                        projection_type='natural earth',
                        showland=True,
                        landcolor='rgb(220, 212, 185)',  # Beige/tan land
                        coastlinecolor='rgb(80, 80, 80)',  # Dark coastline
                        coastlinewidth=1.5,
                        showocean=True,
                        oceancolor='rgb(180, 210, 230)',  # Light blue ocean
                        showlakes=True,
                        lakecolor='rgb(160, 200, 220)',  # Lake blue
                        showcountries=True,
                        countrycolor='rgb(150, 150, 150)',  # Country borders
                        showrivers=True,
                        rivercolor='rgb(160, 200, 220)',
                        center=dict(lat=center_lat, lon=center_lon),
                        projection_scale=20
                    ),
                    height=600
                )

                st.plotly_chart(fig, use_container_width=True)

                # Station details table
                st.markdown("---")
                st.subheader("📊 Station Details")

                display_stations = stations.copy()
                display_stations.columns = ['Station ID', 'Latitude', 'Longitude', 'Measurements']
                display_stations['Latitude'] = display_stations['Latitude'].round(4)
                display_stations['Longitude'] = display_stations['Longitude'].round(4)
                display_stations = display_stations.sort_values('Measurements', ascending=False)

                st.dataframe(display_stations, use_container_width=True, hide_index=True)

    elif selected_module == "Temporal Analysis":
        temporal.render_temporal_analysis()

    elif selected_module == "Data Quality":
        st.title("✅ Data Quality Control")
        st.markdown("### Outlier Detection & Data Validation")

        # Load data
        from utils.data_loader import get_data_loader
        from scipy import stats
        loader = get_data_loader()
        df = loader.load_data()
        custom_colors = loader.get_custom_palette()

        if df.empty:
            st.error("❌ No data available")
        else:
            # Get available variables (same filtering as Temporal Analysis)
            exclude_vars = loader.get_exclude_vars()
            available_vars = [col for col in loader.get_filtered_numerical_cols(df)
                              if col not in exclude_vars]

            if not available_vars:
                st.error("❌ No variables available for analysis")
            else:
                # Variable selection
                selected_var = st.selectbox(
                    "Select variable for outlier analysis",
                    available_vars,
                    index=0,
                    help="Choose an oceanographic variable to analyze for outliers"
                )

                # Outlier detection method
                method = st.radio(
                    "Outlier Detection Method",
                    ["IQR Method", "Z-Score Method", "Modified Z-Score Method"],
                    help="Select the statistical method for outlier detection"
                )

                # Get data for selected variable
                var_data = df[[selected_var]].dropna()

                if len(var_data) < 3:
                    st.warning("⚠️ Insufficient data for outlier analysis")
                else:
                    # Calculate outliers based on method
                    if method == "IQR Method":
                        Q1 = var_data[selected_var].quantile(0.25)
                        Q3 = var_data[selected_var].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        outliers = var_data[(var_data[selected_var] < lower_bound) | (var_data[selected_var] > upper_bound)]
                        method_desc = f"IQR Method (Q1 - 1.5×IQR, Q3 + 1.5×IQR)"

                    elif method == "Z-Score Method":
                        z_scores = np.abs(stats.zscore(var_data[selected_var]))
                        outliers = var_data[z_scores > 3]
                        lower_bound = var_data[selected_var].mean() - 3 * var_data[selected_var].std()
                        upper_bound = var_data[selected_var].mean() + 3 * var_data[selected_var].std()
                        method_desc = "Z-Score Method (|z| > 3)"

                    else:  # Modified Z-Score Method
                        median = var_data[selected_var].median()
                        mad = np.median(np.abs(var_data[selected_var] - median))
                        modified_z_scores = 0.6745 * (var_data[selected_var] - median) / mad
                        outliers = var_data[np.abs(modified_z_scores) > 3.5]
                        lower_bound = var_data[selected_var].min()
                        upper_bound = var_data[selected_var].max()
                        method_desc = "Modified Z-Score Method (|modified z| > 3.5)"

                    # Display statistics
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Observations", len(var_data))
                    with col2:
                        st.metric("Outliers Detected", len(outliers))
                    with col3:
                        outlier_pct = (len(outliers) / len(var_data)) * 100
                        st.metric("Outlier Percentage", f"{outlier_pct:.2f}%")
                    with col4:
                        clean_data_pct = ((len(var_data) - len(outliers)) / len(var_data)) * 100
                        st.metric("Clean Data", f"{clean_data_pct:.2f}%")

                    st.markdown("---")

                    # Create box plot with outliers highlighted
                    import plotly.graph_objects as go

                    fig = go.Figure()

                    # Add box plot
                    fig.add_trace(go.Box(
                        y=var_data[selected_var],
                        name=selected_var,
                        marker_color=custom_colors[0],
                        boxmean='sd'
                    ))

                    # Add outlier points
                    if len(outliers) > 0:
                        fig.add_trace(go.Scatter(
                            y=outliers[selected_var],
                            x=[selected_var] * len(outliers),
                            mode='markers',
                            name='Outliers',
                            marker=dict(
                                color=custom_colors[4],
                                size=10,
                                symbol='x',
                                line=dict(width=2)
                            )
                        ))

                    fig.update_layout(
                        title=f"Outlier Detection: {selected_var}<br><sub>{method_desc}</sub>",
                        yaxis_title=selected_var,
                        showlegend=True,
                        height=500
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Distribution plot
                    st.markdown("---")
                    st.subheader("📊 Distribution Analysis")

                    fig2 = go.Figure()

                    # Histogram
                    fig2.add_trace(go.Histogram(
                        x=var_data[selected_var],
                        name='Distribution',
                        marker_color=custom_colors[0],
                        opacity=0.7,
                        nbinsx=50
                    ))

                    # Add threshold lines for IQR method
                    if method == "IQR Method":
                        fig2.add_vline(x=lower_bound, line_dash="dash", line_color=custom_colors[4],
                                      annotation_text="Lower Bound")
                        fig2.add_vline(x=upper_bound, line_dash="dash", line_color=custom_colors[4],
                                      annotation_text="Upper Bound")

                    fig2.update_layout(
                        title=f"Distribution of {selected_var}",
                        xaxis_title=selected_var,
                        yaxis_title="Frequency",
                        height=400,
                        showlegend=False
                    )

                    st.plotly_chart(fig2, use_container_width=True)

                    # Outlier details table
                    if len(outliers) > 0:
                        st.markdown("---")
                        st.subheader("🔍 Outlier Details")

                        outlier_details = outliers.copy()
                        outlier_details = outlier_details.reset_index()
                        outlier_details.columns = ['Index', selected_var]
                        outlier_details[selected_var] = outlier_details[selected_var].round(4)

                        st.dataframe(outlier_details.head(20), use_container_width=True, hide_index=True)

                        if len(outliers) > 20:
                            st.info(f"Showing first 20 of {len(outliers)} outliers")

                    # Summary statistics
                    st.markdown("---")
                    st.subheader("📈 Summary Statistics")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**All Data:**")
                        st.write(f"Mean: {var_data[selected_var].mean():.4f}")
                        st.write(f"Median: {var_data[selected_var].median():.4f}")
                        st.write(f"Std Dev: {var_data[selected_var].std():.4f}")
                        st.write(f"Min: {var_data[selected_var].min():.4f}")
                        st.write(f"Max: {var_data[selected_var].max():.4f}")

                    with col2:
                        clean_data = var_data[~var_data.index.isin(outliers.index)]
                        st.markdown("**After Removing Outliers:**")
                        st.write(f"Mean: {clean_data[selected_var].mean():.4f}")
                        st.write(f"Median: {clean_data[selected_var].median():.4f}")
                        st.write(f"Std Dev: {clean_data[selected_var].std():.4f}")
                        st.write(f"Min: {clean_data[selected_var].min():.4f}")
                        st.write(f"Max: {clean_data[selected_var].max():.4f}")

    elif selected_module == "About":
        render_about_page()


# ===== ABOUT PAGE =====
def render_about_page():
    """Render about/documentation page"""
    st.title("ℹ️ About GIFT Intelligence Platform")

    st.markdown("""
    ## 🌊 Overview

    The **GIFT Oceanographic Intelligence Platform** is a comprehensive Business Intelligence
    dashboard designed for marine scientists studying the Strait of Gibraltar.

    ### 🎯 Key Features

    - **GIFT Data Overview**: Comprehensive statistics and KPIs for oceanographic measurements
    - **GIFT Stations Location**: Interactive map showing all sampling station locations
    - **Interactive T-S Diagrams**: Water mass characterization (⭐ Flagship feature)
    - **Temporal Analysis**: Annual trends with linear regression and seasonal patterns
    - **Advanced Analytics**: ML-powered clustering and PCA (under construction)
    - **Quality Control**: Automated outlier detection and validation (under construction)

    ### 📊 Data Source

    **GIFT Network (Gibraltar Fixed Time Series)**
    - 865+ oceanographic measurements
    - 37 oceanographic parameters
    - Multi-year temporal coverage
    - Multiple research vessels

    ### 🏗️ Architecture

    Built on a **4-tier architecture**:

    1. **Presentation Layer** (Streamlit UI)
    2. **Business Logic Layer** (Analytics & ML)
    3. **Data Processing Layer** (Transformations)
    4. **Data Storage Layer** (Data loading & caching)

    ### 🛠️ Technology Stack

    - **Framework**: Streamlit
    - **Visualization**: Plotly, Seaborn, Matplotlib
    - **Analysis**: Pandas, NumPy, SciPy
    - **ML**: Scikit-learn
    - **Geospatial**: Folium, GeoPandas

    ### 👥 Team
    """)

    col1, col2 = st.columns(2)

    with col1:
        # Try to load Emma's photo
        try:
            emma_path = "panel/app/assets/img/Emma.jpeg"
            if not Path(emma_path).exists():
                emma_path = "app/assets/img/Emma.jpeg"
            st.image(emma_path, width=200)
        except:
            pass

        st.markdown("""
        #### 👩🏽‍🔬 GIFT Principal Investigator

        **Dr. I. Emma Huertas**

        Marine Biogeochemistry

        ICMAN-CSIC

        **📧 Contact:** emma.huertas@csic.es
        """)

    with col2:
        # Try to load Su's photo
        try:
            su_path = "panel/app/assets/img/Su.jpeg"
            if not Path(su_path).exists():
                su_path = "app/assets/img/Su.jpeg"
            st.image(su_path, width=200)
        except:
            pass

        st.markdown("""
        #### 👩🏻‍🔬 GIFT Coordinator

        **Dr. Susana Flecha**

        Marine Biogeochemistry & AI

        ICMAN-CSIC

        **📧 Contact:** susana.flecha@csic.es
        """)

    st.markdown("""

    ---

    **Version**: 1.0.0
    **Last Updated**: October 2025
    **License**: MIT License
    """)


def render_footer():
    """Render footer with dashboard creator info (mobile-responsive)"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <p style='font-size: 1.1rem; margin-bottom: 10px;'><strong>Dashboard by:</strong></p>
        <p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 10px;'>Dr. Susana Flecha</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer-badges' style='text-align: center; display: flex; flex-direction: column; align-items: center; gap: 8px;'>
        <a href='https://github.com/susafle' target='_blank'>
            <img src='https://img.shields.io/badge/GitHub-susafle-181717?style=for-the-badge&logo=github' alt='GitHub' style='max-width: 250px; width: 100%;'>
        </a>
        <a href='https://www.linkedin.com/in/susana-flecha-b5b05a44/' target='_blank'>
            <img src='https://img.shields.io/badge/LinkedIn-Susana%20Flecha-0077B5?style=for-the-badge&logo=linkedin' alt='LinkedIn' style='max-width: 250px; width: 100%;'>
        </a>
        <a href='https://orcid.org/0000-0003-2826-5820' target='_blank'>
            <img src='https://img.shields.io/badge/ORCID-0000--0003--2826--5820-A6CE39?style=for-the-badge&logo=orcid' alt='ORCID' style='max-width: 250px; width: 100%;'>
        </a>
    </div>
    """, unsafe_allow_html=True)


# ===== MAIN APPLICATION =====
def main():
    """Main application entry point"""

    # Load custom CSS
    load_custom_css()

    # Render header
    render_header()

    # Render sidebar and get selected module
    selected_module = render_sidebar()

    # Render main content
    render_main_content(selected_module)

    # Render footer
    render_footer()


# ===== RUN APPLICATION =====
if __name__ == "__main__":
    main()
