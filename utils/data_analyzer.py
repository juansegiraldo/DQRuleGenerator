import pandas as pd
import numpy as np
from dateutil.parser import parse
import json

class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_basic_stats(self):
        stats = {
            "row_count": len(self.df),
            "column_count": len(self.df.columns),
            "missing_values": self.df.isnull().sum().to_dict(),
            "column_types": self.df.dtypes.astype(str).to_dict()
        }
        return stats

    def infer_column_types(self):
        column_types = {}
        for column in self.df.columns:
            sample = self.df[column].dropna().head(100)
            if len(sample) == 0:
                column_types[column] = "unknown"
                continue

            # Try to infer if it's a date
            try:
                pd.to_datetime(sample.iloc[0])
                column_types[column] = "date"
                continue
            except:
                pass

            # Check if numeric
            if pd.api.types.is_numeric_dtype(sample):
                if self.df[column].dtype == int or self.df[column].round().equals(self.df[column]):
                    column_types[column] = "integer"
                else:
                    column_types[column] = "float"
            else:
                # Check if boolean
                if set(sample.unique()) <= {'True', 'False', True, False}:
                    column_types[column] = "boolean"
                else:
                    column_types[column] = "string"

        return column_types

    def get_column_correlations(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            return self.df[numeric_cols].corr().to_dict()
        return {}

    def get_data_sample(self):
        return self.df.head(5).to_dict(orient='records')

    def generate_column_profiles(self):
        profiles = {}
        for column in self.df.columns:
            profile = {
                "unique_count": self.df[column].nunique(),
                "missing_count": self.df[column].isnull().sum(),
                "sample_values": self.df[column].dropna().head(5).tolist()
            }
            if pd.api.types.is_numeric_dtype(self.df[column]):
                profile.update({
                    "min": float(self.df[column].min()),
                    "max": float(self.df[column].max()),
                    "mean": float(self.df[column].mean()),
                    "std": float(self.df[column].std())
                })
            profiles[column] = profile
        return profiles
