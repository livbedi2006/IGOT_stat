"""
iGOT Karmayogi & NSSTA TPAC Blended Learning Catalogue Service.
Provides:
- Curated iGOT Karmayogi digital courses for statistical civil servants.
- Curated NSSTA (National Statistical Systems Training Academy) TPAC in-person programmes.
- Personalized learning path sequencing (Foundation -> Core -> Practice -> Advanced).
- Dynamic hybrid recommendations powered by RecommenderEngine.
"""

from typing import Dict, Any, List
from ml.recommender_engine import RecommenderEngine


ALL_COURSES = [
    # --- iGOT Karmayogi Courses ---
    {
        "id": "igot_py_101",
        "title": "Python for Government Data Analysis",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Technical",
        "competency_key": "python_data_analysis",
        "req_id": "python_fundamentals",
        "difficulty": "Intermediate",
        "duration_hours": 6.0,
        "duration_label": "6 hours",
        "rating": 4.8,
        "enrollments": 4120,
        "reason": "Builds Python competency for automated data wrangling in current assignment.",
        "description": "Comprehensive hands-on course covering Pandas, NumPy, statistical data cleaning and automated report generation for official datasets."
    },
    {
        "id": "igot_ss_102",
        "title": "Survey Sampling for Official Statistics",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Statistical",
        "competency_key": "survey_sampling",
        "req_id": "survey_sampling",
        "difficulty": "Intermediate",
        "duration_hours": 4.0,
        "duration_label": "4 hours",
        "rating": 4.9,
        "enrollments": 5830,
        "reason": "Directly addresses your #1 highest priority gap in sampling estimation.",
        "description": "Covers multistage stratification, sample allocation formulas, calculation of survey multipliers and estimation of sampling errors in NSS rounds."
    },
    {
        "id": "igot_sd_103",
        "title": "Foundation: Survey Design & Sampling Frames",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Statistical",
        "competency_key": "survey_design",
        "req_id": "survey_design_foundations",
        "difficulty": "Beginner",
        "duration_hours": 3.0,
        "duration_label": "3 hours",
        "rating": 4.7,
        "enrollments": 6200,
        "reason": "Core foundational prerequisite for advanced statistical sampling.",
        "description": "Sampling frames, enumeration blocks, rural/urban classification, and household listing procedures."
    },
    {
        "id": "igot_r_104",
        "title": "Data Visualization & Modeling with R",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Technical",
        "competency_key": "r_econometrics",
        "req_id": "r_econometrics",
        "difficulty": "Intermediate",
        "duration_hours": 5.0,
        "duration_label": "5 hours",
        "rating": 4.6,
        "enrollments": 2980,
        "reason": "Supports automated chart reporting and dissemination work.",
        "description": "Exploratory data analysis with ggplot2, econometric regressions, and reproducible reporting with R Markdown."
    },
    {
        "id": "igot_dpdp_105",
        "title": "Digital Personal Data Protection (DPDP) Act 2023 for Public Fiduciaries",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Digital Governance",
        "competency_key": "data_privacy_dpdp",
        "req_id": "data_privacy_dpdp",
        "difficulty": "Intermediate",
        "duration_hours": 3.5,
        "duration_label": "3.5 hours",
        "rating": 4.9,
        "enrollments": 7150,
        "reason": "Mandatory statutory compliance for all officials handling survey microdata.",
        "description": "Obligations of Data Fiduciaries, anonymization standards, consent mechanisms, and safe release of public statistics."
    },
    {
        "id": "igot_sdmx_106",
        "title": "Metadata Standards & SDMX Implementation",
        "provider": "iGOT Karmayogi",
        "type": "Online Course",
        "domain": "Digital Governance",
        "competency_key": "metadata_standards",
        "req_id": "metadata_standards",
        "difficulty": "Intermediate",
        "duration_hours": 4.0,
        "duration_label": "4 hours",
        "rating": 4.7,
        "enrollments": 1840,
        "reason": "Aligns official statistical releases with UN and NADA standards.",
        "description": "Structure of SDMX registries, data structure definitions (DSD), and automated exchange of time-series data."
    },

    # --- NSSTA TPAC In-Person / Executive Programmes ---
    {
        "id": "nssta_tpac_201",
        "title": "Advanced Survey Design & Quality Assurance",
        "provider": "NSSTA / TPAC",
        "type": "In-person Workshop",
        "domain": "Statistical",
        "competency_key": "survey_design",
        "req_id": "survey_sampling",
        "difficulty": "Advanced",
        "duration_hours": 35.0,
        "duration_label": "5 days (In-Person, Greater Noida)",
        "rating": 4.9,
        "enrollments": 340,
        "reason": "Closes critical Survey Design gap with hands-on mentoring from senior ISS officers.",
        "description": "Intensive executive workshop at NSSTA Campus covering complex survey weighting, non-response mitigation, and field inspection audits."
    },
    {
        "id": "nssta_tpac_202",
        "title": "Advanced: Data Quality Frameworks & CAPI Auditing",
        "provider": "NSSTA / TPAC",
        "type": "In-person Workshop",
        "domain": "Statistical",
        "competency_key": "data_quality",
        "req_id": "data_quality_frameworks",
        "difficulty": "Advanced",
        "duration_hours": 35.0,
        "duration_label": "5 days (In-Person)",
        "rating": 4.8,
        "enrollments": 280,
        "reason": "High-impact TPAC curriculum recommended for DIID and FOD officers.",
        "description": "Methodologies for validating Computer Assisted Personal Interviewing schedules and automated rule-based scrutiny."
    },
    {
        "id": "nssta_tpac_203",
        "title": "Machine Learning Applications in Official Statistics",
        "provider": "NSSTA / TPAC",
        "type": "Hybrid Programme",
        "domain": "Technical",
        "competency_key": "ai_ml_stats",
        "req_id": "statistical_ml",
        "difficulty": "Advanced",
        "duration_hours": 40.0,
        "duration_label": "2 weeks (Hybrid)",
        "rating": 4.9,
        "enrollments": 190,
        "reason": "Prepares official statisticians for AI-driven automated industry coding and predictive forecasting.",
        "description": "Covers classification algorithms, satellite imagery analysis for crop acreage, and synthetic dataset generation."
    },
    {
        "id": "nssta_tpac_204",
        "title": "National Accounts Statistics & Supply-Use Tables (SUT)",
        "provider": "NSSTA / TPAC",
        "type": "In-person Workshop",
        "domain": "Statistical",
        "competency_key": "national_accounts",
        "req_id": "macro_aggregates_nas",
        "difficulty": "Advanced",
        "duration_hours": 28.0,
        "duration_label": "4 days (In-Person)",
        "rating": 4.9,
        "enrollments": 220,
        "reason": "Crucial for officers in National Accounts Division and State DES departments.",
        "description": "SNA 2008 framework, balancing commodity flows in SUT tables, and compiling constant-price state domestic products."
    }
]


class CourseCatalogueService:
    def __init__(self):
        self.recommender = RecommenderEngine()

    def get_recommendations(self, user_gaps: Dict[str, float], completed_competencies: List[str], filter_tag: str = "All") -> List[Dict[str, Any]]:
        """
        Returns ranked course recommendations with explainability metadata.
        """
        ranked = self.recommender.rank_courses(ALL_COURSES, user_gaps, completed_competencies)

        if filter_tag == "iGOT":
            return [c for c in ranked if "iGOT" in c["provider"]]
        elif filter_tag == "NSSTA / TPAC" or filter_tag == "NSSTA":
            return [c for c in ranked if "NSSTA" in c["provider"]]
        elif filter_tag in ["Technical", "Statistical", "Digital Governance", "Behavioural"]:
            return [c for c in ranked if c["domain"] == filter_tag]
        return ranked

    def get_learning_path(self, completed_competencies: List[str]) -> Dict[str, Any]:
        """
        Constructs the sequenced 4-step personalized learning pathway matching Screen 03.
        """
        is_step1_done = "survey_design_foundations" in completed_competencies
        is_step2_done = "survey_sampling" in completed_competencies
        is_step3_done = "data_cleaning_python" in completed_competencies

        pathway_steps = [
            {
                "step_number": 1,
                "title": "Foundation: Survey Design",
                "provider": "iGOT",
                "duration": "3 h",
                "status": "Completed" if is_step1_done else "In progress",
                "badge_color": "emerald",
                "type": "iGOT Course"
            },
            {
                "step_number": 2,
                "title": "Core: Survey Sampling",
                "provider": "iGOT",
                "duration": "4 h",
                "status": "In progress" if not is_step2_done else "Completed",
                "badge_color": "sky",
                "type": "iGOT Course"
            },
            {
                "step_number": 3,
                "title": "Practice: Python Data Cleaning",
                "provider": "Virtual Lab",
                "duration": "2 h",
                "status": "Next" if not is_step3_done else "Completed",
                "badge_color": "amber",
                "type": "Hands-on Virtual Lab"
            },
            {
                "step_number": 4,
                "title": "Advanced: Data Quality Frameworks",
                "provider": "NSSTA / TPAC",
                "duration": "5 days",
                "status": "Locked until step 2" if not is_step2_done else "Unlocked (Eligible)",
                "badge_color": "slate",
                "type": "NSSTA TPAC Workshop"
            }
        ]

        return {
            "path_score": 84,
            "alignment_label": "Role alignment",
            "time_left_hours": 11,
            "time_left_label": "Time left this month",
            "steps": pathway_steps
        }
