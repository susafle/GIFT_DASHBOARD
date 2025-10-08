"""
GIFT Oceanographic Intelligence Platform
DATA PROCESSING LAYER - Data Processors Module

This module handles data transformations, filtering, and preprocessing.
Implements the data processing layer of the 4-tier architecture.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional, Dict
import streamlit as st
from scipy import stats


class DataProcessor:
    """
    Data Processing Layer - Handles data transformations and filtering
    """

    @staticmethod
    @st.cache_data(ttl=1800)
    def filter_valid_data(df: pd.DataFrame, required_cols: List[str]) -> pd.DataFrame:
        """
        Filter data to include only rows with valid (non-NaN) values in required columns

        Args:
            df: Input DataFrame
            required_cols: List of column names that must have valid values

        Returns:
            Filtered DataFrame
        """
        # Check which columns exist
        existing_cols = [col for col in required_cols if col in df.columns]

        if not existing_cols:
            return pd.DataFrame()

        return df[existing_cols].dropna(subset=existing_cols)

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_water_mass_classification(
        df: pd.DataFrame,
        temp_col: str = 'CTD TEMPERATURE (ITS-90)',
        sal_col: str = 'CTD SALINITY (PSS-78)'
    ) -> pd.DataFrame:
        """
        Classify water masses based on temperature and salinity

        Classification logic for Strait of Gibraltar:
        - Atlantic Inflow: Salinity < 37
        - Mediterranean Outflow Water: Salinity > 37.5
        - Atlantic Mediterranean Interface: 37 <= Salinity <= 37.5

        Args:
            df: DataFrame with T-S data
            temp_col: Temperature column name
            sal_col: Salinity column name

        Returns:
            DataFrame with added 'WATER_MASS' column
        """
        df = df.copy()

        if temp_col not in df.columns or sal_col not in df.columns:
            df['WATER_MASS'] = 'Unknown'
            return df

        # Define salinity thresholds for Strait of Gibraltar
        atlantic_threshold = 37.0
        mediterranean_threshold = 37.5

        # Classify water masses based on salinity
        conditions = [
            df[sal_col] < atlantic_threshold,
            df[sal_col] > mediterranean_threshold
        ]
        choices = ['Atlantic Inflow', 'Mediterranean Outflow Water']

        df['WATER_MASS'] = np.select(conditions, choices, default='Atlantic Mediterranean Interface')

        return df

    @staticmethod
    @st.cache_data(ttl=1800)
    def detect_outliers_iqr(df: pd.DataFrame, column: str) -> Tuple[pd.Series, Dict]:
        """
        Detect outliers using Interquartile Range (IQR) method

        Args:
            df: Input DataFrame
            column: Column name to analyze

        Returns:
            Tuple of (boolean Series marking outliers, dictionary with statistics)
        """
        if column not in df.columns:
            return pd.Series([False] * len(df)), {}

        data = df[column].dropna()

        if len(data) == 0:
            return pd.Series([False] * len(df)), {}

        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

        stats_dict = {
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'n_outliers': outliers.sum(),
            'outlier_percentage': (outliers.sum() / len(df)) * 100
        }

        return outliers, stats_dict

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_distribution_stats(df: pd.DataFrame, column: str) -> Dict:
        """
        Calculate distribution statistics for a variable

        Args:
            df: Input DataFrame
            column: Column name to analyze

        Returns:
            Dictionary with distribution statistics
        """
        if column not in df.columns:
            return {}

        data = df[column].dropna()

        if len(data) == 0:
            return {}

        return {
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'q1': data.quantile(0.25),
            'q3': data.quantile(0.75),
            'skewness': data.skew(),
            'kurtosis': data.kurtosis(),
            'count': len(data),
            'missing': df[column].isnull().sum(),
            'completeness': (len(data) / len(df)) * 100
        }

    @staticmethod
    @st.cache_data(ttl=1800)
    def aggregate_by_temporal(
        df: pd.DataFrame,
        value_col: str,
        temporal_col: str = 'MONTH',
        agg_func: str = 'mean'
    ) -> pd.DataFrame:
        """
        Aggregate data by temporal grouping (month/year)

        Args:
            df: Input DataFrame
            value_col: Column to aggregate
            temporal_col: Temporal column for grouping
            agg_func: Aggregation function ('mean', 'median', 'sum')

        Returns:
            Aggregated DataFrame
        """
        if value_col not in df.columns or temporal_col not in df.columns:
            return pd.DataFrame()

        if agg_func == 'mean':
            result = df.groupby(temporal_col)[value_col].mean()
        elif agg_func == 'median':
            result = df.groupby(temporal_col)[value_col].median()
        elif agg_func == 'sum':
            result = df.groupby(temporal_col)[value_col].sum()
        else:
            result = df.groupby(temporal_col)[value_col].mean()

        return result.reset_index()

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_correlation_matrix(
        df: pd.DataFrame,
        method: str = 'spearman',
        min_periods: int = 30
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate correlation matrix with p-values

        Args:
            df: Input DataFrame (numerical columns only)
            method: Correlation method ('spearman' or 'pearson')
            min_periods: Minimum number of observations required

        Returns:
            Tuple of (correlation matrix, p-value matrix)
        """
        from scipy.stats import spearmanr, pearsonr

        # Filter columns with sufficient data
        valid_cols = []
        for col in df.columns:
            if df[col].notna().sum() >= min_periods:
                valid_cols.append(col)

        df_filtered = df[valid_cols]

        if len(valid_cols) < 2:
            return pd.DataFrame(), pd.DataFrame()

        if method == 'spearman':
            corr_matrix, p_values = spearmanr(df_filtered, nan_policy='omit')
            corr_df = pd.DataFrame(corr_matrix, index=valid_cols, columns=valid_cols)
            p_df = pd.DataFrame(p_values, index=valid_cols, columns=valid_cols)
        else:
            corr_df = df_filtered.corr(method='pearson')
            # Calculate p-values for Pearson
            p_df = pd.DataFrame(np.zeros_like(corr_df), index=corr_df.index, columns=corr_df.columns)
            for i, col1 in enumerate(corr_df.columns):
                for j, col2 in enumerate(corr_df.columns):
                    if i != j:
                        valid_data = df_filtered[[col1, col2]].dropna()
                        if len(valid_data) > 3:
                            _, p_val = pearsonr(valid_data[col1], valid_data[col2])
                            p_df.iloc[i, j] = p_val

        return corr_df, p_df

    @staticmethod
    @st.cache_data(ttl=1800)
    def prepare_ts_diagram_data(
        df: pd.DataFrame,
        temp_col: str = 'CTD TEMPERATURE (ITS-90)',
        sal_col: str = 'CTD SALINITY (PSS-78)',
        additional_vars: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Prepare data for T-S diagrams

        Args:
            df: Input DataFrame
            temp_col: Temperature column name
            sal_col: Salinity column name
            additional_vars: Additional variables to include

        Returns:
            Filtered DataFrame with valid T-S data
        """
        required_cols = [temp_col, sal_col]

        if additional_vars:
            required_cols.extend([v for v in additional_vars if v in df.columns])

        return DataProcessor.filter_valid_data(df, required_cols)

    @staticmethod
    def calculate_density(
        temperature: pd.Series,
        salinity: pd.Series,
        pressure: Optional[pd.Series] = None
    ) -> pd.Series:
        """
        Calculate seawater density (simplified equation of state)
        Uses UNESCO 1983 polynomial approximation

        Args:
            temperature: Temperature in °C
            salinity: Salinity in PSS-78
            pressure: Pressure in dbar (optional, assumes 0 if not provided)

        Returns:
            Density in kg/m³
        """
        if pressure is None:
            pressure = pd.Series([0] * len(temperature))

        # Simplified density calculation (sigma-t approximation)
        # For more accurate calculations, use GSW library
        a0 = 999.842594
        a1 = 6.793952e-2
        a2 = -9.095290e-3
        a3 = 1.001685e-4
        a4 = -1.120083e-6
        a5 = 6.536332e-9

        b0 = 8.24493e-1
        b1 = -4.0899e-3
        b2 = 7.6438e-5
        b3 = -8.2467e-7
        b4 = 5.3875e-9

        c0 = -5.72466e-3
        c1 = 1.0227e-4
        c2 = -1.6546e-6

        d0 = 4.8314e-4

        # Calculate density
        t = temperature
        s = salinity

        rho_w = (a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5)
        rho_0 = rho_w + (b0 + b1*t + b2*t**2 + b3*t**3 + b4*t**4)*s + \
                (c0 + c1*t + c2*t**2)*s**1.5 + d0*s**2

        return rho_0


# Convenience functions
def filter_valid_data(df: pd.DataFrame, required_cols: List[str]) -> pd.DataFrame:
    """Filter valid data (convenience function)"""
    return DataProcessor.filter_valid_data(df, required_cols)


def classify_water_masses(df: pd.DataFrame) -> pd.DataFrame:
    """Classify water masses (convenience function)"""
    return DataProcessor.calculate_water_mass_classification(df)


def calculate_stats(df: pd.DataFrame, column: str) -> Dict:
    """Calculate distribution statistics (convenience function)"""
    return DataProcessor.calculate_distribution_stats(df, column)
