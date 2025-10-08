"""
GIFT Oceanographic Intelligence Platform
PRESENTATION LAYER - Physical Oceanography Module

T-S Diagrams and physical oceanography analysis
⭐ FLAGSHIP MODULE
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import get_data_loader
from utils.processors import DataProcessor, classify_water_masses
from utils.analytics import OceanographicAnalytics
from components.charts import OceanographicCharts


def render_physical_oceanography():
    """
    Render the Physical Oceanography Dashboard
    """
    # Create header with side image
    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("🌡️ Physical Oceanography & Biogeochemistry")
        st.markdown("### 🌊 Interactive Temperature-Salinity Diagram")
        st.markdown("""
        <div style="text-align: justify;">
        Explore the physical properties of ocean waters through interactive T-S diagrams,
        water mass classification, and vertical profile analysis. This flagship module provides
        comprehensive insights into the physical dynamics of the Strait of Gibraltar.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        try:
            # Try Streamlit Cloud path first, then local path
            bg_path = "panel/app/assets/img/bg.jpg"
            if not Path(bg_path).exists():
                bg_path = "app/assets/img/bg.jpg"

            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            st.image(bg_path, width=280)
            st.markdown("</div>", unsafe_allow_html=True)
            st.caption("🔬 Biogeochemical Sampling")
        except FileNotFoundError:
            st.info("Background image not available")
        except Exception as e:
            st.warning(f"Error loading image: {str(e)}")

    # Load data
    loader = get_data_loader()
    df = loader.load_data()
    numerical_df = loader.get_numerical_data(df)

    if df.empty:
        st.error("❌ No data available")
        return

    # Define T-S columns
    temp_col = 'CTD TEMPERATURE (ITS-90)'
    sal_col = 'CTD SALINITY (PSS-78)'

    # Check if T-S data exists
    if temp_col not in df.columns or sal_col not in df.columns:
        st.error(f"❌ Required columns not found: {temp_col}, {sal_col}")
        return

    # Sidebar controls
    st.sidebar.markdown("## 🌡️ Physical Oceanography Controls")

    # Select analysis type
    analysis_type = st.sidebar.radio(
        "Select Analysis",
        ["T-S Diagram (Single Variable)", "Multi-Variable T-S Diagrams", "Water Mass Analysis", "Vertical Profiles"]
    )

    st.markdown("---")

    # === T-S DIAGRAM (SINGLE VARIABLE) ===
    if analysis_type == "T-S Diagram (Single Variable)":
        # Get available Z variables
        exclude_vars = loader.get_exclude_vars()
        z_variables = [col for col in loader.get_filtered_numerical_cols(df)
                       if col not in [temp_col, sal_col] and col not in exclude_vars]

        # Select color variable
        color_var = st.selectbox(
            "Select variable for color-coding",
            ['None'] + z_variables,
            help="Choose a variable to color-code the T-S diagram"
        )

        # Select colorscale
        colorscales = loader.get_colorscales()
        colorscale = st.selectbox("Color Scale", colorscales, index=0)

        # Prepare data
        if color_var and color_var != 'None':
            plot_data = DataProcessor.prepare_ts_diagram_data(
                df, temp_col, sal_col, [color_var]
            )
        else:
            plot_data = DataProcessor.prepare_ts_diagram_data(
                df, temp_col, sal_col
            )

        if len(plot_data) == 0:
            st.warning("⚠️ No valid data for T-S diagram")
            return

        # Create T-S diagram
        fig = OceanographicCharts.create_ts_diagram(
            plot_data,
            temp_col=temp_col,
            sal_col=sal_col,
            color_var=color_var if color_var != 'None' else None,
            colorscale=colorscale,
            title=f"T-S Diagram: {color_var}" if color_var != 'None' else "T-S Diagram",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Data Points",
                f"{len(plot_data):,}"
            )

        with col2:
            st.metric(
                "Temp Range",
                f"{plot_data[temp_col].min():.2f} - {plot_data[temp_col].max():.2f} °C"
            )

        with col3:
            st.metric(
                "Sal Range",
                f"{plot_data[sal_col].min():.3f} - {plot_data[sal_col].max():.3f}"
            )

        if color_var and color_var != 'None':
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    f"{color_var} Mean",
                    f"{plot_data[color_var].mean():.3f}"
                )

            with col2:
                st.metric(
                    f"{color_var} Range",
                    f"{plot_data[color_var].min():.3f} - {plot_data[color_var].max():.3f}"
                )

            with col3:
                st.metric(
                    f"{color_var} Std",
                    f"±{plot_data[color_var].std():.3f}"
                )

    # === MULTI-VARIABLE T-S DIAGRAMS ===
    elif analysis_type == "Multi-Variable T-S Diagrams":
        st.subheader("🌊 Multi-Variable T-S Diagram Panel")

        # Get available Z variables
        exclude_vars = loader.get_exclude_vars()
        z_variables = [col for col in loader.get_filtered_numerical_cols(df)
                       if col not in [temp_col, sal_col] and col not in exclude_vars]

        # Select variables
        selected_vars = st.multiselect(
            "Select up to 4 variables for comparison",
            z_variables,
            default=z_variables[:4] if len(z_variables) >= 4 else z_variables,
            max_selections=4
        )

        if len(selected_vars) == 0:
            st.warning("⚠️ Please select at least one variable")
            return

        # Prepare data
        plot_data = DataProcessor.prepare_ts_diagram_data(
            df, temp_col, sal_col, selected_vars
        )

        if len(plot_data) == 0:
            st.warning("⚠️ No valid data for T-S diagrams")
            return

        # Get colorscales
        colorscales = loader.get_colorscales()

        # Create multi-panel T-S diagram
        fig = OceanographicCharts.create_multi_ts_diagrams(
            plot_data,
            temp_col=temp_col,
            sal_col=sal_col,
            color_vars=selected_vars,
            colorscales=colorscales,
            rows=2,
            cols=2,
            height=900,
            width=1400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistics table
        st.markdown("---")
        st.subheader("📊 Variable Statistics")

        stats_data = []
        for var in selected_vars:
            if var in plot_data.columns:
                stats = DataProcessor.calculate_distribution_stats(plot_data, var)
                stats_data.append({
                    'Variable': var,
                    'Mean': f"{stats.get('mean', 0):.3f}",
                    'Std': f"{stats.get('std', 0):.3f}",
                    'Min': f"{stats.get('min', 0):.3f}",
                    'Max': f"{stats.get('max', 0):.3f}",
                    'Count': stats.get('count', 0)
                })

        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

    # === WATER MASS ANALYSIS ===
    elif analysis_type == "Water Mass Analysis":
        st.subheader("🌊 Water Mass Classification & Properties")

        # Classify water masses
        df_classified = classify_water_masses(df)

        # Analyze water mass properties
        wm_analysis = OceanographicAnalytics.analyze_water_mass_properties(df_classified)

        # Display results
        col1, col2, col3 = st.columns(3)

        for idx, (wm_type, wm_data) in enumerate(wm_analysis.items()):
            col = [col1, col2, col3][idx % 3]

            with col:
                st.markdown(f"### {wm_type} Water")
                st.metric(
                    "Observations",
                    f"{wm_data['count']:,}",
                    delta=f"{wm_data['percentage']:.1f}%"
                )

                # Key properties
                props = wm_data['properties']
                if temp_col in props:
                    st.write(f"**Temperature:** {props[temp_col]['mean']:.2f} ± {props[temp_col]['std']:.2f} °C")
                if sal_col in props:
                    st.write(f"**Salinity:** {props[sal_col]['mean']:.3f} ± {props[sal_col]['std']:.3f}")
                if 'DISSOLVED OXYGEN' in props:
                    st.write(f"**Oxygen:** {props['DISSOLVED OXYGEN']['mean']:.1f} ± {props['DISSOLVED OXYGEN']['std']:.1f} µM")

        st.markdown("---")

        # T-S diagram with water mass classification
        st.subheader("T-S Diagram - Color-Coded by Water Mass")

        # Create T-S plot colored by water mass
        import plotly.express as px

        plot_data = df_classified[[temp_col, sal_col, 'WATER_MASS']].dropna()

        fig = px.scatter(
            plot_data,
            x=sal_col,
            y=temp_col,
            color='WATER_MASS',
            color_discrete_map={
                'Atlantic Inflow': '#1e3c72',
                'Mediterranean Outflow Water': '#667eea',
                'Atlantic Mediterranean Interface': '#2a5298'
            },
            labels={
                sal_col: 'Salinity (PSS-78)',
                temp_col: 'Temperature (°C, ITS-90)',
                'WATER_MASS': 'Water Mass'
            },
            title="T-S Diagram - Water Mass Classification",
            height=600
        )

        fig.update_traces(marker=dict(size=8, opacity=0.6, line=dict(width=0.5, color='white')))
        fig.update_layout(
            hovermode='closest',
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.3)'),
            yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.3)')
        )

        st.plotly_chart(fig, use_container_width=True)

    # === VERTICAL PROFILES ===
    elif analysis_type == "Vertical Profiles":
        st.subheader("📏 Vertical Profiles")

        # Check if depth data exists
        depth_col = 'SAMPLING DEPTH'
        if depth_col not in df.columns:
            st.error(f"❌ Depth column '{depth_col}' not found")
            return

        # Select variable for profile
        profile_vars = [temp_col, sal_col, 'DISSOLVED OXYGEN', 'CHLOROPHYLL', 'NITRATE', 'PHOSPHATE']
        available_vars = [v for v in profile_vars if v in df.columns]

        selected_var = st.selectbox("Select variable for vertical profile", available_vars)

        # Prepare data
        profile_data = df[[depth_col, selected_var]].dropna().sort_values(depth_col)

        if len(profile_data) == 0:
            st.warning("⚠️ No valid profile data")
            return

        # Create profile plot
        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=profile_data[selected_var],
            y=profile_data[depth_col],
            mode='markers+lines',
            marker=dict(size=6, color='#1e3c72'),
            line=dict(color='#1e3c72', width=2),
            name=selected_var
        ))

        fig.update_layout(
            title=f"Vertical Profile: {selected_var}",
            xaxis_title=selected_var,
            yaxis_title="Depth (m)",
            yaxis=dict(autorange="reversed"),  # Depth increases downward
            height=600,
            hovermode='closest'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Profile statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Surface Value", f"{profile_data[selected_var].iloc[0]:.3f}")

        with col2:
            st.metric("Bottom Value", f"{profile_data[selected_var].iloc[-1]:.3f}")

        with col3:
            gradient = (profile_data[selected_var].iloc[-1] - profile_data[selected_var].iloc[0]) / \
                       (profile_data[depth_col].iloc[-1] - profile_data[depth_col].iloc[0])
            st.metric("Avg. Gradient", f"{gradient:.5f}/m")


if __name__ == "__main__":
    render_physical_oceanography()
