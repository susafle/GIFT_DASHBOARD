"""
GIFT Oceanographic Intelligence Platform
PRESENTATION LAYER - Executive Dashboard Module

Executive overview with KPIs and high-level metrics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import get_data_loader
from utils.processors import DataProcessor, classify_water_masses
from utils.campaign_analytics import CampaignAnalytics


def render_executive_dashboard():
    """
    Render the Executive Overview Dashboard
    """
    st.title("📊 GIFT Overview")
    st.markdown("### Oceanographic Intelligence Dashboard")
    st.markdown("---")

    # Load data
    loader = get_data_loader()
    df = loader.load_data()

    if df.empty:
        st.error("❌ No data available")
        return

    # Get summary statistics
    summary = loader.get_data_summary(df)

    # === TOP ROW: KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📈 Total Observations",
            value=f"{summary['total_observations']:,}",
            delta="Active"
        )

    with col2:
        st.metric(
            label="🚢 Research Vessels",
            value=summary['vessels'],
            delta=None
        )

    with col3:
        st.metric(
            label="🗓️ Campaigns",
            value=summary['campaigns'],
            delta=None
        )

    with col4:
        st.metric(
            label="📍 Stations",
            value=summary['stations'],
            delta=None
        )

    st.markdown("---")

    # === SECOND ROW: WATER MASS DISTRIBUTION ===
    st.subheader("🌊 Water Mass Distribution")

    col1, col2 = st.columns(2)

    with col1:
        # Add title for the image
        st.markdown('<p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Vertical salinity distribution along longitude</p>', unsafe_allow_html=True)

        # Add vertical space
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

        # Display variable completeness image with right alignment
        try:
            # Try Streamlit Cloud path first, then local path
            img_path = "panel/app/assets/img/Imagen 1.png"
            if not Path(img_path).exists():
                img_path = "app/assets/img/Imagen 1.png"

            st.markdown('<div style="text-align: right; padding-right: 2rem;">', unsafe_allow_html=True)
            st.image(img_path, width=350)
            # Add citation as caption aligned to the right edge of the image
            st.markdown('<p style="font-size: 0.85rem; color: #666; margin-top: 0.2rem; margin-bottom: 0;">(Flecha <i>et al.</i>, 2015)</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.info("Variable completeness visualization not available")
        except Exception as e:
            st.warning(f"Error loading image: {str(e)}")

    with col2:
        # Add title for the chart
        st.markdown('<p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Water Mass Classification</p>', unsafe_allow_html=True)

        # Get custom color palette
        custom_colors = loader.get_custom_palette()

        # Classify water masses
        if all(col in df.columns for col in ['CTD TEMPERATURE (ITS-90)', 'CTD SALINITY (PSS-78)']):
            df_classified = classify_water_masses(df)

            # Count water masses
            wm_counts = df_classified['WATER_MASS'].value_counts()

            # Format labels for two lines
            label_mapping = {
                'Atlantic Inflow': 'Atlantic<br>Inflow',
                'Mediterranean Outflow Water': 'Mediterranean<br>Outflow Water',
                'Atlantic Mediterranean Interface': 'Atlantic Mediterranean<br>Interface'
            }
            formatted_labels = [label_mapping.get(label, label) for label in wm_counts.index]

            # Create pie chart
            fig = go.Figure(data=[
                go.Pie(
                    labels=formatted_labels,
                    values=wm_counts.values,
                    hole=0.4,
                    marker=dict(
                        colors=[custom_colors[0], custom_colors[4], custom_colors[2]]
                    ),
                    textinfo='label+percent',
                    textposition='outside'
                )
            ])

            fig.update_layout(
                height=400,
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Temperature and Salinity data required for water mass classification")

    st.markdown("---")

    # === THIRD ROW: CAMPAIGNS AND VESSELS ANALYSIS ===
    st.subheader("🌊 Oceanographic Campaigns & Vessels Analysis")

    # Get custom color palette
    custom_colors = loader.get_custom_palette()

    # Campaign & Vessel Analysis
    if 'CRUISE-CODE' in df.columns and 'VESSEL' in df.columns:
        # Analyze campaigns and vessels
        campaign_summary = CampaignAnalytics.analyze_campaign_summary(df)
        vessel_summary = CampaignAnalytics.analyze_vessel_usage(df)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🚢 Vessel Usage Distribution")

            # Vessel usage bar chart
            vessel_counts = pd.Series(vessel_summary['vessel_counts'])
            fig = go.Figure(data=[
                go.Bar(
                    x=vessel_counts.index,
                    y=vessel_counts.values,
                    marker=dict(
                        color=custom_colors[:len(vessel_counts)],
                        line=dict(color='white', width=1)
                    ),
                    text=vessel_counts.values,
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Measurements: %{y}<extra></extra>'
                )
            ])

            fig.update_layout(
                title="",
                xaxis_title="Vessel",
                yaxis_title="Number of Measurements",
                height=400,
                plot_bgcolor='white',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 📊 Campaigns per Year")

            # Temporal campaign analysis
            if 'DATE' in df.columns:
                temporal_summary = CampaignAnalytics.analyze_temporal_campaigns(df)

                if 'campaigns_per_year' in temporal_summary:
                    campaigns_year = pd.Series(temporal_summary['campaigns_per_year']).sort_index()

                    fig = go.Figure(data=[
                        go.Scatter(
                            x=campaigns_year.index,
                            y=campaigns_year.values,
                            mode='lines+markers',
                            line=dict(color=custom_colors[0], width=3),
                            marker=dict(
                                size=10,
                                color=custom_colors[3],
                                line=dict(color='white', width=2)
                            ),
                            fill='tozeroy',
                            fillcolor=f'rgba(13, 59, 102, 0.2)',
                            hovertemplate='<b>Year %{x}</b><br>Campaigns: %{y}<extra></extra>'
                        )
                    ])

                    fig.update_layout(
                        title="",
                        xaxis_title="Year",
                        yaxis_title="Number of Campaigns",
                        height=400,
                        plot_bgcolor='white',
                        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)'),
                        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')
                    )

                    st.plotly_chart(fig, use_container_width=True)

        # Third row: Vessel-Year Heatmap
        st.markdown("---")
        st.markdown("#### 🗓️ Campaign Activity: Vessels × Years")

        vessel_year_matrix = CampaignAnalytics.create_vessel_year_heatmap(df)

        if not vessel_year_matrix.empty:
            fig = go.Figure(data=go.Heatmap(
                z=vessel_year_matrix.values,
                x=vessel_year_matrix.columns,
                y=vessel_year_matrix.index,
                colorscale=[[0, 'white'], [0.5, custom_colors[2]], [1, custom_colors[4]]],
                text=vessel_year_matrix.values,
                texttemplate='%{text}',
                textfont=dict(size=10),
                hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Campaigns: %{z}<extra></extra>',
                colorbar=dict(title="Campaigns")
            ))

            fig.update_layout(
                title="Number of Campaigns by Vessel and Year",
                xaxis_title="Year",
                yaxis_title="Vessel",
                height=300,
                plot_bgcolor='white'
            )

            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # === FOURTH ROW: ENVIRONMENTAL KPIs ===
    st.subheader("🌡️ Environmental Parameters")

    col1, col2, col3, col4 = st.columns(4)

    # Temperature
    with col1:
        if 'CTD TEMPERATURE (ITS-90)' in df.columns:
            temp_mean = df['CTD TEMPERATURE (ITS-90)'].mean()
            temp_std = df['CTD TEMPERATURE (ITS-90)'].std()
            st.metric(
                label="Avg. Temperature",
                value=f"{temp_mean:.2f} °C",
                delta=f"±{temp_std:.2f}"
            )
        else:
            st.metric(label="Avg. Temperature", value="N/A")

    # Salinity
    with col2:
        if 'CTD SALINITY (PSS-78)' in df.columns:
            sal_mean = df['CTD SALINITY (PSS-78)'].mean()
            sal_std = df['CTD SALINITY (PSS-78)'].std()
            st.metric(
                label="Avg. Salinity",
                value=f"{sal_mean:.2f}",
                delta=f"±{sal_std:.2f}"
            )
        else:
            st.metric(label="Avg. Salinity", value="N/A")

    # Oxygen
    with col3:
        if 'DISSOLVED OXYGEN' in df.columns:
            oxy_mean = df['DISSOLVED OXYGEN'].mean()
            oxy_min = df['DISSOLVED OXYGEN'].min()
            hypoxic = (df['DISSOLVED OXYGEN'] < 60).sum()
            st.metric(
                label="Avg. Oxygen",
                value=f"{oxy_mean:.1f} µM",
                delta=f"{hypoxic} hypoxic" if hypoxic > 0 else "No hypoxia",
                delta_color="inverse"
            )
        else:
            st.metric(label="Avg. Oxygen", value="N/A")

    # Chlorophyll
    with col4:
        if 'CHLOROPHYLL' in df.columns:
            chl_mean = df['CHLOROPHYLL'].mean()
            chl_max = df['CHLOROPHYLL'].max()
            st.metric(
                label="Avg. Chlorophyll-a",
                value=f"{chl_mean:.3f} µg/L",
                delta=f"Max: {chl_max:.2f}"
            )
        else:
            st.metric(label="Avg. Chlorophyll", value="N/A")

    st.markdown("---")

    # === FOURTH ROW: TEMPORAL COVERAGE ===
    st.subheader("📅 Temporal Coverage")

    if 'DATE' in df.columns and pd.api.types.is_datetime64_any_dtype(df['DATE']):
        col1, col2 = st.columns(2)

        with col1:
            st.info(f"**Start Date:** {summary['date_range']['start'].strftime('%Y-%m-%d')}")
            st.info(f"**End Date:** {summary['date_range']['end'].strftime('%Y-%m-%d')}")

        with col2:
            days_span = (summary['date_range']['end'] - summary['date_range']['start']).days
            st.info(f"**Time Span:** {days_span} days")
            st.info(f"**Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    st.markdown("---")

    # === ALERTS SECTION ===
    st.subheader("⚠️ Alerts & Notifications")

    # Calculate completeness for alerts
    completeness = (df.notna().sum() / len(df) * 100).sort_values(ascending=False)

    # Check for data quality issues
    completeness_threshold = 80
    low_completeness = completeness[completeness < completeness_threshold]

    if len(low_completeness) > 0:
        with st.expander(f"⚠️ {len(low_completeness)} variables with <{completeness_threshold}% completeness"):
            for var, pct in low_completeness.items():
                st.warning(f"**{var}**: {pct:.1f}% complete")

    # Check for hypoxia
    if 'DISSOLVED OXYGEN' in df.columns:
        hypoxic_count = (df['DISSOLVED OXYGEN'] < 60).sum()
        if hypoxic_count > 0:
            st.warning(f"⚠️ **Hypoxia Alert**: {hypoxic_count} measurements below 60 µM oxygen")

    # GHG data availability
    if 'MEAN CH4' in df.columns:
        ch4_available = df['MEAN CH4'].notna().sum()
        if ch4_available < len(df) * 0.1:
            st.info(f"ℹ️ **Limited GHG Data**: Only {ch4_available} methane measurements available ({ch4_available/len(df)*100:.1f}%)")


if __name__ == "__main__":
    render_executive_dashboard()
