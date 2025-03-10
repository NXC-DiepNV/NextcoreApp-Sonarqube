from typing import List

import pandas as pd
class DataFrameCore:
    @staticmethod
    def convert_column_to_numeric(df, column_name):
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)
        return df

    @staticmethod
    def convert_column_to_date(df, column_name: str, format_date: str = '%Y/%m/%d'):
        df[column_name] = pd.to_datetime(df[column_name], format=format_date)
        return df

    @staticmethod
    def convert_columns_to_numeric(df, columns: List[str]):
        for column in columns:
            # Convert column to numeric and replace errors with 0
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        return df