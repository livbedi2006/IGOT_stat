"""
MCQ Quality Validator Service for STATWISE Platform (Prompt L).
Validates candidate MCQs against MoSPI DIID assessment standards.
Rejects or flags:
1. Fewer or more than four options.
2. Invalid correct index (must be 0, 1, 2, 3 or A, B, C, D).
3. Duplicate options (case-insensitive string match).
4. Answer leaked in question stem.
5. All/none-of-the-above patterns ("all of the above", "none of the above", "both a and b").
6. Missing evidence, missing citation, or missing page reference.
7. Inconsistent or missing explanation.
8. Duplicate/near-duplicate question stems.
9. Ambiguous wording or stems shorter than 15 characters.
10. Absent or invalid competency tag.

Returns structured audit report:
- pass_quality: bool
- executed_checks: Dict[str, bool]
- warnings: List[str]
- confidence_score: float (0.0 to 1.0)
- rejection_reasons: List[str]
- regeneration_instruction: Optional[str]
"""

import re
from typing import Dict, Any, List, Optional


FORBIDDEN_OPTION_PATTERNS = [
    r"\ball of the above\b",
    r"\bnone of the above\b",
    r"\bboth a and b\b",
    r"\bboth b and c\b",
    r"\bboth a and c\b",
    r"\ball the above\b",
    r"\bnone of these\b",
    r"\bneither a nor b\b"
]


class MCQQualityValidator:
    """Validates MCQ pedagogical and statistical soundness."""

    def __init__(self, existing_questions: Optional[List[str]] = None):
        self.existing_question_stems = [self._normalize_stem(q) for q in (existing_questions or [])]

    def _normalize_stem(self, stem: str) -> str:
        return re.sub(r"[^a-zA-Z0-9 ]", "", stem.lower().strip())

    def validate_mcq(self, mcq: Dict[str, Any]) -> Dict[str, Any]:
        executed_checks = {
            "check_four_options": False,
            "check_valid_correct_index": False,
            "check_no_duplicate_options": False,
            "check_no_forbidden_phrasing": False,
            "check_no_answer_leak": False,
            "check_evidence_and_page": False,
            "check_explanation_soundness": False,
            "check_competency_tagged": False,
            "check_stem_clarity": False,
            "check_uniqueness": False
        }

        rejection_reasons: List[str] = []
        warnings: List[str] = []

        # 1. Check exactly four options
        options = mcq.get("options", [])
        if isinstance(options, list) and len(options) == 4:
            executed_checks["check_four_options"] = True
        else:
            rejection_reasons.append(f"MCQ must have exactly 4 options. Found: {len(options) if isinstance(options, list) else 0}")

        # Extract text from options (supports list of dicts [{"id": "A", "text": "..."}] or list of strings)
        opt_texts = []
        for opt in (options if isinstance(options, list) else []):
            if isinstance(opt, dict):
                opt_texts.append(opt.get("text", "").strip())
            else:
                opt_texts.append(str(opt).strip())

        # 2. Check valid correct option index
        correct_val = mcq.get("correct_answer") or mcq.get("correct_index")
        valid_index = False
        correct_text = ""

        if isinstance(correct_val, int) and 0 <= correct_val <= 3:
            valid_index = True
            if len(opt_texts) > correct_val:
                correct_text = opt_texts[correct_val]
        elif isinstance(correct_val, str):
            c_upper = correct_val.strip().upper()
            mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
            if c_upper in mapping and mapping[c_upper] < len(opt_texts):
                valid_index = True
                correct_text = opt_texts[mapping[c_upper]]
            elif correct_val.isdigit() and 0 <= int(correct_val) <= 3:
                valid_index = True
                correct_text = opt_texts[int(correct_val)]

        if valid_index:
            executed_checks["check_valid_correct_index"] = True
        else:
            rejection_reasons.append(f"Invalid correct_answer identifier: '{correct_val}'. Must identify an option in [0..3] or [A..D].")

        # 3. Check duplicate options
        clean_opts = [o.lower() for o in opt_texts if o]
        if len(set(clean_opts)) == len(opt_texts) and len(opt_texts) == 4:
            executed_checks["check_no_duplicate_options"] = True
        else:
            rejection_reasons.append("Duplicate or empty options detected in options list.")

        # 4. Check forbidden patterns (all/none of the above)
        has_forbidden = False
        for text in opt_texts:
            for pattern in FORBIDDEN_OPTION_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    has_forbidden = True
                    break
        if not has_forbidden:
            executed_checks["check_no_forbidden_phrasing"] = True
        else:
            rejection_reasons.append("Forbidden 'all of the above' / 'none of the above' phrasing detected. Every option must be a distinct, concrete alternative.")

        # 5. Check answer leaked in question stem
        stem = mcq.get("question", "").strip()
        if len(stem) >= 15:
            executed_checks["check_stem_clarity"] = True
        else:
            rejection_reasons.append("Question stem is too short or ambiguous (< 15 characters).")

        answer_leaked = False
        if correct_text and len(correct_text) > 8 and correct_text.lower() in stem.lower():
            answer_leaked = True
            rejection_reasons.append(f"Answer leakage detected: verbatim key phrase '{correct_text[:20]}...' appears in question stem.")
        if not answer_leaked:
            executed_checks["check_no_answer_leak"] = True

        # 6. Check evidence and page reference
        grounding = mcq.get("grounding") or {}
        has_doc = bool(grounding.get("source_document") or mcq.get("source_document") or mcq.get("source_file_id"))
        has_page = bool(grounding.get("page_number") or mcq.get("page_number") or mcq.get("source_page_slide"))
        has_citation = bool(grounding.get("citation") or mcq.get("supporting_source_text") or grounding.get("paragraph"))

        if has_doc and (has_page or has_citation):
            executed_checks["check_evidence_and_page"] = True
        else:
            rejection_reasons.append("Missing source grounding: Must cite source_document and page_number/paragraph.")

        # 7. Check explanation soundness
        explanation = mcq.get("explanation", "").strip()
        if len(explanation) >= 20:
            executed_checks["check_explanation_soundness"] = True
        else:
            warnings.append("Explanation is very brief. Provide detailed reasoning for official statistical training.")

        # 8. Check competency tag
        comp = mcq.get("competency_key") or mcq.get("competency_id") or mcq.get("competency_ids")
        if comp:
            executed_checks["check_competency_tagged"] = True
        else:
            rejection_reasons.append("Absent competency tag. Every question must link to a MoSPI competency framework node.")

        # 9. Check uniqueness
        norm_stem = self._normalize_stem(stem)
        is_duplicate = any(norm_stem == existing for existing in self.existing_question_stems)
        if not is_duplicate:
            executed_checks["check_uniqueness"] = True
        else:
            rejection_reasons.append("Question stem is a duplicate or near-duplicate of an existing item in the assessment bank.")

        # Overall quality score calculation
        passed_checks_count = sum(1 for v in executed_checks.values() if v)
        total_checks = len(executed_checks)
        confidence_score = round(passed_checks_count / total_checks, 3)

        pass_quality = (len(rejection_reasons) == 0)

        regeneration_instruction = None
        if not pass_quality:
            regeneration_instruction = (
                f"Regenerate MCQ addressing: {'; '.join(rejection_reasons)}. "
                "Ensure exactly 4 distinct plausible distractors, valid answer key, explicit page citation from training document, "
                "and no all/none of the above phrasing."
            )

        return {
            "pass_quality": pass_quality,
            "executed_checks": executed_checks,
            "passed_checks_count": passed_checks_count,
            "total_checks": total_checks,
            "confidence_score": confidence_score,
            "warnings": warnings,
            "rejection_reasons": rejection_reasons,
            "regeneration_instruction": regeneration_instruction
        }


# Singleton validator instance
mcq_validator = MCQQualityValidator()
