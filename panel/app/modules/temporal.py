"""
GIFT Oceanographic Intelligence Platform
PRESENTATION LAYER - Temporal Analysis Module

Temporal trends and patterns analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import get_data_loader
from utils.campaign_analytics import TemporalAnalytics


def render_temporal_analysis():
    """
    Render the Temporal Analysis Dashboard
    """
    st.title("📅 Temporal Analysis")
    st.markdown("""
    Analyze temporal evolution of oceanographic variables, identify long-term trends,
    and explore seasonal patterns in the Strait of Gibraltar.
    """)

    # Load data
    loader = get_data_loader()
    df = loader.load_data()
    custom_colors = loader.get_custom_palette()

    if df.empty:
        st.error("❌ No data available")
        return

    # Check if DATE column exists
    if 'DATE' not in df.columns:
        st.error("❌ DATE column not found in dataset")
        return

    # Get available variables (include temp and salinity, exclude only config vars)
    exclude_vars = loader.get_exclude_vars()
    available_vars = [col for col in loader.get_filtered_numerical_cols(df)
                      if col not in exclude_vars]

    if not available_vars:
        st.error("❌ No variables available for analysis")
        return

    # Analysis type selection in sidebar
    st.sidebar.markdown("## 📅 Temporal Analysis Controls")
    analysis_type = st.sidebar.radio(
        "Analysis Type",
        ["Annual Trends with Linear Regression", "Seasonal Patterns", "Combined View"],
        help="Select the type of temporal analysis to perform"
    )

    # === ANNUAL TRENDS ANALYSIS ===
    if analysis_type in ["Annual Trends with Linear Regression", "Combined View"]:
        st.subheader("📈 Annual Trend Analysis")

        # Variable selection (like T-S diagram)
        selected_var = st.selectbox(
            "Select variable for temporal analysis",
            available_vars,
            index=0,
            help="Choose an oceanographic variable to analyze temporal trends"
        )

        # Calculate annual averages
        annual_stats = TemporalAnalytics.calculate_annual_averages(df, selected_var)

        if not annual_stats.empty:
            # Calculate linear trend
            trend_analysis = TemporalAnalytics.calculate_linear_trend(df, selected_var)

            # Create figure
            fig = go.Figure()

            # Add annual means as scatter points
            fig.add_trace(go.Scatter(
                x=annual_stats['YEAR'],
                y=annual_stats['mean'],
                mode='markers+lines',
                name='Annual Mean',
                marker=dict(
                    size=12,
                    color=custom_colors[3],
                    line=dict(color='white', width=2)
                ),
                line=dict(color=custom_colors[0], width=2),
                error_y=dict(
                    type='data',
                    array=annual_stats['std'],
                    visible=True,
                    color=custom_colors[0],
                    thickness=2
                ),
                hovertemplate='<b>Year %{x}</b><br>Mean: %{y:.3f}<br>Std: %{error_y.array:.3f}<extra></extra>'
            ))

            # Add trend line
            if trend_analysis:
                fig.add_trace(go.Scatter(
                    x=trend_analysis['years'],
                    y=trend_analysis['trend_line'],
                    mode='lines',
                    name='Linear Trend',
                    line=dict(
                        color=custom_colors[4],
                        width=3,
                        dash='dash'
                    ),
                    hovertemplate='<b>Trend Line</b><br>Year: %{x}<br>Value: %{y:.3f}<extra></extra>'
                ))

            fig.update_layout(
                title="",
                xaxis_title="Year",
                yaxis_title=selected_var,
                height=500,
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)'),
                hovermode='x unified',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(255,255,255,0.8)"
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # Display trend statistics
            if trend_analysis:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Trend Equation",
                        "",
                        delta=trend_analysis['equation']
                    )

                with col2:
                    direction_emoji = "📈" if trend_analysis['trend_direction'] == 'increasing' else "📉"
                    st.metric(
                        "Trend Direction",
                        f"{direction_emoji} {trend_analysis['trend_direction'].capitalize()}",
                        delta=f"{trend_analysis['annual_change']:.4f}/year"
                    )

                with col3:
                    st.metric(
                        "R² (Fit Quality)",
                        f"{trend_analysis['r_squared']:.4f}",
                        delta="Good fit" if trend_analysis['r_squared'] > 0.7 else "Moderate fit"
                    )

                with col4:
                    significance = "✅ Significant" if trend_analysis['is_significant'] else "⚠️ Not significant"
                    st.metric(
                        "Statistical Significance",
                        significance,
                        delta=f"p-value: {trend_analysis['p_value']:.4f}"
                    )

                # Additional interpretation
                st.markdown("---")
                st.markdown("#### 📊 Interpretation")

                total_change = trend_analysis['total_change']
                years_span = trend_analysis['years'][-1] - trend_analysis['years'][0]

                if trend_analysis['is_significant']:
                    st.success(f"""
                    **Significant Trend Detected** (p < 0.05):
                    - The variable **{selected_var}** shows a statistically significant **{trend_analysis['trend_direction']}** trend
                    - Annual change rate: **{trend_analysis['annual_change']:.4f}** units/year
                    - Total change over {years_span} years: **{total_change:.3f}** units
                    - The linear model explains **{trend_analysis['r_squared']*100:.1f}%** of the variance
                    """)
                else:
                    st.info(f"""
                    **No Significant Trend** (p ≥ 0.05):
                    - The variable **{selected_var}** does not show a statistically significant trend
                    - Observed annual change: **{trend_analysis['annual_change']:.4f}** units/year (not significant)
                    - Natural variability dominates over any potential trend
                    """)

        else:
            st.warning("⚠️ Insufficient data for annual trend analysis")

    # === SEASONAL PATTERNS ANALYSIS ===
    if analysis_type in ["Seasonal Patterns", "Combined View"]:
        st.markdown("---")
        st.subheader("🌿 Seasonal Patterns")

        # Variable selection (like T-S diagram)
        if analysis_type == "Seasonal Patterns":
            # If only seasonal is selected, show selector here
            selected_var = st.selectbox(
                "Select variable for seasonal analysis",
                available_vars,
                index=0,
                help="Choose an oceanographic variable to analyze seasonal patterns"
            )
        # else: selected_var is already defined from Annual Trends section

        # Calculate seasonal statistics
        seasonal_stats = TemporalAnalytics.calculate_seasonal_patterns(df, selected_var)

        if not seasonal_stats.empty:
            # Create polar plot for seasonal patterns
            fig = go.Figure()

            # Add trace for monthly means
            fig.add_trace(go.Scatterpolar(
                r=seasonal_stats['mean'].tolist() + [seasonal_stats['mean'].iloc[0]],  # Close the loop
                theta=seasonal_stats['MONTH_NAME'].tolist() + [seasonal_stats['MONTH_NAME'].iloc[0]],
                mode='lines+markers',
                name='Monthly Mean',
                line=dict(color=custom_colors[0], width=3),
                marker=dict(
                    size=10,
                    color=custom_colors[3],
                    line=dict(color='white', width=2)
                ),
                fill='toself',
                fillcolor=f'rgba(13, 59, 102, 0.2)',
                hovertemplate='<b>%{theta}</b><br>Mean: %{r:.3f}<extra></extra>'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        showgrid=True,
                        gridcolor='rgba(128,128,128,0.2)'
                    ),
                    angularaxis=dict(
                        direction="clockwise",
                        period=12
                    )
                ),
                title="Monthly Average Distribution (Polar View)",
                height=500,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Bar chart for seasonal comparison
            fig2 = go.Figure()

            fig2.add_trace(go.Bar(
                x=seasonal_stats['MONTH_NAME'],
                y=seasonal_stats['mean'],
                marker=dict(
                    color=custom_colors[:len(seasonal_stats)],
                    line=dict(color='white', width=1)
                ),
                error_y=dict(
                    type='data',
                    array=seasonal_stats['std'],
                    visible=True,
                    color='rgba(128,128,128,0.5)',
                    thickness=2
                ),
                text=[f"{v:.2f}" for v in seasonal_stats['mean']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Mean: %{y:.3f}<br>Std: %{error_y.array:.3f}<extra></extra>'
            ))

            fig2.update_layout(
                title="Monthly Averages (Bar Chart)",
                xaxis_title="Month",
                yaxis_title=selected_var,
                height=400,
                plot_bgcolor='white',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')
            )

            st.plotly_chart(fig2, use_container_width=True)

            # Seasonal statistics table
            st.markdown("---")
            st.markdown("#### 📋 Seasonal Statistics")

            display_stats = seasonal_stats[['MONTH_NAME', 'mean', 'std', 'count']].copy()
            display_stats.columns = ['Month', 'Mean', 'Std Dev', 'N Samples']
            display_stats['Mean'] = display_stats['Mean'].round(3)
            display_stats['Std Dev'] = display_stats['Std Dev'].round(3)

            st.dataframe(display_stats, use_container_width=True, hide_index=True)

        else:
            st.warning("⚠️ Insufficient data for seasonal analysis")


if __name__ == "__main__":
    render_temporal_analysis()
