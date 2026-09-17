"""
STATWISE Official Statistics Competency Framework & Gap Analytics Engine.
Adheres strictly to SIH MoSPI Problem Statement 26101 and the STATWISE Prompt Pack:
- 4 Domains: Statistical, Technical, Digital Governance, Behavioural/Managerial.
- 5 Cadre Personas: Junior Statistical Officer (JSO), Senior Statistical Officer (SSO),
  Data Analyst (ANALYST), Indian Statistical Service (ISS), and Training Administrator (TRAINER).
- 5 Evidence Types: self_assessment, quiz, course_completion, manager_validation, virtual_lab.
- Configurable Gap Ranking:
  Score = 0.45 * Normalized_Gap + 0.30 * Role_Criticality + 0.15 * Assignment_Relevance + 0.10 * Prerequisite_Urgency.
"""

from typing import Dict, Any, List, Optional
import copy


# Complete 4-Domain Competency Catalogue with Criticality, Prerequisites & Evidence Types
COMPETENCY_REGISTRY = {
    # --- Statistical Domain ---
    "survey_design": {
        "id": "survey_design",
        "name": "Survey Design & Sampling Frames",
        "domain": "Statistical",
        "role_criticality": 5,      # Scale 1-5
        "criticality_weight": 0.95, # Normalized 0-1
        "description": "Formulation of sampling frames, stratification, allocation and NSS multi-stage sampling methodology.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["quiz", "course_completion", "manager_validation"]
    },
    "survey_sampling": {
        "id": "survey_sampling",
        "name": "Sample Estimation & Variance Calculation",
        "domain": "Statistical",
        "role_criticality": 5,
        "criticality_weight": 0.95,
        "description": "Horvitz-Thompson estimation, multiplier calculation, calibration weighting and sampling error.",
        "prerequisites": ["survey_design"],
        "evidence_types": ["quiz", "virtual_lab", "course_completion"]
    },
    "national_accounts": {
        "id": "national_accounts",
        "name": "National Accounts Statistics (NAS & SUT)",
        "domain": "Statistical",
        "role_criticality": 4,
        "criticality_weight": 0.85,
        "description": "System of National Accounts (SNA 2008), GVA compilation, supply-use tables and deflators.",
        "prerequisites": ["macroeconomics_basics"],
        "evidence_types": ["course_completion", "quiz"]
    },
    "price_indices": {
        "id": "price_indices",
        "name": "Price Indices Compilation (CPI & WPI)",
        "domain": "Statistical",
        "role_criticality": 4,
        "criticality_weight": 0.88,
        "description": "Laspeyres index formula, item weighting baskets, rural/urban aggregation and core inflation.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["quiz", "virtual_lab"]
    },
    "industrial_stats": {
        "id": "industrial_stats",
        "name": "Industrial Statistics (ASI & IIP)",
        "domain": "Statistical",
        "role_criticality": 4,
        "criticality_weight": 0.82,
        "description": "Annual Survey of Industries methodology, NIC classification and IIP production weights.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["quiz", "virtual_lab"]
    },

    # --- Technical & Data Science Domain ---
    "python_data_analysis": {
        "id": "python_data_analysis",
        "name": "Python for Data Analysis & Wrangling",
        "domain": "Technical",
        "role_criticality": 5,
        "criticality_weight": 0.90,
        "description": "Pandas, NumPy, automated data wrangling, outlier detection and statistical validation.",
        "prerequisites": ["programming_basics"],
        "evidence_types": ["virtual_lab", "quiz", "course_completion"]
    },
    "r_econometrics": {
        "id": "r_econometrics",
        "name": "R for Econometrics & Modeling",
        "domain": "Technical",
        "role_criticality": 3,
        "criticality_weight": 0.75,
        "description": "Time-series forecasting, ARIMA, panel regressions and survey data packages (survey, srvyr).",
        "prerequisites": ["python_data_analysis"],
        "evidence_types": ["virtual_lab", "course_completion"]
    },
    "gis_fundamentals": {
        "id": "gis_fundamentals",
        "name": "GIS & Spatial Analytics",
        "domain": "Technical",
        "role_criticality": 4,
        "criticality_weight": 0.80,
        "description": "QGIS, geospatial boundary shapefiles, spatial sampling allocation and thematic census mapping.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["virtual_lab", "course_completion"]
    },
    "sql_databases": {
        "id": "sql_databases",
        "name": "SQL & Microdata Warehousing",
        "domain": "Technical",
        "role_criticality": 4,
        "criticality_weight": 0.78,
        "description": "Relational schema design, complex joins on survey microdata files, and indexing.",
        "prerequisites": ["programming_basics"],
        "evidence_types": ["virtual_lab", "quiz"]
    },
    "ai_ml_stats": {
        "id": "ai_ml_stats",
        "name": "Machine Learning for Official Statistics",
        "domain": "Technical",
        "role_criticality": 4,
        "criticality_weight": 0.85,
        "description": "Supervised predictive modeling, automated text coding of economic activities, and imputation.",
        "prerequisites": ["python_data_analysis", "survey_sampling"],
        "evidence_types": ["virtual_lab", "course_completion"]
    },

    # --- Digital Governance & Privacy Domain ---
    "metadata_standards": {
        "id": "metadata_standards",
        "name": "Metadata Standards (SDMX & NADA)",
        "domain": "Digital Governance",
        "role_criticality": 4,
        "criticality_weight": 0.88,
        "description": "Statistical Data and Metadata eXchange standard, DDI cataloguing and open data portals.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["quiz", "manager_validation"]
    },
    "data_privacy_dpdp": {
        "id": "data_privacy_dpdp",
        "name": "Data Privacy & DPDP Act 2023",
        "domain": "Digital Governance",
        "role_criticality": 5,
        "criticality_weight": 0.92,
        "description": "Personal data fiduciary obligations, microdata anonymization, and statistical confidentiality.",
        "prerequisites": [],
        "evidence_types": ["quiz", "course_completion", "manager_validation"]
    },
    "capi_digital_tools": {
        "id": "capi_digital_tools",
        "name": "Computer Assisted Personal Interviewing (CAPI)",
        "domain": "Digital Governance",
        "role_criticality": 4,
        "criticality_weight": 0.85,
        "description": "Digital field schedules, validation checks during data collection, and tablet sync protocols.",
        "prerequisites": ["survey_design"],
        "evidence_types": ["quiz", "manager_validation"]
    },

    # --- Behavioural & Leadership Domain ---
    "project_management": {
        "id": "project_management",
        "name": "Statistical Project Management",
        "domain": "Behavioural",
        "role_criticality": 4,
        "criticality_weight": 0.80,
        "description": "Survey timeline management, field team logistics, budget oversight and quality audits.",
        "prerequisites": [],
        "evidence_types": ["manager_validation", "course_completion"]
    },
    "leadership_ethics": {
        "id": "leadership_ethics",
        "name": "Leadership & Statistical Ethics",
        "domain": "Behavioural",
        "role_criticality": 4,
        "criticality_weight": 0.85,
        "description": "UN Fundamental Principles of Official Statistics, conflict resolution and team mentoring.",
        "prerequisites": [],
        "evidence_types": ["manager_validation", "course_completion"]
    },
    "evidence_communication": {
        "id": "evidence_communication",
        "name": "Evidence-Based Policy Communication",
        "domain": "Behavioural",
        "role_criticality": 4,
        "criticality_weight": 0.78,
        "description": "Writing statistical press notes, data dissemination briefings and stakeholder presentations.",
        "prerequisites": ["basic_statistics"],
        "evidence_types": ["manager_validation", "quiz"]
    }
}


# 5 Cadre Role Personas (Prompt C & S)
ROLE_PROFILES = {
    "JSO": {
        "role_code": "JSO",
        "title": "Junior Statistical Officer",
        "department": "Data Informatics & Innovation Division (DIID)",
        "typical_experience": "3 years",
        "default_assignment": "PLFS Microdata Scrutiny & CAPI Validation",
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
        "role_code": "SSO",
        "title": "Senior Statistical Officer",
        "department": "Field Operations Division (FOD)",
        "typical_experience": "8 years",
        "default_assignment": "Regional Field Super-Inspection & Frame Updating",
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
    "ANALYST": {
        "role_code": "ANALYST",
        "title": "Data Analyst & GIS Specialist",
        "department": "DIID Technical Unit",
        "typical_experience": "4 years",
        "default_assignment": "Geospatial Frame Matching & Big Data Pipeline",
        "target_mastery": {
            "survey_design": 0.70,
            "survey_sampling": 0.75,
            "national_accounts": 0.60,
            "price_indices": 0.65,
            "industrial_stats": 0.65,
            "python_data_analysis": 0.95,
            "r_econometrics": 0.85,
            "gis_fundamentals": 0.95,
            "sql_databases": 0.90,
            "ai_ml_stats": 0.90,
            "metadata_standards": 0.85,
            "data_privacy_dpdp": 0.88,
            "capi_digital_tools": 0.75,
            "project_management": 0.75,
            "leadership_ethics": 0.70,
            "evidence_communication": 0.75
        }
    },
    "ISS": {
        "role_code": "ISS",
        "title": "Indian Statistical Service Officer (Director)",
        "department": "National Accounts Division (NAD)",
        "typical_experience": "15 years",
        "default_assignment": "National GDP Revision & Supply-Use Balancing",
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
    },
    "TRAINER": {
        "role_code": "TRAINER",
        "title": "NSSTA Faculty / Training Administrator",
        "department": "NSSTA Greater Noida Campus",
        "typical_experience": "12 years",
        "default_assignment": "TPAC Curriculum Design & Faculty Assessment",
        "target_mastery": {
            "survey_design": 0.95,
            "survey_sampling": 0.95,
            "national_accounts": 0.90,
            "price_indices": 0.90,
            "industrial_stats": 0.88,
            "python_data_analysis": 0.85,
            "r_econometrics": 0.85,
            "gis_fundamentals": 0.85,
            "sql_databases": 0.80,
            "ai_ml_stats": 0.85,
            "metadata_standards": 0.92,
            "data_privacy_dpdp": 0.92,
            "capi_digital_tools": 0.90,
            "project_management": 0.90,
            "leadership_ethics": 0.95,
            "evidence_communication": 0.95
        }
    }
}


# Demo Persona Seed Profiles (Prompt S)
DEMO_PERSONAS = {
    "usr_officer_default": {
        "user_id": "usr_officer_default",
        "name": "Statistical Officer",
        "official_email": "officer@mospi.gov.in",
        "designation": "Junior Statistical Officer",
        "role_code": "JSO",
        "department": "Data Informatics & Innovation Division (DIID)",
        "current_assignment": "PLFS Microdata Scrutiny & Automated Tabulation",
        "experience_years": 3,
        "qualification": "M.Sc. Statistics",
        "preferred_language": "English / Hindi",
        "previous_training": "Foundation Course on Official Statistics (NSSTA 2023)",
        "career_goal": "Promotion to Senior Statistical Officer and Lead Data Science Division",
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
        ],
        "evidence_ledger": {
            "survey_design": [{"type": "quiz", "score": 82, "source": "PLFS Baseline Assessment"}],
            "python_data_analysis": [{"type": "virtual_lab", "score": 75, "source": "Pandas Data Cleaning Exercise"}],
            "metadata_standards": [{"type": "course_completion", "score": 70, "source": "iGOT SDMX Overview"}]
        }
    }
}
# Backward compatibility alias
DEMO_PERSONAS["usr_livjot_26101"] = DEMO_PERSONAS["usr_officer_default"]


class CompetencyService:
    def __init__(self):
        # Configurable Ranking Weights (Prompt D)
        # gap = 45%, role criticality = 30%, assignment relevance = 15%, prerequisite urgency = 10%
        self.weight_gap = 0.45
        self.weight_criticality = 0.30
        self.weight_assignment = 0.15
        self.weight_prereq = 0.10

        self.learner_state = copy.deepcopy(DEMO_PERSONAS["usr_officer_default"])
        self.learner_state["id"] = self.learner_state.get("user_id", "usr_officer_default")
        self.learner_state["role"] = self.learner_state.get("role_code", "JSO")

    def update_onboarding_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates learner onboarding profile with server-side validation (Prompt B).
        """
        allowed_fields = [
            "name", "full_name", "official_email", "designation", "department",
            "current_assignment", "experience_years", "qualification",
            "preferred_language", "previous_training", "career_goal"
        ]
        for field in allowed_fields:
            if field in profile_data and profile_data[field]:
                self.learner_state[field] = profile_data[field]
                if field == "full_name":
                    self.learner_state["name"] = profile_data[field]
                elif field == "name":
                    self.learner_state["full_name"] = profile_data[field]

        # Keep id and role aliases synced
        self.learner_state["id"] = self.learner_state.get("user_id", "usr_officer_default")
        self.learner_state["role"] = self.learner_state.get("role_code", "JSO")

        # Sync role code if designation matches known cadres
        if "role_code" in profile_data and profile_data["role_code"] in ROLE_PROFILES:
            self.set_role(profile_data["role_code"])

        return self.get_profile()

    def get_profile(self) -> Dict[str, Any]:
        role_code = self.learner_state["role_code"]
        role_target = ROLE_PROFILES[role_code]["target_mastery"]
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
                curr_sum = sum(current.get(k, 0.5) for k in domain_skills)
                targ_sum = sum(role_target.get(k, 0.8) for k in domain_skills)
                pct = int(round((curr_sum / targ_sum) * 100))
                domain_health[d] = pct

        # Calculate evidence-backed ranked skill gaps (Prompt D)
        gaps = []
        assignment_text = self.learner_state.get("current_assignment", "").lower()
        completed = self.learner_state["completed_competencies"]

        for k, v in COMPETENCY_REGISTRY.items():
            c_val = current.get(k, 0.5)
            t_val = role_target.get(k, 0.8)
            gap_val = max(0.0, round(t_val - c_val, 2))

            # 1. Normalized Gap (0-1)
            norm_gap = gap_val

            # 2. Role Criticality (Normalized 0-1 from 1-5 scale)
            norm_crit = v["role_criticality"] / 5.0

            # 3. Assignment Relevance (1.0 if keywords match current assignment, else 0.4)
            comp_name_lower = v["name"].lower()
            is_relevant_to_assignment = any(
                token in assignment_text for token in comp_name_lower.split() if len(token) > 3
            )
            assign_rel = 1.0 if is_relevant_to_assignment else 0.4

            # 4. Prerequisite Urgency (1.0 if this competency unblocks downstream courses, else 0.5)
            has_unblocked_dependents = any(
                k in item["prerequisites"] for item in COMPETENCY_REGISTRY.values()
            )
            prereq_urgency = 1.0 if has_unblocked_dependents else 0.5

            # Weighted Formula: 45% gap + 30% criticality + 15% assignment + 10% prereq
            priority_score = round(
                (self.weight_gap * norm_gap +
                 self.weight_criticality * norm_crit +
                 self.weight_assignment * assign_rel +
                 self.weight_prereq * prereq_urgency) * 100, 1
            )

            is_urgent = gap_val >= 0.20 and v["role_criticality"] >= 4

            # Evidence breakdown
            evidence = self.learner_state.get("evidence_ledger", {}).get(k, [
                {"type": "self_assessment", "score": int(c_val * 100), "source": "Cadre Baseline"}
            ])

            gaps.append({
                "id": k,
                "name": v["name"],
                "domain": v["domain"],
                "current_mastery": int(round(c_val * 100)),
                "target_mastery": int(round(t_val * 100)),
                "gap": int(round(gap_val * 100)),
                "gap_ratio": round(gap_val, 2),
                "priority_score": priority_score,
                "role_criticality": v["role_criticality"],
                "is_urgent": is_urgent,
                "description": v["description"],
                "evidence": evidence,
                "learner_reason": f"Required for {v['role_criticality']}/5 criticality in {self.learner_state['designation']} role."
            })

        # Sort gaps by weighted priority score descending
        gaps.sort(key=lambda x: x["priority_score"], reverse=True)
        priority_gaps_count = len([g for g in gaps if g["gap"] > 15])
        urgent_gaps_count = len([g for g in gaps if g["is_urgent"]])

        # Radar chart comparative overlay (6 key representative skills)
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
            "top_gaps": gaps[:5],
            "all_gaps": gaps,
            "radar_chart": radar_data,
            "gap_formula": {
                "gap_weight": self.weight_gap,
                "criticality_weight": self.weight_criticality,
                "assignment_weight": self.weight_assignment,
                "prereq_weight": self.weight_prereq
            }
        }

    def record_learning_progress(self, competency_id: str, mastery_gain: float = 0.08, hours_added: float = 1.0, evidence_type: str = "quiz", source_name: str = "Assessment"):
        """
        Dynamically records evidence and updates competency score.
        """
        if competency_id in self.learner_state["current_mastery"]:
            prev = self.learner_state["current_mastery"][competency_id]
            new_val = min(1.0, round(prev + mastery_gain, 2))
            self.learner_state["current_mastery"][competency_id] = new_val

            # Record evidence
            if "evidence_ledger" not in self.learner_state:
                self.learner_state["evidence_ledger"] = {}
            if competency_id not in self.learner_state["evidence_ledger"]:
                self.learner_state["evidence_ledger"][competency_id] = []
            self.learner_state["evidence_ledger"][competency_id].append({
                "type": evidence_type,
                "score": int(new_val * 100),
                "source": source_name
            })

        self.learner_state["learning_hours"] = round(self.learner_state["learning_hours"] + hours_added, 1)
        return self.get_profile()

    def set_role(self, role_code: str):
        if role_code in ROLE_PROFILES:
            prof = ROLE_PROFILES[role_code]
            self.learner_state["role_code"] = role_code
            self.learner_state["role"] = role_code
            self.learner_state["id"] = self.learner_state.get("user_id", "usr_officer_default")
            self.learner_state["designation"] = prof["title"]
            self.learner_state["department"] = prof["department"]
            self.learner_state["experience_years"] = prof.get("typical_experience", "5 years")
            self.learner_state["current_assignment"] = prof.get("default_assignment", "Statistical Work")
        return self.get_profile()
