"""
GIFT Oceanographic Intelligence Platform
DATA STORAGE LAYER - Data Loader Module

This module handles all data loading, caching, and basic validation.
Implements the lowest layer of the 4-tier architecture.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Optional, Dict, List
import yaml
import requests
from io import StringIO


class DataLoader:
    """
    Data Storage Layer - Handles data loading and caching
    """

    def __init__(self, config_path: str = "app/config/config.yaml"):
        """Initialize data loader with configuration"""
        self.config = self._load_config(config_path)
        self.data_path = self._resolve_data_path()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Return default config if file not found
            return {
                'data': {'raw_data': '../data/GIFT_database_prepared.csv'},
                'exclude_vars': []
            }

    def _get_dropbox_url(self) -> Optional[str]:
        """
        Extract Dropbox URL from secrets configuration.
        Supports both flat and nested formats.
        Returns: Complete Dropbox URL or None if not configured
        """
        try:
            if not hasattr(st, 'secrets'):
                return None

            base = ''
            key = ''

            # Try flat format first (dropbox_base, dropbox_key)
            if 'dropbox_base' in st.secrets and 'dropbox_key' in st.secrets:
                base = st.secrets.get('dropbox_base', '')
                key = st.secrets.get('dropbox_key', '')
            # Try nested format ([dropbox] section)
            elif 'dropbox' in st.secrets:
                base = st.secrets['dropbox'].get('base', '')
                key = st.secrets['dropbox'].get('key', '')

            if base and key:
                return f"{base}?rlkey={key}&dl=1"

        except Exception:
            pass

        return None

    def _resolve_data_path(self) -> Path:
        """Resolve the absolute path to the data file"""
        raw_path = self.config.get('data', {}).get('raw_data',
                                                     '../data/GIFT_database_prepared.csv')

        # Try multiple possible paths
        possible_paths = [
            Path(raw_path),
            Path(__file__).parent.parent.parent / 'data' / 'GIFT_database_prepared.csv',
            Path(__file__).parent.parent.parent.parent / 'data' / 'GIFT_database_prepared.csv',
        ]

        for path in possible_paths:
            if path.exists():
                return path

        # If no path found, return the first one (will raise error on load)
        return possible_paths[0]

    @st.cache_data(ttl=3600, show_spinner="Loading oceanographic data...")
    def load_data(_self) -> pd.DataFrame:
        """
        Load the main dataset with caching
        Returns: DataFrame with all GIFT Network data
        """
        try:
            df = None

            # First, try to load from Dropbox URL in secrets
            try:
                dropbox_url = _self._get_dropbox_url()

                if dropbox_url:
                    response = requests.get(dropbox_url, timeout=30)
                    response.raise_for_status()
                    df = pd.read_csv(StringIO(response.text))
            except Exception as dropbox_error:
                # Silently fall back to local file
                pass

            # Fallback to local file if Dropbox failed or not configured
            if df is None:
                df = pd.read_csv(_self.data_path)

            # Basic data type conversions
            if 'DATE' in df.columns:
                df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

            # Add computed columns
            if 'DATE' in df.columns:
                df['YEAR'] = df['DATE'].dt.year
                df['MONTH'] = df['DATE'].dt.month
                df['MONTH_NAME'] = df['DATE'].dt.month_name()

            return df

        except FileNotFoundError:
            st.error(f"❌ Data file not found at: {_self.data_path}")
            st.error("📋 **Troubleshooting:**")
            st.error("1. Ensure Dropbox secrets are configured in Streamlit Cloud Settings → Secrets")
            st.error("2. For local development, place GIFT_database_prepared.csv in panel/data/")
            st.code("""
[dropbox]
base = "https://www.dropbox.com/scl/fi/u3c6w7u710rp6a42bm1a1/GIFT_database_prepared.csv"
key = "6dwgu16a4ygajsjtx1mff4664"
            """, language="toml")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_numerical_data(_self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract numerical columns only
        Returns: DataFrame with numerical columns
        """
        exclude_vars = _self.config.get('exclude_vars', [])

        # Select numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Remove excluded variables
        filtered_cols = [col for col in numerical_cols if col not in exclude_vars]

        return df[filtered_cols]

    @st.cache_data(ttl=3600)
    def get_filtered_numerical_cols(_self, df: pd.DataFrame) -> List[str]:
        """
        Get list of filtered numerical column names
        Returns: List of column names
        """
        exclude_vars = _self.config.get('exclude_vars', [])
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        return [col for col in numerical_cols if col not in exclude_vars]

    def get_data_summary(_self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for the dataset
        Returns: Dictionary with summary information
        """
        return {
            'total_observations': len(df),
            'total_variables': len(df.columns),
            'numerical_variables': len(df.select_dtypes(include=[np.number]).columns),
            'date_range': {
                'start': df['DATE'].min() if 'DATE' in df.columns else None,
                'end': df['DATE'].max() if 'DATE' in df.columns else None
            },
            'vessels': df['VESSEL'].nunique() if 'VESSEL' in df.columns else 0,
            'campaigns': df['CRUISE-CODE'].nunique() if 'CRUISE-CODE' in df.columns else 0,
            'stations': df['STATION-ID'].nunique() if 'STATION-ID' in df.columns else 0,
        }

    def get_completeness(_self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate data completeness percentage for each column
        Returns: Series with completeness percentage (0-100)
        """
        completeness = (1 - df.isnull().sum() / len(df)) * 100
        return completeness.sort_values(ascending=False)

    def get_oceanographic_vars(_self) -> Dict[str, Dict]:
        """
        Get oceanographic variable definitions from config
        Returns: Dictionary with variable metadata
        """
        return _self.config.get('oceanography', {})

    def get_exclude_vars(_self) -> List[str]:
        """Get list of variables to exclude from analysis"""
        return _self.config.get('exclude_vars', [])

    def get_colorscales(_self) -> List[str]:
        """Get list of colorscales for T-S diagrams only"""
        return _self.config.get('colorscales', ['Viridis', 'Plasma', 'Inferno'])

    def get_custom_palette(_self) -> List[str]:
        """Get custom color palette for all plots except T-S diagrams"""
        return _self.config.get('custom_palette', ['#0d3b66', '#faf0ca', '#f4d35e', '#ee964b', '#f95738', '#8c1c13'])


# Singleton instance
@st.cache_resource
def get_data_loader():
    """Get or create DataLoader singleton instance"""
    return DataLoader()


# Convenience functions for easy access
def load_gift_data() -> pd.DataFrame:
    """Load GIFT Network data (convenience function)"""
    loader = get_data_loader()
    return loader.load_data()


def get_numerical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Get numerical data only (convenience function)"""
    loader = get_data_loader()
    return loader.get_numerical_data(df)


def get_data_summary(df: pd.DataFrame) -> Dict:
    """Get data summary (convenience function)"""
    loader = get_data_loader()
    return loader.get_data_summary(df)
