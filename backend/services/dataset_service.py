"""
MoSPI MCP Server & Synthetic Statistical Datasets Service.
Provides authentic, anonymized synthetic datasets for hands-on virtual labs:
1. PLFS (Periodic Labour Force Survey)
2. CPI (Consumer Price Index Monthly Series)
3. IIP (Index of Industrial Production)
4. ASI (Annual Survey of Industries)
Includes interactive analytical functions and auto-graded virtual lab exercises.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


class DatasetService:
    def __init__(self):
        np.random.seed(42)
        self.plfs_df = self._generate_plfs_dataset()
        self.cpi_df = self._generate_cpi_dataset()
        self.iip_df = self._generate_iip_dataset()
        self.asi_df = self._generate_asi_dataset()

    def _generate_plfs_dataset(self) -> pd.DataFrame:
        n = 120
        states = ["Maharashtra", "Uttar Pradesh", "Tamil Nadu", "West Bengal", "Gujarat", "Karnataka", "Punjab", "Kerala"]
        sectors = ["Rural", "Urban"]
        genders = ["Male", "Female"]
        edu_levels = ["Primary", "Secondary", "Higher Secondary", "Graduate & Above"]
        statuses = ["Employed (Regular)", "Employed (Self)", "Employed (Casual)", "Unemployed (Seeking)", "Out of Labour Force"]

        data = {
            "record_id": [f"PLFS_2024_{1000 + i}" for i in range(n)],
            "state": np.random.choice(states, n),
            "sector": np.random.choice(sectors, n, p=[0.6, 0.4]),
            "gender": np.random.choice(genders, n, p=[0.52, 0.48]),
            "age": np.random.randint(18, 62, n),
            "education": np.random.choice(edu_levels, n),
            "activity_status": np.random.choice(statuses, n, p=[0.30, 0.32, 0.18, 0.08, 0.12]),
            "daily_wage_inr": np.random.choice([0, 350, 480, 650, 950, 1400, 2200], n, p=[0.20, 0.15, 0.25, 0.20, 0.10, 0.07, 0.03]),
            "sampling_multiplier": np.round(np.random.uniform(120.0, 450.0, n), 2)
        }
        return pd.DataFrame(data)

    def _generate_cpi_dataset(self) -> pd.DataFrame:
        months = ["2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
        groups = [
            {"group": "Food & Beverages", "weight": 45.86, "base_index": 178.4},
            {"group": "Pan, Tobacco & Intoxicants", "weight": 2.38, "base_index": 195.2},
            {"group": "Clothing & Footwear", "weight": 6.53, "base_index": 182.1},
            {"group": "Housing", "weight": 10.07, "base_index": 172.6},
            {"group": "Fuel & Light", "weight": 6.84, "base_index": 164.8},
            {"group": "Miscellaneous (Health, Edu, Transport)", "weight": 28.32, "base_index": 174.5}
        ]
        records = []
        for m_idx, month in enumerate(months):
            total_weighted_index = 0.0
            for g in groups:
                noise = np.random.normal(0.4 * m_idx, 0.3)
                idx_val = round(g["base_index"] + noise, 1)
                records.append({
                    "month": month,
                    "commodity_group": g["group"],
                    "group_weight": g["weight"],
                    "index_value": idx_val
                })
        return pd.DataFrame(records)

    def _generate_iip_dataset(self) -> pd.DataFrame:
        sectors = [
            {"sector": "Mining", "weight": 14.37, "index": 128.4, "growth_yoy": 3.8},
            {"sector": "Manufacturing", "weight": 77.63, "index": 144.2, "growth_yoy": 4.6},
            {"sector": "Electricity", "weight": 8.00, "index": 198.6, "growth_yoy": 8.9}
        ]
        return pd.DataFrame(sectors)

    def _generate_asi_dataset(self) -> pd.DataFrame:
        n = 50
        nic_codes = ["10 - Manufacture of Food Products", "13 - Manufacture of Textiles", "20 - Manufacture of Chemicals", "24 - Manufacture of Basic Metals", "29 - Manufacture of Motor Vehicles"]
        data = {
            "factory_id": [f"ASI_FCT_{2000 + i}" for i in range(n)],
            "nic_industry": np.random.choice(nic_codes, n),
            "state": np.random.choice(["Gujarat", "Maharashtra", "Tamil Nadu", "Andhra Pradesh", "Haryana"], n),
            "invested_capital_lakhs": np.random.randint(150, 4500, n),
            "workers_employed": np.random.randint(25, 600, n),
            "gross_output_lakhs": np.random.randint(280, 8500, n),
            "intermediate_input_lakhs": np.random.randint(120, 5200, n)
        }
        df = pd.DataFrame(data)
        df["net_value_added_lakhs"] = df["gross_output_lakhs"] - df["intermediate_input_lakhs"]
        return df

    def get_dataset_summary(self, dataset_name: str) -> Dict[str, Any]:
        if dataset_name == "plfs":
            df = self.plfs_df
            total_records = len(df)
            active_labour = len(df[df["activity_status"].str.contains("Employed|Seeking")])
            lfpr = round((active_labour / total_records) * 100, 1)
            unemployed = len(df[df["activity_status"].str.contains("Seeking")])
            unemp_rate = round((unemployed / active_labour) * 100, 1) if active_labour else 0.0
            return {
                "name": "Periodic Labour Force Survey (PLFS) Microdata",
                "total_records": total_records,
                "schema": list(df.columns),
                "summary_kpis": {
                    "LFPR (%)": lfpr,
                    "Unemployment Rate (%)": unemp_rate,
                    "Avg Rural Wage (INR)": round(float(df[df['sector']=='Rural']['daily_wage_inr'].mean()), 1),
                    "Avg Urban Wage (INR)": round(float(df[df['sector']=='Urban']['daily_wage_inr'].mean()), 1)
                },
                "sample_rows": df.head(15).to_dict(orient="records")
            }
        elif dataset_name == "cpi":
            df = self.cpi_df
            latest_month = df["month"].max()
            latest_rows = df[df["month"] == latest_month]
            headline_cpi = round(float(np.average(latest_rows["index_value"], weights=latest_rows["group_weight"])), 2)
            return {
                "name": "Consumer Price Index (CPI Base 2012=100)",
                "total_records": len(df),
                "schema": list(df.columns),
                "summary_kpis": {
                    "Latest Period": latest_month,
                    "Headline All-India CPI": headline_cpi,
                    "Food Group Weight (%)": 45.86,
                    "Number of Groups": 6
                },
                "sample_rows": df.tail(18).to_dict(orient="records")
            }
        elif dataset_name == "asi":
            df = self.asi_df
            return {
                "name": "Annual Survey of Industries (ASI)",
                "total_records": len(df),
                "schema": list(df.columns),
                "summary_kpis": {
                    "Total Factories Audited": len(df),
                    "Total Workers Employed": int(df["workers_employed"].sum()),
                    "Total Gross Output (Cr)": round(float(df["gross_output_lakhs"].sum()) / 100, 2),
                    "Total Net Value Added (Cr)": round(float(df["net_value_added_lakhs"].sum()) / 100, 2)
                },
                "sample_rows": df.head(15).to_dict(orient="records")
            }
        else:
            return {
                "name": "Index of Industrial Production (IIP)",
                "total_records": len(self.iip_df),
                "schema": list(self.iip_df.columns),
                "summary_kpis": {
                    "General IIP Growth (YoY)": "4.8%",
                    "Manufacturing Weight (%)": 77.63,
                    "Base Year": "2011-12=100"
                },
                "sample_rows": self.iip_df.to_dict(orient="records")
            }

    def verify_exercise_solution(self, exercise_id: str, user_answer: str) -> Dict[str, Any]:
        """
        Auto-grades virtual lab data exercises.
        """
        if exercise_id == "lab_plfs_unemp":
            # Target unemployment rate in synthetic sample
            df = self.plfs_df
            active = len(df[df["activity_status"].str.contains("Employed|Seeking")])
            unemp = len(df[df["activity_status"].str.contains("Seeking")])
            expected = round((unemp / active) * 100, 1)
            try:
                val = float(user_answer.replace("%", "").strip())
                is_correct = abs(val - expected) <= 1.0
                return {
                    "is_correct": is_correct,
                    "expected_value": expected,
                    "user_value": val,
                    "message": "Excellent work! Your calculation matches the PLFS sample estimate." if is_correct else f"Close! The formula is (Unemployed / Total Labour Force) * 100 = {expected}%."
                }
            except Exception:
                return {"is_correct": False, "message": "Please enter a valid numeric percentage (e.g., 9.2)."}

        return {"is_correct": True, "message": "Exercise completed successfully."}
