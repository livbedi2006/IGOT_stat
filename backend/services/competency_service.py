"""
Competency Framework & Analytics Engine for MoSPI Official Statistics.
Covers 4 core domains:
1. Statistical Methodology & NSSO Operations
2. Technical & Data Science (Python, R, SQL, GIS)
3. Digital Governance, Privacy (DPDP Act 2023) & Standards (SDMX)
4. Behavioural, Leadership & Official Communication
"""

from typing import Dict, Any, List


# Official statistical competency catalogue
COMPETENCY_REGISTRY = {
    # --- Statistical Domain ---
    "survey_design": {
        "id": "survey_design",
        "name": "Survey Design & Sampling Frames",
        "domain": "Statistical",
        "criticality": 0.95,
        "description": "Formulation of sampling frames, stratification, allocation and NSS multi-stage sampling."
    },
    "survey_sampling": {
        "id": "survey_sampling",
        "name": "Sample Estimation & Variance Calculation",
        "domain": "Statistical",
        "criticality": 0.95,
        "description": "Horvitz-Thompson estimation, multiplier calculation, calibration weighting and sampling error."
    },
    "national_accounts": {
        "id": "national_accounts",
        "name": "National Accounts Statistics (NAS)",
        "domain": "Statistical",
        "criticality": 0.85,
        "description": "System of National Accounts (SNA 2008), GVA compilation, supply-use tables and deflators."
    },
    "price_indices": {
        "id": "price_indices",
        "name": "Price Indices (CPI & WPI)",
        "domain": "Statistical",
        "criticality": 0.88,
        "description": "Laspeyres index, item weighting baskets, rural/urban aggregation and core inflation."
    },
    "industrial_stats": {
        "id": "industrial_stats",
        "name": "Industrial Statistics (ASI & IIP)",
        "domain": "Statistical",
        "criticality": 0.82,
        "description": "Annual Survey of Industries methodology, NIC classification and IIP production weights."
    },

    # --- Technical Domain ---
    "python_data_analysis": {
        "id": "python_data_analysis",
        "name": "Python for Data Analysis",
        "domain": "Technical",
        "criticality": 0.90,
        "description": "Pandas, NumPy, automated data wrangling, outlier detection and statistical validation."
    },
    "r_econometrics": {
        "id": "r_econometrics",
        "name": "R for Econometrics & Modeling",
        "domain": "Technical",
        "criticality": 0.75,
        "description": "Time-series forecasting, ARIMA, panel regressions and survey data packages (survey, srvyr)."
    },
    "gis_fundamentals": {
        "id": "gis_fundamentals",
        "name": "GIS & Spatial Analytics",
        "domain": "Technical",
        "criticality": 0.80,
        "description": "QGIS, geospatial boundary shapefiles, spatial sampling allocation and thematic census mapping."
    },
    "sql_databases": {
        "id": "sql_databases",
        "name": "SQL & Statistical Data Warehousing",
        "domain": "Technical",
        "criticality": 0.78,
        "description": "Relational schema design, complex joins on microdata files, and indexing for big datasets."
    },
    "ai_ml_stats": {
        "id": "ai_ml_stats",
        "name": "Machine Learning for Official Statistics",
        "domain": "Technical",
        "criticality": 0.85,
        "description": "Supervised predictive modeling, automated text coding of economic activities, and imputation."
    },

    # --- Digital Governance Domain ---
    "metadata_standards": {
        "id": "metadata_standards",
        "name": "Metadata Standards (SDMX & NADA)",
        "domain": "Digital Governance",
        "criticality": 0.88,
        "description": "Statistical Data and Metadata eXchange standard, DDI cataloguing and open data portals."
    },
    "data_privacy_dpdp": {
        "id": "data_privacy_dpdp",
        "name": "Data Privacy & DPDP Act 2023",
        "domain": "Digital Governance",
        "criticality": 0.92,
        "description": "Personal data fiduciary obligations, microdata anonymization, and statistical confidentiality."
    },
    "capi_digital_tools": {
        "id": "capi_digital_tools",
        "name": "Computer Assisted Personal Interviewing (CAPI)",
        "domain": "Digital Governance",
        "criticality": 0.85,
        "description": "Digital field schedules, validation checks during data collection, and tablet sync protocols."
    },

    # --- Behavioural & Leadership Domain ---
    "project_management": {
        "id": "project_management",
        "name": "Statistical Project Management",
        "domain": "Behavioural",
        "criticality": 0.80,
        "description": "Survey timeline management, field team logistics, budget oversight and quality assurance audits."
    },
    "leadership_ethics": {
        "id": "leadership_ethics",
        "name": "Leadership & Statistical Ethics",
        "domain": "Behavioural",
        "criticality": 0.85,
        "description": "UN Fundamental Principles of Official Statistics, conflict resolution and team mentoring."
    },
    "evidence_communication": {
        "id": "evidence_communication",
        "name": "Evidence-Based Policy Communication",
        "domain": "Behavioural",
        "criticality": 0.78,
        "description": "Writing statistical press notes, data dissemination briefings and stakeholder presentations."
    }
}


# Default role profiles
ROLE_PROFILES = {
    "JSO": {
        "title": "Junior Statistical Officer",
        "department": "Data Informatics & Innovation Division (DIID)",
        "experience": "3 years",
        "target_mastery": {
            "survey_design": 0.85,
            "survey_sampling": 0.80,
            "national_accounts": 0.65,
            "price_indices": 0.70,
            "industrial_stats": 0.70,
            "python_data_analysis": 0.75,
            "r_econometrics": 0.55,
            "gis_fundamentals": 0.70,
            "sql_databases": 0.70,
            "ai_ml_stats": 0.65,
            "metadata_standards": 0.80,
            "data_privacy_dpdp": 0.85,
            "capi_digital_tools": 0.85,
            "project_management": 0.80,
            "leadership_ethics": 0.75,
            "evidence_communication": 0.70
        }
    },
    "SSO": {
        "title": "Senior Statistical Officer",
        "department": "Field Operations Division (FOD)",
        "experience": "8 years",
        "target_mastery": {
            "survey_design": 0.90,
            "survey_sampling": 0.88,
            "national_accounts": 0.75,
            "price_indices": 0.80,
            "industrial_stats": 0.85,
            "python_data_analysis": 0.80,
            "r_econometrics": 0.70,
            "gis_fundamentals": 0.80,
            "sql_databases": 0.80,
            "ai_ml_stats": 0.75,
            "metadata_standards": 0.85,
            "data_privacy_dpdp": 0.90,
            "capi_digital_tools": 0.90,
            "project_management": 0.88,
            "leadership_ethics": 0.85,
            "evidence_communication": 0.82
        }
    },
    "ISS": {
        "title": "Indian Statistical Service Officer (Director)",
        "department": "National Accounts Division (NAD)",
        "experience": "15 years",
        "target_mastery": {
            "survey_design": 0.95,
            "survey_sampling": 0.92,
            "national_accounts": 0.95,
            "price_indices": 0.92,
            "industrial_stats": 0.90,
            "python_data_analysis": 0.75,
            "r_econometrics": 0.80,
            "gis_fundamentals": 0.75,
            "sql_databases": 0.75,
            "ai_ml_stats": 0.80,
            "metadata_standards": 0.95,
            "data_privacy_dpdp": 0.95,
            "capi_digital_tools": 0.85,
            "project_management": 0.95,
            "leadership_ethics": 0.95,
            "evidence_communication": 0.95
        }
    }
}


class CompetencyService:
    def __init__(self):
        # Initial state representing Livjot Singh Bedi (JSO, DIID) as specified in STATWISE Screenbook
        self.learner_state = {
            "user_id": "usr_livjot_26101",
            "name": "Livjot Singh Bedi",
            "designation": "Junior Statistical Officer",
            "role_code": "JSO",
            "department": "Data Informatics & Innovation Division (DIID)",
            "experience": "3 years",
            "preferred_language": "English / Hindi",
            "learning_hours": 24.5,
            "quiz_accuracy": 82.0,
            "current_mastery": {
                "survey_design": 0.62,
                "survey_sampling": 0.58,
                "national_accounts": 0.50,
                "price_indices": 0.55,
                "industrial_stats": 0.48,
                "python_data_analysis": 0.48,
                "r_econometrics": 0.42,
                "gis_fundamentals": 0.44,
                "sql_databases": 0.60,
                "ai_ml_stats": 0.38,
                "metadata_standards": 0.55,
                "data_privacy_dpdp": 0.64,
                "capi_digital_tools": 0.72,
                "project_management": 0.66,
                "leadership_ethics": 0.70,
                "evidence_communication": 0.65
            },
            "completed_competencies": [
                "survey_design_foundations",
                "basic_statistics",
                "python_fundamentals"
            ]
        }

    def get_profile(self) -> Dict[str, Any]:
        role_target = ROLE_PROFILES[self.learner_state["role_code"]]["target_mastery"]
        current = self.learner_state["current_mastery"]

        # Calculate overall readiness
        total_current = sum(current.values())
        total_target = sum(role_target.values())
        readiness_pct = round((total_current / total_target) * 100, 1)

        # Domain health scores
        domains = ["Statistical", "Technical", "Digital Governance", "Behavioural"]
        domain_health = {}
        for d in domains:
            domain_skills = [k for k, v in COMPETENCY_REGISTRY.items() if v["domain"] == d]
            if domain_skills:
                curr_sum = sum(current[k] for k in domain_skills)
                targ_sum = sum(role_target[k] for k in domain_skills)
                pct = int(round((curr_sum / targ_sum) * 100))
                domain_health[d] = pct

        # Calculate gaps
        gaps = []
        for k, v in COMPETENCY_REGISTRY.items():
            c_val = current.get(k, 0.5)
            t_val = role_target.get(k, 0.8)
            gap_val = max(0.0, round(t_val - c_val, 2))
            priority = round(gap_val * v["criticality"] * 100, 1)
            is_urgent = gap_val >= 0.25 and v["criticality"] >= 0.85
            gaps.append({
                "id": k,
                "name": v["name"],
                "domain": v["domain"],
                "current_mastery": int(round(c_val * 100)),
                "target_mastery": int(round(t_val * 100)),
                "gap": int(round(gap_val * 100)),
                "gap_ratio": round(gap_val, 2),
                "priority_score": priority,
                "is_urgent": is_urgent,
                "description": v["description"]
            })

        # Sort gaps by priority score descending
        gaps.sort(key=lambda x: x["priority_score"], reverse=True)
        priority_gaps_count = len([g for g in gaps if g["gap"] > 15])
        urgent_gaps_count = len([g for g in gaps if g["is_urgent"]])

        # Radar chart comparative overlay items
        radar_keys = ["survey_design", "python_data_analysis", "metadata_standards", "leadership_ethics", "gis_fundamentals", "project_management"]
        radar_data = []
        for rk in radar_keys:
            radar_data.append({
                "skill": COMPETENCY_REGISTRY[rk]["name"].split(" ")[0],
                "full_name": COMPETENCY_REGISTRY[rk]["name"],
                "current": int(round(current.get(rk, 0.5) * 100)),
                "target": int(round(role_target.get(rk, 0.8) * 100))
            })

        return {
            "learner": self.learner_state,
            "overall_readiness": {
                "current_readiness": int(readiness_pct),
                "target_readiness": 85,
                "status": "On Track" if readiness_pct >= 65 else "Needs Attention"
            },
            "kpis": {
                "overall_readiness": int(readiness_pct),
                "priority_gaps_count": priority_gaps_count,
                "urgent_gaps_count": urgent_gaps_count,
                "learning_hours": self.learner_state["learning_hours"],
                "quiz_accuracy": self.learner_state["quiz_accuracy"]
            },
            "domain_health": domain_health,
            "top_gaps": gaps[:6],
            "all_gaps": gaps,
            "radar_chart": radar_data
        }

    def record_learning_progress(self, competency_id: str, mastery_gain: float = 0.08, hours_added: float = 1.0):
        """
        Dynamically updates competency scores in real-time post completion.
        """
        if competency_id in self.learner_state["current_mastery"]:
            prev = self.learner_state["current_mastery"][competency_id]
            self.learner_state["current_mastery"][competency_id] = min(1.0, round(prev + mastery_gain, 2))
        self.learner_state["learning_hours"] = round(self.learner_state["learning_hours"] + hours_added, 1)
        return self.get_profile()

    def set_role(self, role_code: str):
        if role_code in ROLE_PROFILES:
            self.learner_state["role_code"] = role_code
            self.learner_state["designation"] = ROLE_PROFILES[role_code]["title"]
            self.learner_state["department"] = ROLE_PROFILES[role_code]["department"]
            self.learner_state["experience"] = ROLE_PROFILES[role_code]["experience"]
        return self.get_profile()
