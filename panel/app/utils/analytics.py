"""
GIFT Oceanographic Intelligence Platform
BUSINESS LOGIC LAYER - Analytics Module

This module contains the business logic and analytical functions.
Implements the business logic layer of the 4-tier architecture.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import streamlit as st
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class OceanographicAnalytics:
    """
    Business Logic Layer - Oceanographic analysis and calculations
    """

    @staticmethod
    @st.cache_data(ttl=1800)
    def analyze_water_mass_properties(
        df: pd.DataFrame,
        water_mass_col: str = 'WATER_MASS'
    ) -> Dict[str, Dict]:
        """
        Analyze properties for each water mass type

        Args:
            df: DataFrame with water mass classifications
            water_mass_col: Column containing water mass classifications

        Returns:
            Dictionary with statistics for each water mass
        """
        if water_mass_col not in df.columns:
            return {}

        results = {}
        numerical_cols = df.select_dtypes(include=[np.number]).columns

        for water_mass in df[water_mass_col].unique():
            if pd.isna(water_mass):
                continue

            subset = df[df[water_mass_col] == water_mass]
            results[water_mass] = {
                'count': len(subset),
                'percentage': (len(subset) / len(df)) * 100,
                'properties': {}
            }

            # Calculate mean properties
            for col in numerical_cols:
                if col in subset.columns:
                    results[water_mass]['properties'][col] = {
                        'mean': subset[col].mean(),
                        'std': subset[col].std(),
                        'median': subset[col].median()
                    }

        return results

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_nutrient_ratios(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate nutrient stoichiometric ratios (N:P, Si:N, etc.)

        Args:
            df: DataFrame with nutrient data

        Returns:
            DataFrame with added ratio columns
        """
        df = df.copy()

        # N:P ratio (Redfield ratio ≈ 16)
        if 'NITRATE' in df.columns and 'PHOSPHATE' in df.columns:
            df['N_P_RATIO'] = df['NITRATE'] / df['PHOSPHATE'].replace(0, np.nan)

        # Si:N ratio
        if 'SILICATE' in df.columns and 'NITRATE' in df.columns:
            df['SI_N_RATIO'] = df['SILICATE'] / df['NITRATE'].replace(0, np.nan)

        # Si:P ratio
        if 'SILICATE' in df.columns and 'PHOSPHATE' in df.columns:
            df['SI_P_RATIO'] = df['SILICATE'] / df['PHOSPHATE'].replace(0, np.nan)

        return df

    @staticmethod
    @st.cache_data(ttl=1800)
    def identify_hypoxic_zones(
        df: pd.DataFrame,
        oxygen_col: str = 'DISSOLVED OXYGEN',
        threshold: float = 60.0
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Identify hypoxic zones (low oxygen areas)

        Args:
            df: DataFrame with oxygen data
            oxygen_col: Column name for oxygen concentration
            threshold: Hypoxia threshold in µM (default: 60)

        Returns:
            Tuple of (DataFrame with hypoxia flag, statistics dictionary)
        """
        df = df.copy()

        if oxygen_col not in df.columns:
            return df, {}

        df['IS_HYPOXIC'] = df[oxygen_col] < threshold

        stats_dict = {
            'hypoxic_count': df['IS_HYPOXIC'].sum(),
            'hypoxic_percentage': (df['IS_HYPOXIC'].sum() / len(df)) * 100,
            'mean_oxygen': df[oxygen_col].mean(),
            'min_oxygen': df[oxygen_col].min(),
            'threshold': threshold
        }

        return df, stats_dict

    @staticmethod
    @st.cache_data(ttl=1800)
    def perform_pca_analysis(
        df: pd.DataFrame,
        n_components: int = 3,
        scale: bool = True
    ) -> Tuple[np.ndarray, PCA, pd.DataFrame]:
        """
        Perform Principal Component Analysis

        Args:
            df: DataFrame with numerical variables
            n_components: Number of principal components
            scale: Whether to standardize variables

        Returns:
            Tuple of (transformed data, PCA model, loadings DataFrame)
        """
        # Remove rows with any NaN
        df_clean = df.dropna()

        if len(df_clean) < n_components:
            return np.array([]), None, pd.DataFrame()

        # Standardize if requested
        if scale:
            scaler = StandardScaler()
            X = scaler.fit_transform(df_clean)
        else:
            X = df_clean.values

        # Perform PCA
        pca = PCA(n_components=n_components)
        X_transformed = pca.fit_transform(X)

        # Create loadings DataFrame
        loadings = pd.DataFrame(
            pca.components_.T,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=df_clean.columns
        )

        return X_transformed, pca, loadings

    @staticmethod
    @st.cache_data(ttl=1800)
    def perform_kmeans_clustering(
        df: pd.DataFrame,
        n_clusters: int = 3,
        scale: bool = True,
        random_state: int = 42
    ) -> Tuple[np.ndarray, KMeans, float]:
        """
        Perform K-means clustering

        Args:
            df: DataFrame with numerical variables
            n_clusters: Number of clusters
            scale: Whether to standardize variables
            random_state: Random seed for reproducibility

        Returns:
            Tuple of (cluster labels, KMeans model, silhouette score)
        """
        from sklearn.metrics import silhouette_score

        # Remove rows with any NaN
        df_clean = df.dropna()

        if len(df_clean) < n_clusters:
            return np.array([]), None, 0.0

        # Standardize if requested
        if scale:
            scaler = StandardScaler()
            X = scaler.fit_transform(df_clean)
        else:
            X = df_clean.values

        # Perform K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(X)

        # Calculate silhouette score
        if len(np.unique(labels)) > 1:
            silhouette = silhouette_score(X, labels)
        else:
            silhouette = 0.0

        return labels, kmeans, silhouette

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_seasonal_statistics(
        df: pd.DataFrame,
        value_col: str,
        month_col: str = 'MONTH'
    ) -> pd.DataFrame:
        """
        Calculate seasonal statistics for a variable

        Args:
            df: Input DataFrame
            value_col: Column to analyze
            month_col: Month column for grouping

        Returns:
            DataFrame with seasonal statistics
        """
        if value_col not in df.columns or month_col not in df.columns:
            return pd.DataFrame()

        seasonal_stats = df.groupby(month_col)[value_col].agg([
            ('mean', 'mean'),
            ('median', 'median'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max'),
            ('count', 'count')
        ]).reset_index()

        return seasonal_stats

    @staticmethod
    @st.cache_data(ttl=1800)
    def detect_anomalies_zscore(
        df: pd.DataFrame,
        column: str,
        threshold: float = 3.0
    ) -> Tuple[pd.Series, Dict]:
        """
        Detect anomalies using Z-score method

        Args:
            df: Input DataFrame
            column: Column to analyze
            threshold: Z-score threshold for anomaly (default: 3.0)

        Returns:
            Tuple of (boolean Series marking anomalies, statistics dict)
        """
        if column not in df.columns:
            return pd.Series([False] * len(df)), {}

        data = df[column].dropna()

        if len(data) == 0:
            return pd.Series([False] * len(df)), {}

        # Calculate Z-scores
        z_scores = np.abs(stats.zscore(data))
        anomalies = pd.Series([False] * len(df), index=df.index)
        anomalies.loc[data.index] = z_scores > threshold

        stats_dict = {
            'n_anomalies': anomalies.sum(),
            'anomaly_percentage': (anomalies.sum() / len(df)) * 100,
            'threshold': threshold,
            'mean': data.mean(),
            'std': data.std()
        }

        return anomalies, stats_dict

    @staticmethod
    @st.cache_data(ttl=1800)
    def calculate_vertical_gradients(
        df: pd.DataFrame,
        depth_col: str = 'SAMPLING DEPTH',
        variable_col: str = 'CTD TEMPERATURE (ITS-90)'
    ) -> pd.DataFrame:
        """
        Calculate vertical gradients for a variable

        Args:
            df: Input DataFrame
            depth_col: Depth column name
            variable_col: Variable to calculate gradient

        Returns:
            DataFrame with gradients
        """
        if depth_col not in df.columns or variable_col not in df.columns:
            return pd.DataFrame()

        # Sort by depth
        df_sorted = df[[depth_col, variable_col]].dropna().sort_values(depth_col)

        if len(df_sorted) < 2:
            return pd.DataFrame()

        # Calculate gradient
        gradients = df_sorted[variable_col].diff() / df_sorted[depth_col].diff()
        df_sorted['GRADIENT'] = gradients

        return df_sorted

    @staticmethod
    def calculate_stratification_index(
        df: pd.DataFrame,
        depth_col: str = 'SAMPLING DEPTH',
        density_col: str = 'DENSITY (sq) (sigma-theta)'
    ) -> float:
        """
        Calculate stratification index (simplified)

        Args:
            df: Input DataFrame
            depth_col: Depth column
            density_col: Density column

        Returns:
            Stratification index value
        """
        if depth_col not in df.columns or density_col not in df.columns:
            return 0.0

        df_sorted = df[[depth_col, density_col]].dropna().sort_values(depth_col)

        if len(df_sorted) < 2:
            return 0.0

        # Simple stratification: difference between surface and bottom density
        surface_density = df_sorted[density_col].iloc[0]
        bottom_density = df_sorted[density_col].iloc[-1]

        stratification = bottom_density - surface_density

        return stratification
# Convenience functions
def analyze_water_masses(df: pd.DataFrame) -> Dict:
    """Analyze water mass properties (convenience function)"""
    return OceanographicAnalytics.analyze_water_mass_properties(df)


def perform_pca(df: pd.DataFrame, n_components: int = 3):
    """Perform PCA (convenience function)"""
    return OceanographicAnalytics.perform_pca_analysis(df, n_components)


def cluster_data(df: pd.DataFrame, n_clusters: int = 3):
    """Perform K-means clustering (convenience function)"""
    return OceanographicAnalytics.perform_kmeans_clustering(df, n_clusters)
