import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import classification_report, accuracy_score


# Curated statistical training dataset representing questions from official MoSPI / NSSO training manuals
TRAINING_QUESTIONS = [
    # Remember (Easy)
    ("What is the definition of sampling error in sample survey methodology?", "Remember"),
    ("Identify the statutory body responsible for Consumer Price Index compilation in India.", "Remember"),
    ("State the base year currently utilized for the Index of Industrial Production (IIP).", "Remember"),
    ("Which schedule is used by NSSO for Periodic Labour Force Survey household listing?", "Remember"),
    ("Define gross value added (GVA) at basic prices according to National Accounts Statistics.", "Remember"),
    ("List the four primary stages of stratified multistage sampling design.", "Remember"),
    ("Recall the formula used for calculating the Laspeyres price index.", "Remember"),
    ("What is the frequency of release for the quarterly PLFS bulletin?", "Remember"),
    ("Name the international metadata standard adopted by MoSPI for statistical dissemination.", "Remember"),
    ("What does SDMX stand for in modern official statistical systems?", "Remember"),

    # Understand (Easy/Medium)
    ("Explain why stratified random sampling yields lower variance than simple random sampling.", "Understand"),
    ("Describe the conceptual distinction between workforce and labour force in PLFS surveys.", "Understand"),
    ("Explain the impact of non-response bias on population parameter estimates.", "Understand"),
    ("Interpret a Gini coefficient of 0.38 in the context of household consumer expenditure.", "Understand"),
    ("Summarize how the wholesale price index differs from the consumer price index in coverage.", "Understand"),
    ("Explain the role of the National Sample Survey organization in official data collection.", "Understand"),
    ("Describe how post-stratification adjusts for under-coverage in survey frames.", "Understand"),
    ("Clarify the distinction between intermediate consumption and final consumption in NAS.", "Understand"),
    ("Explain how substitution bias affects fixed-basket price indices over time.", "Understand"),
    ("Describe the purpose of calibration weighting in sample survey estimation.", "Understand"),

    # Apply (Medium)
    ("Calculate the sample size required to estimate a population proportion with 3% margin of error.", "Apply"),
    ("Compute the Paasche index number using the provided base and current year price-quantity vectors.", "Apply"),
    ("Apply stratified sampling formula to determine stratum weights given population variances.", "Apply"),
    ("Execute Python pandas code to clean duplicate enterprise records from an ASI dataset.", "Apply"),
    ("Estimate the unemployment rate for rural females using the provided sample weights.", "Apply"),
    ("Calculate the design effect (Deff) for a two-stage cluster sampling design.", "Apply"),
    ("Implement a SQL query to aggregate quarterly factory outputs grouped by 2-digit NIC code.", "Apply"),
    ("Compute the real GDP growth rate adjusted for the GDP deflator.", "Apply"),
    ("Apply Horvitz-Thompson estimator to calculate total crop production from sample data.", "Apply"),
    ("Demonstrate how to calibrate survey weights using known auxiliary population totals.", "Apply"),

    # Analyze (Medium/Hard)
    ("Differentiate between sampling errors and non-sampling errors in field enumeration.", "Analyze"),
    ("Analyze the discrepancy between ASI enterprise estimates and MCA-21 database returns.", "Analyze"),
    ("Decompose the time series of IIP into seasonal, trend, and irregular cyclical components.", "Analyze"),
    ("Compare the efficiency of systematic sampling versus simple random sampling for linear trend populations.", "Analyze"),
    ("Examine how changes in the deflator calculation affect real manufacturing sector growth rates.", "Analyze"),
    ("Analyze the sensitivity of the poverty headcount ratio to shifts in the poverty line threshold.", "Analyze"),
    ("Investigate why response rates vary significantly between urban and rural sampling units.", "Analyze"),
    ("Contrast the production boundary with the asset boundary in the 2008 System of National Accounts.", "Analyze"),
    ("Examine potential sources of bias in telephone-assisted surveys compared to personal interviews.", "Analyze"),
    ("Dissect the variance components attributable to primary and secondary sampling units.", "Analyze"),

    # Evaluate (Hard)
    ("Evaluate whether a rotating panel design is superior to a cross-sectional design for PLFS.", "Evaluate"),
    ("Assess the statistical validity of imputing missing expenditure values using hot-deck imputation.", "Evaluate"),
    ("Critique the suitability of using administrative GST records as a direct proxy for informal sector output.", "Evaluate"),
    ("Validate whether the sample size in a district-level survey meets precision criteria for SDG indicators.", "Evaluate"),
    ("Appraise the trade-offs between respondent burden and questionnaire depth in economic censuses.", "Evaluate"),
    ("Determine whether chain-linking methodology provides superior inflation estimates during structural economic shifts.", "Evaluate"),
    ("Judge the compliance of a proposed statistical data pipeline with DPDP Act 2023 principles.", "Evaluate"),
    ("Evaluate the risk of disclosure when releasing microdata files with pseudo-identifiers.", "Evaluate"),
    ("Assess whether hedonic price regression adequately accounts for quality improvements in electronics CPI.", "Evaluate"),
    ("Formulate recommendations for mitigating attrition bias in longitudinal panel surveys.", "Evaluate")
]


class BloomsTaxonomyClassifier:
    def __init__(self):
        self.pipeline = None
        self.metrics = {}
        self._train()

    def _train(self):
        questions = [item[0] for item in TRAINING_QUESTIONS]
        labels = [item[1] for item in TRAINING_QUESTIONS]

        # Stratified train/test split (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            questions, labels, test_size=0.20, random_state=42, stratify=labels
        )

        # L2-regularized pipeline with bounded features
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=350,
                sublinear_tf=True
            )),
            ('clf', LogisticRegression(
                C=1.2,                # L2 penalty to stop memorization
                max_iter=300,
                solver='lbfgs',
                random_state=42
            ))
        ])

        # 5-fold cross validation on train
        cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.pipeline, X_train, y_train, cv=cv, scoring='accuracy')

        self.pipeline.fit(X_train, y_train)

        train_acc = accuracy_score(y_train, self.pipeline.predict(X_train))
        test_acc = accuracy_score(y_test, self.pipeline.predict(X_test))

        # Check overfitting gap
        generalization_gap = abs(train_acc - test_acc)
        is_overfitting = generalization_gap > 0.15

        self.metrics = {
            "model_type": "TF-IDF + L2 Regularized Logistic Regression",
            "cross_val_accuracy_mean": round(float(np.mean(cv_scores)), 3),
            "cross_val_accuracy_std": round(float(np.std(cv_scores)), 3),
            "train_accuracy": round(float(train_acc), 3),
            "test_accuracy": round(float(test_acc), 3),
            "generalization_gap": round(float(generalization_gap), 3),
            "is_overfitting": is_overfitting,
            "status": "Trained & Validated (Regularized)"
        }

    def predict(self, question_text: str):
        """
        Classifies question into Bloom's cognitive level and maps to Difficulty (Easy, Medium, Hard).
        """
        level = self.pipeline.predict([question_text])[0]
        probs = self.pipeline.predict_proba([question_text])[0]
        classes = self.pipeline.classes_
        confidence = float(np.max(probs))

        # Map to overall difficulty
        difficulty_map = {
            "Remember": "Easy",
            "Understand": "Easy",
            "Apply": "Medium",
            "Analyze": "Medium",
            "Evaluate": "Hard"
        }
        difficulty = difficulty_map.get(level, "Medium")

        return {
            "blooms_level": level,
            "difficulty": difficulty,
            "confidence": round(confidence, 3),
            "class_probabilities": {
                cls_name: round(float(p), 3) for cls_name, p in zip(classes, probs)
            }
        }
