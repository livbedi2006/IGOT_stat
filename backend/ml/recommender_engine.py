from typing import List, Dict, Any
import numpy as np


class RecommenderEngine:
    def __init__(self):
        # Weights according to PRD FR-21
        self.w_relevance = 0.40
        self.w_difficulty = 0.25
        self.w_duration = 0.15
        self.w_rating = 0.20

        # Knowledge graph prerequisites mapping
        self.prerequisites_graph = {
            "survey_sampling": ["survey_design_foundations"],
            "complex_estimation": ["survey_sampling"],
            "data_cleaning_python": ["python_fundamentals"],
            "statistical_ml": ["data_cleaning_python", "basic_statistics"],
            "data_quality_frameworks": ["survey_sampling"],
            "macro_aggregates_nas": ["basic_macroeconomics"],
            "chain_linking_indices": ["index_numbers_foundations"]
        }

    def evaluate_prerequisites(self, course_req_id: str, completed_competencies: List[str]) -> bool:
        """
        Validates if learner meets DAG prerequisites for a course.
        """
        prereqs = self.prerequisites_graph.get(course_req_id, [])
        for p in prereqs:
            if p not in completed_competencies:
                return False
        return True

    def calculate_difficulty_match(self, course_difficulty: str, user_proficiency: float) -> float:
        """
        Scores how well course difficulty matches learner proficiency level:
        - If proficiency < 40%, 'Beginner' or 'Easy' is best match (1.0).
        - If proficiency 40-70%, 'Intermediate' or 'Medium' is best match (1.0).
        - If proficiency > 70%, 'Advanced' or 'Hard' is best match (1.0).
        """
        user_band = "Beginner" if user_proficiency < 45 else ("Intermediate" if user_proficiency < 75 else "Advanced")

        if course_difficulty.lower() == user_band.lower():
            return 1.0
        elif (user_band == "Beginner" and course_difficulty.lower() == "intermediate") or \
             (user_band == "Intermediate" and course_difficulty.lower() in ["beginner", "advanced"]):
            return 0.70
        else:
            return 0.40

    def calculate_duration_fit(self, duration_hours: float, user_target_hours_per_week: float = 6.0) -> float:
        """
        Scores whether the course length fits within monthly learning capacity.
        Courses between 2 to 8 hours score highest for micro-learning.
        """
        if duration_hours <= 0:
            return 0.5
        if 2.0 <= duration_hours <= 8.0:
            return 1.0
        elif duration_hours <= 16.0:
            return 0.85
        elif duration_hours <= 40.0:
            return 0.70
        else:
            return 0.55

    def rank_courses(
        self,
        courses: List[Dict[str, Any]],
        user_gaps: Dict[str, float],
        completed_competencies: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Ranks courses using multi-criteria weighted scoring + prerequisite checks.
        """
        scored_courses = []

        for c in courses:
            competency_key = c.get("competency_key", "")
            # Gap value between 0.0 and 1.0
            gap = user_gaps.get(competency_key, 0.5)

            # 1. Relevance score based on gap magnitude & alignment
            relevance = float(np.clip(gap, 0.1, 1.0))

            # 2. Difficulty match
            difficulty = c.get("difficulty", "Intermediate")
            user_mastery = 1.0 - gap
            difficulty_match = self.calculate_difficulty_match(difficulty, user_mastery * 100)

            # 3. Duration fit
            duration_hours = c.get("duration_hours", 4.0)
            duration_fit = self.calculate_duration_fit(duration_hours)

            # 4. Normalized rating (e.g. 4.8 / 5.0 -> 0.96)
            rating = c.get("rating", 4.5) / 5.0

            # Multi-criteria utility score
            final_score = (
                self.w_relevance * relevance +
                self.w_difficulty * difficulty_match +
                self.w_duration * duration_fit +
                self.w_rating * rating
            )

            # Prerequisite satisfaction check
            req_id = c.get("req_id", "")
            prereqs_satisfied = self.evaluate_prerequisites(req_id, completed_competencies)

            match_percentage = int(round(final_score * 100))

            course_copy = dict(c)
            course_copy["match_percentage"] = match_percentage
            course_copy["composite_score"] = round(final_score, 3)
            course_copy["prerequisites_satisfied"] = prereqs_satisfied
            course_copy["score_breakdown"] = {
                "relevance_contribution": round(self.w_relevance * relevance * 100, 1),
                "difficulty_contribution": round(self.w_difficulty * difficulty_match * 100, 1),
                "duration_contribution": round(self.w_duration * duration_fit * 100, 1),
                "rating_contribution": round(self.w_rating * rating * 100, 1)
            }
            scored_courses.append(course_copy)

        # Sort descending by composite score
        scored_courses.sort(key=lambda x: x["composite_score"], reverse=True)
        return scored_courses
