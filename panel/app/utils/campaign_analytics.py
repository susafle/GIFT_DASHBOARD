"""
GIFT Oceanographic Intelligence Platform
BUSINESS LOGIC LAYER - Campaign & Vessel Analytics

Campaign and vessel analysis functions
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats


class CampaignAnalytics:
    """
    Analytics for oceanographic campaigns and vessels
    """

    @staticmethod
    @st.cache_data(ttl=1800)
    def analyze_campaign_summary(df: pd.DataFrame) -> Dict:
        """
        Generate campaign summary statistics

        Args:
            df: Input DataFrame with CRUISE-CODE column

        Returns:
            Dictionary with campaign statistics
        """
        if 'CRUISE-CODE' not in df.columns:
            return {}

        summary = {
            'total_campaigns': df['CRUISE-CODE'].nunique(),
            'total_measurements': len(df),
            'avg_measurements_per_campaign': len(df) / df['CRUISE-CODE'].nunique(),
            'campaign_distribution': df['CRUISE-CODE'].value_counts().to_dict(),
            'top_10_campaigns': df['CRUISE-CODE'].value_counts().head(10).to_dict()
        }

        return summary

    @staticmethod
    @st.cache_data(ttl=1800)
    def analyze_vessel_usage(df: pd.DataFrame) -> Dict:
        """
        Analyze vessel usage patterns

        Args:
            df: Input DataFrame with VESSEL column

        Returns:
            Dictionary with vessel statistics
        """
        if 'VESSEL' not in df.columns:
            return {}

        vessel_counts = df['VESSEL'].value_counts()
        vessel_percentages = (vessel_counts / len(df) * 100).round(1)

        summary = {
            'total_vessels': df['VESSEL'].nunique(),
            'vessel_counts': vessel_counts.to_dict(),
            'vessel_percentages': vessel_percentages.to_dict(),
            'dominant_vessel': vessel_counts.index[0],
            'dominant_vessel_pct': vessel_percentages.iloc[0]
        }

        return summary

    @staticmethod
    @st.cache_data(ttl=1800)
    def analyze_temporal_campaigns(df: pd.DataFrame, date_col: str = 'DATE') -> Dict:
        """
        Analyze temporal distribution of campaigns

        Args:
            df: Input DataFrame with date column
            date_col: Name of date column

        Returns:
            Dictionary with temporal statistics
        """
        if date_col not in df.columns or 'CRUISE-CODE' not in df.columns:
            return {}

        # Ensure date column is datetime
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df_clean = df.dropna(subset=[date_col])

        # Extract temporal features
        df_clean['YEAR'] = df_clean[date_col].dt.year
        df_clean['MONTH'] = df_clean[date_col].dt.month

        # Campaigns per year
        campaigns_per_year = df_clean.groupby('YEAR')['CRUISE-CODE'].nunique()

        # Measurements per year
        measurements_per_year = df_clean.groupby('YEAR').size()

        summary = {
            'date_range': {
                'start': df_clean[date_col].min(),
                'end': df_clean[date_col].max()
            },
            'years_active': int(campaigns_per_year.index.max() - campaigns_per_year.index.min() + 1),
            'campaigns_per_year': campaigns_per_year.to_dict(),
            'measurements_per_year': measurements_per_year.to_dict(),
            'avg_campaigns_per_year': float(campaigns_per_year.mean()),
            'most_active_year': int(campaigns_per_year.idxmax()),
            'campaigns_in_most_active_year': int(campaigns_per_year.max())
        }

        return summary

    @staticmethod
    @st.cache_data(ttl=1800)
    def analyze_vessel_campaigns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create cross-analysis of vessels and campaigns

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with vessel-campaign statistics
        """
        if 'VESSEL' not in df.columns or 'CRUISE-CODE' not in df.columns:
            return pd.DataFrame()

        # Create summary
        vessel_stats = []
        for vessel in df['VESSEL'].unique():
            vessel_data = df[df['VESSEL'] == vessel]
            stats_dict = {
                'Vessel': vessel,
                'Campaigns': vessel_data['CRUISE-CODE'].nunique(),
                'Measurements': len(vessel_data),
                'Avg_Measurements_per_Campaign': len(vessel_data) / vessel_data['CRUISE-CODE'].nunique()
            }

            if 'YEAR' in vessel_data.columns:
                stats_dict['Years_Active'] = vessel_data['YEAR'].nunique()
                stats_dict['First_Year'] = int(vessel_data['YEAR'].min())
                stats_dict['Last_Year'] = int(vessel_data['YEAR'].max())

            vessel_stats.append(stats_dict)

        return pd.DataFrame(vessel_stats).sort_values('Measurements', ascending=False)

    @staticmethod
    @st.cache_data(ttl=1800)
    def create_vessel_year_heatmap(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create vessel-year campaigns matrix for heatmap

        Args:
            df: Input DataFrame

        Returns:
            Pivot table with vessels vs years
        """
        if 'VESSEL' not in df.columns or 'CRUISE-CODE' not in df.columns:
            return pd.DataFrame()

        if 'YEAR' not in df.columns and 'DATE' in df.columns:
            df['YEAR'] = pd.to_datetime(df['DATE'], errors='coerce').dt.year

        if 'YEAR' not in df.columns:
            return pd.DataFrame()

        # Create pivot table
        vessel_year = df.groupby(['VESSEL', 'YEAR'])['CRUISE-CODE'].nunique().unstack(fill_value=0)

        return vessel_year


class TemporalAnalytics:
    """
    Analytics for temporal trends and patterns
    """

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_annual_averages(
        df: pd.DataFrame,
        variable: str,
        date_col: str = 'DATE'
    ) -> pd.DataFrame:
        """
        Calculate annual averages for a variable

        Args:
            df: Input DataFrame
            variable: Variable to analyze
            date_col: Date column name

        Returns:
            DataFrame with annual statistics
        """
        if variable not in df.columns or date_col not in df.columns:
            return pd.DataFrame()

        # Ensure date column is datetime
        df_clean = df[[date_col, variable]].copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
        df_clean = df_clean.dropna()

        # Extract year
        df_clean['YEAR'] = df_clean[date_col].dt.year

        # Calculate annual statistics
        annual_stats = df_clean.groupby('YEAR')[variable].agg([
            ('mean', 'mean'),
            ('std', 'std'),
            ('count', 'count'),
            ('min', 'min'),
            ('max', 'max')
        ]).reset_index()

        return annual_stats

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_linear_trend(
        df: pd.DataFrame,
        variable: str,
        date_col: str = 'DATE'
    ) -> Dict:
        """
        Calculate linear trend for a variable over time

        Args:
            df: Input DataFrame
            variable: Variable to analyze
            date_col: Date column name

        Returns:
            Dictionary with trend statistics and equation
        """
        annual_stats = TemporalAnalytics.calculate_annual_averages(df, variable, date_col)

        if annual_stats.empty:
            return {}

        # Perform linear regression
        x = annual_stats['YEAR'].values
        y = annual_stats['mean'].values

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # Create equation string
        sign = '+' if intercept >= 0 else ''
        equation = f"y = {slope:.4f}x {sign}{intercept:.4f}"

        # Calculate trend line
        trend_line = slope * x + intercept

        result = {
            'slope': float(slope),
            'intercept': float(intercept),
            'r_squared': float(r_value ** 2),
            'p_value': float(p_value),
            'std_err': float(std_err),
            'equation': equation,
            'trend_line': trend_line.tolist(),
            'years': x.tolist(),
            'values': y.tolist(),
            'is_significant': p_value < 0.05,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing',
            'annual_change': float(slope),
            'total_change': float(slope * (x[-1] - x[0]))
        }

        return result

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_seasonal_patterns(
        df: pd.DataFrame,
        variable: str,
        date_col: str = 'DATE'
    ) -> pd.DataFrame:
        """
        Calculate seasonal patterns (monthly averages)

        Args:
            df: Input DataFrame
            variable: Variable to analyze
            date_col: Date column name

        Returns:
            DataFrame with seasonal statistics
        """
        if variable not in df.columns or date_col not in df.columns:
            return pd.DataFrame()

        # Ensure date column is datetime
        df_clean = df[[date_col, variable]].copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
        df_clean = df_clean.dropna()

        # Extract month
        df_clean['MONTH'] = df_clean[date_col].dt.month
        df_clean['MONTH_NAME'] = df_clean[date_col].dt.month_name()

        # Calculate monthly statistics
        monthly_stats = df_clean.groupby(['MONTH', 'MONTH_NAME'])[variable].agg([
            ('mean', 'mean'),
            ('std', 'std'),
            ('count', 'count')
        ]).reset_index()

        return monthly_stats.sort_values('MONTH')
