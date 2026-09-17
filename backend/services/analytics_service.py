"""
Role-Protected Administrator Analytics Service for MoSPI STATWISE Platform (Prompt P).
Features:
- Aggregate organization analytics: onboarded officials, active learners,
  learning hours, completion rate, domain scores, pre/post improvement.
- Top gaps broken down by department and designation.
- Provider usage (iGOT vs NSSTA/TPAC).
- Recommendation acceptance rates.
- Privacy Protection / Small Cohort Masking: Any group with fewer than 3 learners
  is masked (< 3) to prevent re-identification of civil servants.
- CSV and printable export generation.
"""

import csv
import io
from typing import Dict, Any, List, Optional
from datetime import datetime


DEPARTMENTS_DATA = [
    {"department": "Field Operations Division (FOD)", "officials": 3420, "avg_hours": 18.5, "completion_pct": 74, "top_gap": "Survey Sampling & Multipliers"},
    {"department": "National Accounts Division (NAD)", "officials": 1280, "avg_hours": 24.2, "completion_pct": 82, "top_gap": "SNA 2008 & FISIM"},
    {"department": "Price Statistics Division (PSD)", "officials": 940, "avg_hours": 16.0, "completion_pct": 78, "top_gap": "CPI Elementary Aggregation"},
    {"department": "Economic Statistics Division (ESD)", "officials": 1150, "avg_hours": 21.4, "completion_pct": 71, "top_gap": "IIP Item Replacement"},
    {"department": "Data Informatics & Innovation (DIID)", "officials": 860, "avg_hours": 29.8, "completion_pct": 86, "top_gap": "DPDP Microdata Anonymization"},
    {"department": "State DES - Sikkim Cell", "officials": 2, "avg_hours": 14.0, "completion_pct": 50, "top_gap": "CAPI Field Operations"}  # Small cohort for testing masking!
]

ROLE_BREAKDOWN = [
    {"role": "Junior Statistical Officer (JSO)", "officials": 4210, "avg_score": 62, "pass_rate": 74, "top_gap": "Python Data Wrangling"},
    {"role": "Senior Statistical Officer (SSO)", "officials": 2450, "avg_score": 71, "pass_rate": 81, "top_gap": "GIS Spatial Mapping"},
    {"role": "Data Analyst (MoSPI DIID)", "officials": 620, "avg_score": 83, "pass_rate": 92, "top_gap": "Machine Learning for Anomaly Detection"},
    {"role": "Indian Statistical Service (ISS)", "officials": 715, "avg_score": 88, "pass_rate": 95, "top_gap": "Executive Statistical Leadership"},
    {"role": "State Statistical Directorate - Lakshadweep", "officials": 1, "avg_score": 58, "pass_rate": 50, "top_gap": "Survey Sampling"}  # Small cohort!
]


class AdminAnalyticsService:
    def __init__(self):
        pass

    def get_organization_metrics(
        self,
        department_filter: Optional[str] = None,
        role_filter: Optional[str] = None,
        domain_filter: Optional[str] = None,
        mask_small_cohorts: bool = True
    ) -> Dict[str, Any]:
        """
        Computes aggregate metrics with small cohort masking (< 3) (Prompt P).
        """
        # Filter departments
        dept_list = list(DEPARTMENTS_DATA)
        if department_filter and department_filter != "All":
            dept_list = [d for d in dept_list if d["department"] == department_filter]

        # Apply privacy masking for small cohorts
        processed_depts = []
        for d in dept_list:
            item = dict(d)
            if mask_small_cohorts and item["officials"] < 3:
                item["officials_display"] = "< 3 (Masked for Privacy)"
                item["is_masked"] = True
            else:
                item["officials_display"] = str(item["officials"])
                item["is_masked"] = False
            processed_depts.append(item)

        # Filter roles
        role_list = list(ROLE_BREAKDOWN)
        if role_filter and role_filter != "All":
            role_list = [r for r in role_list if role_filter in r["role"]]

        processed_roles = []
        for r in role_list:
            item = dict(r)
            if mask_small_cohorts and item["officials"] < 3:
                item["officials_display"] = "< 3 (Masked for Privacy)"
                item["is_masked"] = True
            else:
                item["officials_display"] = str(item["officials"])
                item["is_masked"] = False
            processed_roles.append(item)

        total_officials = sum(d["officials"] for d in DEPARTMENTS_DATA)

        return {
            "kpis": {
                "total_officials": total_officials,
                "active_learners": 6840,
                "total_learning_hours": 142580,
                "overall_completion_rate_pct": 74.5,
                "avg_mastery_pct": 68.2,
                "pre_to_post_improvement_pct": 28.4,
                "recommendation_acceptance_pct": 69.1,
                "quiz_pass_rate_pct": 79.4
            },
            "domain_scores": [
                {"domain": "Statistical Methodology", "current_avg": 66, "target": 85, "growth": "+18%"},
                {"domain": "Technical & Automation", "current_avg": 54, "target": 80, "growth": "+22%"},
                {"domain": "Digital Governance & Privacy", "current_avg": 73, "target": 85, "growth": "+14%"},
                {"domain": "Behavioural & Leadership", "current_avg": 71, "target": 85, "growth": "+9%"}
            ],
            "provider_usage": [
                {"provider": "iGOT Karmayogi (Self-Paced Digital)", "enrolments": 14920, "share_pct": 68.4},
                {"provider": "NSSTA Greater Noida (In-Person/Residential)", "enrolments": 4810, "share_pct": 22.1},
                {"provider": "Blended Virtual Lab & Workshops", "enrolments": 2080, "share_pct": 9.5}
            ],
            "departments_breakdown": processed_depts,
            "roles_breakdown": processed_roles,
            "privacy_notice": "In compliance with MoSPI Data Confidentiality and DPDP Act 2023, cohorts with fewer than 3 individuals are masked to prevent personal re-identification."
        }

    def generate_csv_report(self) -> str:
        """Generates CSV export of organization analytics (Prompt P)."""
        metrics = self.get_organization_metrics(mask_small_cohorts=True)
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["=== MoSPI STATWISE Platform - Cadre Training & Competency Audit Report ==="])
        writer.writerow(["Generated At", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")])
        writer.writerow([])

        writer.writerow(["Key Performance Indicators", "Value"])
        for k, v in metrics["kpis"].items():
            writer.writerow([k.replace("_", " ").title(), v])
        writer.writerow([])

        writer.writerow(["Department Breakdown", "Officials", "Avg Hours", "Completion %", "Top Competency Gap"])
        for d in metrics["departments_breakdown"]:
            writer.writerow([d["department"], d["officials_display"], d["avg_hours"], f"{d['completion_pct']}%", d["top_gap"]])
        writer.writerow([])

        writer.writerow(["Role Breakdown", "Officials", "Avg Baseline Score", "Quiz Pass Rate %", "Top Competency Gap"])
        for r in metrics["roles_breakdown"]:
            writer.writerow([r["role"], r["officials_display"], r["avg_score"], f"{r['pass_rate']}%", r["top_gap"]])
        writer.writerow([])

        writer.writerow(["Domain Competency Progress", "Current Avg Score", "Target Benchmark", "Improvement"])
        for dom in metrics["domain_scores"]:
            writer.writerow([dom["domain"], dom["current_avg"], dom["target"], dom["growth"]])

        return output.getvalue()


# Singleton analytics service
admin_analytics_service = AdminAnalyticsService()
