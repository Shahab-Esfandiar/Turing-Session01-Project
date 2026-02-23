# app/hierarchical_cleaner.py
import pandas as pd
import numpy as np
import re
import os
from core.logger import logger

class HierarchicalCleaner:
    PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    MULTI_SEPARATORS = ["/", ",", "،", ";", "؛", " و "]

    def __init__(self, file_path):
        self.file_path = file_path

    def get_clean_dataframe(self):
        logger.info(f"Cleaning hierarchical structure: {os.path.basename(self.file_path)}")
        
        # Determine engine based on extension
        if self.file_path.endswith(".csv"):
            raw_df = pd.read_csv(self.file_path, header=None, dtype=str)
        else:
            # openpyxl is for .xlsx, xlrd is for .xls
            engine = 'openpyxl' if self.file_path.endswith('.xlsx') else 'xlrd'
            raw_df = pd.read_excel(self.file_path, header=None, dtype=str, engine=engine)

        # Use .map() to avoid the FutureWarning from .applymap()
        raw_df = raw_df.map(self._normalize_value)

        start_idx = self._detect_start(raw_df)
        
        # Process Headers
        headers_raw = raw_df.iloc[:start_idx].ffill(axis=1).ffill(axis=0)
        resolved_headers = []
        for col in headers_raw.columns:
            levels = headers_raw[col].dropna().astype(str).unique()
            clean_levels = [l.strip() for l in levels if l.strip().lower() not in ['nan', 'none', '']]
            resolved_headers.append(" | ".join(clean_levels) if clean_levels else f"Column_{col}")

        # Extract Data
        df = raw_df.iloc[start_idx:].reset_index(drop=True)
        df.columns = resolved_headers
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

        # Semantic Explosion
        df = self._explode_multivalues(df)
        
        # Final Type Inference
        return self._infer_types(df)

    def _normalize_value(self, val):
        if pd.isna(val): return val
        s = str(val).strip().translate(self.PERSIAN_DIGITS).replace(",", "")
        try:
            # Check if it's a pure number before converting
            if re.match(r'^-?\d+(\.\d+)?$', s):
                return float(s)
            return s
        except:
            return s

    def _detect_start(self, df):
        for i, row in df.iterrows():
            # Count cells that are already numeric or look like numbers
            numeric_count = sum(1 for v in row if isinstance(v, (int, float)) or str(v).replace('.','',1).isdigit())
            if numeric_count > (len(row) * 0.4):
                return i
        return 0

    def _explode_multivalues(self, df):
        for col in df.columns:
            # Check if column values contain separators in the first few rows
            sample = df[col].dropna().astype(str).head(20)
            pattern = "|".join(map(re.escape, self.MULTI_SEPARATORS))
            if any(re.search(pattern, val) for val in sample):
                df[col] = df[col].astype(str).apply(
                    lambda x: [i.strip() for i in re.split(pattern, x)] if pd.notna(x) else x
                )
                df = df.explode(col)
        return df

    def _infer_types(self, df):
        for col in df.columns:
            # Ensure we are not trying to numeric-convert a column of lists
            if df[col].apply(lambda x: isinstance(x, list)).any():
                continue
                
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notnull().mean() > 0.8:
                df[col] = converted
        return df