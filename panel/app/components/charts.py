"""
GIFT Oceanographic Intelligence Platform
PRESENTATION LAYER - Chart Components

This module contains reusable chart components using Plotly.
Implements visualization components for the presentation layer.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional, Dict


class OceanographicCharts:
    """
    Reusable chart components for oceanographic data
    """

    @staticmethod
    def create_ts_diagram(
        df: pd.DataFrame,
        temp_col: str = 'CTD TEMPERATURE (ITS-90)',
        sal_col: str = 'CTD SALINITY (PSS-78)',
        color_var: Optional[str] = None,
        colorscale: str = 'Viridis',
        title: str = 'Temperature-Salinity Diagram',
        height: int = 600
    ) -> go.Figure:
        """
        Create an interactive T-S diagram

        Args:
            df: DataFrame with T-S data
            temp_col: Temperature column name
            sal_col: Salinity column name
            color_var: Optional variable for color-coding points
            colorscale: Plotly colorscale name
            title: Chart title
            height: Chart height in pixels

        Returns:
            Plotly Figure object
        """
        # Filter valid data
        required_cols = [temp_col, sal_col]
        if color_var:
            required_cols.append(color_var)

        df_plot = df[required_cols].dropna()

        if len(df_plot) == 0:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No valid data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            return fig

        # Create scatter plot
        if color_var:
            fig = px.scatter(
                df_plot,
                x=sal_col,
                y=temp_col,
                color=color_var,
                color_continuous_scale=colorscale,
                labels={
                    sal_col: 'Salinity (PSS-78)',
                    temp_col: 'Temperature (°C, ITS-90)',
                    color_var: color_var
                },
                title=title,
                hover_data={
                    sal_col: ':.3f',
                    temp_col: ':.3f',
                    color_var: ':.3f'
                }
            )
        else:
            fig = px.scatter(
                df_plot,
                x=sal_col,
                y=temp_col,
                labels={
                    sal_col: 'Salinity (PSS-78)',
                    temp_col: 'Temperature (°C, ITS-90)'
                },
                title=title
            )

        # Update layout
        fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0.5, color='white')))
        fig.update_layout(
            height=height,
            showlegend=True,
            hovermode='closest',
            xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.3)'),
            yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.3)'),
            plot_bgcolor='white'
        )

        return fig

    @staticmethod
    def create_multi_ts_diagrams(
        df: pd.DataFrame,
        temp_col: str,
        sal_col: str,
        color_vars: List[str],
        colorscales: List[str],
        rows: int = 2,
        cols: int = 2,
        height: int = 900,
        width: int = 1400
    ) -> go.Figure:
        """
        Create multiple T-S diagrams in subplots

        Args:
            df: DataFrame with data
            temp_col: Temperature column
            sal_col: Salinity column
            color_vars: List of variables for color-coding
            colorscales: List of colorscales for each subplot
            rows: Number of subplot rows
            cols: Number of subplot columns
            height: Total figure height
            width: Total figure width

        Returns:
            Plotly Figure with subplots
        """
        # Create subplot titles
        subplot_titles = [f'T-S: {var}' for var in color_vars[:rows*cols]]

        # Create figure with subplots
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            horizontal_spacing=0.12,
            vertical_spacing=0.12
        )

        # Add each T-S diagram
        for idx, color_var in enumerate(color_vars[:rows*cols]):
            row = (idx // cols) + 1
            col = (idx % cols) + 1

            # Filter valid data for this variable
            required_cols = [temp_col, sal_col, color_var]
            df_plot = df[required_cols].dropna()

            if len(df_plot) == 0:
                continue

            # Select colorscale
            colorscale = colorscales[idx % len(colorscales)]

            # Create scatter trace
            trace = go.Scatter(
                x=df_plot[sal_col],
                y=df_plot[temp_col],
                mode='markers',
                marker=dict(
                    size=6,
                    color=df_plot[color_var],
                    colorscale=colorscale,
                    opacity=0.7,
                    line=dict(width=0.5, color='white'),
                    colorbar=dict(
                        title=color_var,
                        x=1.02 + (col-1) * 0.05,
                        len=0.4,
                        y=0.75 if row == 1 else 0.25,
                        thickness=12
                    ) if idx < 2 else None,
                    showscale=idx < 2
                ),
                name=color_var,
                showlegend=False,
                hovertemplate=(
                    f'<b>{color_var}</b><br>' +
                    f'Salinity: %{{x:.3f}} PSS-78<br>' +
                    f'Temperature: %{{y:.3f}} °C<br>' +
                    f'{color_var}: %{{marker.color:.3f}}<br>' +
                    '<extra></extra>'
                )
            )

            fig.add_trace(trace, row=row, col=col)

        # Update axes
        fig.update_xaxes(
            title_text="Salinity (PSS-78)",
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(128,128,128,0.3)'
        )
        fig.update_yaxes(
            title_text="Temperature (°C)",
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(128,128,128,0.3)'
        )

        # Update layout
        fig.update_layout(
            height=height,
            width=width,
            showlegend=False,
            title_text="🌊 Temperature-Salinity Diagrams - GIFT Network",
            title_x=0.5,
            margin=dict(r=200, t=100, b=80, l=80)
        )

        return fig

    @staticmethod
    def create_correlation_heatmap(
        corr_matrix: pd.DataFrame,
        p_values: Optional[pd.DataFrame] = None,
        title: str = 'Correlation Matrix',
        height: int = 700,
        colorscale: str = 'RdBu'
    ) -> go.Figure:
        """
        Create interactive correlation heatmap

        Args:
            corr_matrix: Correlation matrix DataFrame
            p_values: Optional p-value matrix
            title: Chart title
            height: Chart height
            colorscale: Color scale name

        Returns:
            Plotly Figure
        """
        # Prepare hover text
        if p_values is not None:
            hover_text = []
            for i, row in enumerate(corr_matrix.index):
                hover_text.append([])
                for j, col in enumerate(corr_matrix.columns):
                    corr_val = corr_matrix.iloc[i, j]
                    p_val = p_values.iloc[i, j]
                    hover_text[i].append(
                        f'{row} vs {col}<br>' +
                        f'r = {corr_val:.3f}<br>' +
                        f'p = {p_val:.4f}<br>' +
                        f'{"Significant" if p_val < 0.05 else "Not significant"}'
                    )
        else:
            hover_text = corr_matrix.values

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale=colorscale,
            zmid=0,
            zmin=-1,
            zmax=1,
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            colorbar=dict(title='Correlation')
        ))

        fig.update_layout(
            title=title,
            height=height,
            xaxis=dict(tickangle=-45),
            yaxis=dict(tickangle=0)
        )

        return fig

    @staticmethod
    def create_boxplot(
        df: pd.DataFrame,
        column: str,
        title: Optional[str] = None,
        height: int = 500
    ) -> go.Figure:
        """
        Create interactive box plot

        Args:
            df: DataFrame
            column: Column to plot
            title: Chart title
            height: Chart height

        Returns:
            Plotly Figure
        """
        if title is None:
            title = f'Distribution: {column}'

        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df[column].dropna(),
            name=column,
            boxmean='sd',
            marker_color='#1e3c72'
        ))

        fig.update_layout(
            title=title,
            yaxis_title=column,
            height=height,
            showlegend=False
        )

        return fig

    @staticmethod
    def create_time_series(
        df: pd.DataFrame,
        date_col: str,
        value_col: str,
        title: Optional[str] = None,
        height: int = 500
    ) -> go.Figure:
        """
        Create time series plot

        Args:
            df: DataFrame
            date_col: Date column
            value_col: Value column
            title: Chart title
            height: Chart height

        Returns:
            Plotly Figure
        """
        if title is None:
            title = f'{value_col} over time'

        df_plot = df[[date_col, value_col]].dropna().sort_values(date_col)

        fig = px.line(
            df_plot,
            x=date_col,
            y=value_col,
            title=title,
            labels={date_col: 'Date', value_col: value_col}
        )

        fig.update_traces(line_color='#1e3c72')
        fig.update_layout(
            height=height,
            hovermode='x unified',
            xaxis=dict(rangeslider=dict(visible=True))
        )

        return fig

    @staticmethod
    def create_histogram(
        df: pd.DataFrame,
        column: str,
        bins: int = 30,
        title: Optional[str] = None,
        height: int = 500
    ) -> go.Figure:
        """
        Create histogram with distribution curve

        Args:
            df: DataFrame
            column: Column to plot
            bins: Number of bins
            title: Chart title
            height: Chart height

        Returns:
            Plotly Figure
        """
        if title is None:
            title = f'Distribution: {column}'

        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=title,
            labels={column: column},
            marginal='box'
        )

        fig.update_layout(height=height, showlegend=False)

        return fig

    @staticmethod
    def create_3d_scatter(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        z_col: str,
        color_col: Optional[str] = None,
        title: str = '3D Scatter Plot',
        height: int = 700
    ) -> go.Figure:
        """
        Create 3D scatter plot

        Args:
            df: DataFrame
            x_col, y_col, z_col: Column names for axes
            color_col: Optional column for color
            title: Chart title
            height: Chart height

        Returns:
            Plotly Figure
        """
        fig = px.scatter_3d(
            df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col if color_col else None,
            title=title,
            labels={x_col: x_col, y_col: y_col, z_col: z_col}
        )

        fig.update_layout(
            height=height,
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            )
        )

        return fig


# Convenience function
def plot_ts_diagram(df: pd.DataFrame, color_var: Optional[str] = None) -> go.Figure:
    """Quick T-S diagram (convenience function)"""
    return OceanographicCharts.create_ts_diagram(df, color_var=color_var)
