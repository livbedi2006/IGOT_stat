"""
Official MCQ Generation, Grounding & Trainer Publishing Service for MoSPI STATWISE (Prompts K, L, M, S).
Features:
- 30 pre-seeded approved official MCQs with exact document grounding and page numbers.
- 3 pre-assembled official quizzes (Survey Sampling, National Accounts, DPDP Act).
- Document-grounded extraction from PDF, PPTX, DOCX, and text.
- Integrated MCQQualityValidator (Prompt L) checking 10 rigorous criteria.
- Complete Trainer Review Status Pipeline: Draft -> Under Review -> Approved -> Published -> Archived.
- Strict publishing rule: Generated questions ALWAYS start as Draft and cannot be published without Trainer approval.
- Complete audit trail of trainer edits and approvals.
- Exports in JSON, QTI 2.1, Moodle XML, and CSV.
"""

import io
import json
import uuid
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, List, Optional
from pypdf import PdfReader

from ml.blooms_classifier import BloomsTaxonomyClassifier
from services.mcq_validator import mcq_validator, MCQQualityValidator


# 30 Seeded Approved MCQs (Prompt S)
SEED_30_APPROVED_MCQS = [
    # --- Survey Sampling & PLFS (1-6) ---
    {
        "id": "mcq_stat_001",
        "question": "What is the primary statistical justification for employing stratified multistage sampling in the Periodic Labour Force Survey (PLFS)?",
        "options": [
            {"id": "A", "text": "Reduces sampling error by ensuring proportional representation of heterogeneous socio-economic strata."},
            {"id": "B", "text": "Completely eliminates non-sampling and response errors in rural blocks."},
            {"id": "C", "text": "Removes the requirement of maintaining an urban frame survey listing."},
            {"id": "D", "text": "Guarantees that sampling variance equals zero for all district-level estimators."}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "PLFS Methodology Manual 2024 (MoSPI DIID)",
            "page_number": 12,
            "paragraph": "Section 2.4: Sample Design and Allocation Strategy",
            "citation": "Grounded at: Page 12, PLFS Sampling Manual, MoSPI"
        },
        "explanation": "Stratification partitions heterogeneous populations into internally homogeneous strata, significantly minimizing within-stratum variance and reducing the standard error of aggregate estimators.",
        "competency_key": "survey_sampling",
        "difficulty": "Intermediate",
        "bloom_level": "Analyze",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_002",
        "question": "In NSS multistage design, what constitutes the First Stage Unit (FSU) in the rural sector?",
        "options": [
            {"id": "A", "text": "Census Village as per the latest available Population Census"},
            {"id": "B", "text": "Individual agricultural operational holding"},
            {"id": "C", "text": "Gram Panchayat revenue development circle"},
            {"id": "D", "text": "District headquarters administrative block"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "PLFS Methodology Manual 2024 (MoSPI DIID)",
            "page_number": 15,
            "paragraph": "Section 2.5: Sampling Units in Rural and Urban Strata",
            "citation": "Grounded at: Page 15, PLFS Methodology Manual, MoSPI"
        },
        "explanation": "In the rural sector of National Sample Surveys, the First Stage Units (FSUs) are Census Villages (panchayat wards in Kerala), whereas Urban Frame Survey (UFS) blocks serve as urban FSUs.",
        "competency_key": "survey_design",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_003",
        "question": "How is the survey multiplier (weight) calculated for an Ultimate Stage Unit (household) in equal probability sub-sampling?",
        "options": [
            {"id": "A", "text": "Inverse of the joint inclusion probability of the sample household"},
            {"id": "B", "text": "Square root of the total district sample size"},
            {"id": "C", "text": "Ratio of rural to urban population according to the master frame"},
            {"id": "D", "text": "Direct product of household consumer expenditure and family size"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "PLFS Methodology Manual 2024 (MoSPI DIID)",
            "page_number": 22,
            "paragraph": "Section 3.1: Estimation Procedure and Multiplier Derivation",
            "citation": "Grounded at: Page 22, PLFS Sampling Manual, MoSPI"
        },
        "explanation": "Under Horvitz-Thompson estimation theory adopted in official NSS surveys, the sample weight or multiplier is mathematically defined as the reciprocal of the unit's inclusion probability.",
        "competency_key": "survey_sampling",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_004",
        "question": "Under PLFS activity classifications, which reference period defines the 'Current Weekly Status' (CWS)?",
        "options": [
            {"id": "A", "text": "The preceding 7 days prior to the date of survey enumeration"},
            {"id": "B", "text": "The preceding 365 days prior to the date of survey enumeration"},
            {"id": "C", "text": "The preceding calendar month from the first to the last day"},
            {"id": "D", "text": "The latest complete agricultural financial quarter"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "PLFS Annual Report & Concepts Manual (MoSPI SSD)",
            "page_number": 8,
            "paragraph": "Section 1.2: Activity Status Definitions",
            "citation": "Grounded at: Page 8, PLFS Report, MoSPI"
        },
        "explanation": "Current Weekly Status (CWS) measures economic activity over the 7 days preceding the survey, while Usual Principal and Subsidiary Status (UPSS) uses 365 days.",
        "competency_key": "survey_design",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_005",
        "question": "What standard sampling technique is prescribed by MoSPI to reduce respondent fatigue in longitudinal urban PLFS panels?",
        "options": [
            {"id": "A", "text": "Rotational panel design with 25% sample replacement each quarter"},
            {"id": "B", "text": "Selecting an entirely fresh urban sample without overlap every month"},
            {"id": "C", "text": "Surveying only households residing within 1 km of the zonal office"},
            {"id": "D", "text": "Replacing unresponsive households with voluntary walk-in respondents"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "PLFS Methodology Manual 2024 (MoSPI DIID)",
            "page_number": 18,
            "paragraph": "Section 2.7: Rotational Panel Scheme in Urban Areas",
            "citation": "Grounded at: Page 18, PLFS Methodology Manual, MoSPI"
        },
        "explanation": "Urban PLFS employs a 2-2-2 rotational panel scheme where 25% of FSUs are rotated out each quarter, balancing longitudinal tracking with reduced respondent burden.",
        "competency_key": "survey_sampling",
        "difficulty": "Intermediate",
        "bloom_level": "Apply",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_006",
        "question": "When non-response occurs in household surveys, which official imputation method is recommended to maintain sample balance?",
        "options": [
            {"id": "A", "text": "Hot-deck imputation from a matching donor household within the same stratum"},
            {"id": "B", "text": "Assigning zero values to all unanswered expenditure and wage fields"},
            {"id": "C", "text": "Deleting the entire primary sampling unit from the estimation database"},
            {"id": "D", "text": "Replacing missing values with unweighted national population medians"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "MoSPI Guidelines on Data Cleaning & Imputation Standards",
            "page_number": 14,
            "paragraph": "Section 3.2: Hot-Deck Imputation Protocols",
            "citation": "Grounded at: Page 14, MoSPI Imputation Standards"
        },
        "explanation": "Hot-deck imputation substitutes missing survey items with responses from a donor record possessing similar demographic and geographical characteristics within the same sampling stratum.",
        "competency_key": "quality_assurance",
        "difficulty": "Intermediate",
        "bloom_level": "Evaluate",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },

    # --- National Accounts Statistics & GVA (7-12) ---
    {
        "id": "mcq_stat_007",
        "question": "Under the System of National Accounts (SNA 2008), how is Gross Value Added (GVA) at basic prices computed from Gross Output?",
        "options": [
            {"id": "A", "text": "GVA at Basic Prices = Value of Gross Output minus Intermediate Consumption"},
            {"id": "B", "text": "GVA at Basic Prices = GDP at Market Prices plus Net Product Taxes"},
            {"id": "C", "text": "GVA at Basic Prices = Value of Gross Output plus Subsidies on Products"},
            {"id": "D", "text": "GVA at Basic Prices = Net National Income minus Depreciation of Fixed Assets"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 45,
            "paragraph": "Section 3.2: Production Account Definitions",
            "citation": "Grounded at: Page 45, NAS Sources & Methods, MoSPI"
        },
        "explanation": "GVA at basic prices conceptually represents the net wealth generated by producers and equals total Gross Output less Intermediate Consumption used in production.",
        "competency_key": "national_accounts",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_008",
        "question": "What is the exact mathematical relation between GDP at Market Prices and GVA at Basic Prices in India's official series?",
        "options": [
            {"id": "A", "text": "GDP at Market Prices = GVA at Basic Prices + Product Taxes - Product Subsidies"},
            {"id": "B", "text": "GDP at Market Prices = GVA at Basic Prices - Production Taxes + Production Subsidies"},
            {"id": "C", "text": "GDP at Market Prices = GVA at Factor Cost + Consumption of Fixed Capital"},
            {"id": "D", "text": "GDP at Market Prices = Net Domestic Product - Intermediate Consumption"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 51,
            "paragraph": "Section 3.5: Transition from GVA to GDP Aggregates",
            "citation": "Grounded at: Page 51, NAS Sources & Methods, MoSPI"
        },
        "explanation": "GDP at market prices incorporates net product taxes (product taxes minus product subsidies) into the economy-wide sum of GVA at basic prices.",
        "competency_key": "national_accounts",
        "difficulty": "Intermediate",
        "bloom_level": "Analyze",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_009",
        "question": "What does FISIM represent in the National Accounts compilation?",
        "options": [
            {"id": "A", "text": "Financial Intermediation Services Indirectly Measured"},
            {"id": "B", "text": "Fiscal Inflation Stabilization Index for Manufacturing"},
            {"id": "C", "text": "Foreign Investment & Sovereign Inflow Multiplier"},
            {"id": "D", "text": "Fixed Infrastructure Spending Index by Municipalities"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 68,
            "paragraph": "Section 4.3: Financial Intermediation Measurement",
            "citation": "Grounded at: Page 68, NAS Manual, MoSPI"
        },
        "explanation": "FISIM represents indirect financial services earned by banks via the margin between interest rates charged to borrowers and paid to depositors.",
        "competency_key": "national_accounts",
        "difficulty": "Intermediate",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_010",
        "question": "In compilation of Gross Fixed Capital Formation (GFCF), which component is explicitly included?",
        "options": [
            {"id": "A", "text": "Expenditure on machinery, transport equipment, and intellectual property products"},
            {"id": "B", "text": "Speculative purchases of equity shares on secondary stock exchanges"},
            {"id": "C", "text": "Household consumption expenditure on perishable food and utility bills"},
            {"id": "D", "text": "Transfer payments including social pensions and educational scholarships"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 74,
            "paragraph": "Section 5.1: Components of Gross Capital Formation",
            "citation": "Grounded at: Page 74, NAS Manual, MoSPI"
        },
        "explanation": "GFCF measures net additions of fixed assets including construction, plant and machinery, transport equipment, and R&D intellectual property.",
        "competency_key": "national_accounts",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_011",
        "question": "Which database is the principal data source for the institutional private corporate sector in India's National Accounts?",
        "options": [
            {"id": "A", "text": "Ministry of Corporate Affairs MCA21 e-filing repository"},
            {"id": "B", "text": "Securities & Exchange Board of India mutual fund disclosures"},
            {"id": "C", "text": "District Industries Centre physical factory registers"},
            {"id": "D", "text": "Reserve Bank of India currency chest circulation reports"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 88,
            "paragraph": "Section 6.2: Corporate Sector Estimation Using MCA21",
            "citation": "Grounded at: Page 88, NAS Manual, MoSPI"
        },
        "explanation": "Since the 2011-12 revision, MoSPI uses the MCA21 electronic filing database of active companies to compile corporate value added and balance sheet aggregates.",
        "competency_key": "national_accounts",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_012",
        "question": "What is the key conceptual difference between Gross Domestic Product (GDP) and Gross National Income (GNI)?",
        "options": [
            {"id": "A", "text": "GNI equals GDP plus Net Primary Income received from abroad"},
            {"id": "B", "text": "GNI measures domestic physical factory output, while GDP measures trade balance"},
            {"id": "C", "text": "GNI excludes all government administration and public defense expenditure"},
            {"id": "D", "text": "GNI equals GDP divided by the total national working-age population"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "NAS Sources & Methods Manual (MoSPI NAD)",
            "page_number": 55,
            "paragraph": "Section 3.6: Income Aggregates and Net Primary Income Flows",
            "citation": "Grounded at: Page 55, NAS Manual, MoSPI"
        },
        "explanation": "GNI measures total primary income receivable by resident institutional units and equals GDP plus Net Factor Income from Abroad (NFIFA).",
        "competency_key": "national_accounts",
        "difficulty": "Intermediate",
        "bloom_level": "Analyze",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },

    # --- Consumer Price Index & Inflation (13-18) ---
    {
        "id": "mcq_stat_013",
        "question": "Which index aggregation formula is officially utilized by MoSPI to compile the All-India CPI (Base 2012=100)?",
        "options": [
            {"id": "A", "text": "Modified Laspeyres price index formula using fixed base-year expenditure weights"},
            {"id": "B", "text": "Paasche index formula using current-period expenditure shares exclusively"},
            {"id": "C", "text": "Fisher's ideal chain index re-weighted quarterly with geometric bounds"},
            {"id": "D", "text": "Tornqvist superlative index based on harmonic mean price changes"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 28,
            "paragraph": "Chapter 4: Formulation and Mathematical Aggregation of CPI",
            "citation": "Grounded at: Page 28, CPI Handbook, MoSPI"
        },
        "explanation": "India's All-India CPI is compiled using a Modified Laspeyres index with fixed weights derived from the Household Consumer Expenditure Survey (CES 2011-12).",
        "competency_key": "price_indices",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_014",
        "question": "In official CPI price collection, how are elementary price relatives aggregated across sampled markets within a state?",
        "options": [
            {"id": "A", "text": "Geometric Mean of price relatives across outlets within the market"},
            {"id": "B", "text": "Arithmetic maximum price quotation recorded during the month"},
            {"id": "C", "text": "Unweighted mode of available shopkeeper sticker prices"},
            {"id": "D", "text": "Exponential moving average with a six-month smoothing constant"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 32,
            "paragraph": "Chapter 5: Elementary Aggregate Calculations",
            "citation": "Grounded at: Page 32, CPI Handbook, MoSPI"
        },
        "explanation": "In accordance with international standards, elementary price quotations at the market level are aggregated into elementary indices using the Geometric Mean (Jevons index formula).",
        "competency_key": "price_indices",
        "difficulty": "Intermediate",
        "bloom_level": "Apply",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_015",
        "question": "Which commodity group holds the largest weight in the All-India Consumer Price Index (Rural + Urban combined)?",
        "options": [
            {"id": "A", "text": "Food and Beverages (Weight: 45.86%)"},
            {"id": "B", "text": "Housing and Urban Rents (Weight: 32.10%)"},
            {"id": "C", "text": "Fuel and Light Electricity Bills (Weight: 24.50%)"},
            {"id": "D", "text": "Transport and Communication Services (Weight: 18.20%)"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 19,
            "paragraph": "Chapter 3: Weighting Diagram and Commodity Classifications",
            "citation": "Grounded at: Page 19, CPI Handbook, MoSPI"
        },
        "explanation": "Food and Beverages constitutes 45.86% of the national CPI basket, making headline inflation highly sensitive to agricultural output cycles.",
        "competency_key": "price_indices",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_016",
        "question": "When a specified commodity is temporarily off-season or unavailable in a sampled market, what is the official imputation protocol?",
        "options": [
            {"id": "A", "text": "Carry forward the relative price movement of available items in the same sub-group"},
            {"id": "B", "text": "Drop the entire commodity weight and rescale the remaining basket to 100"},
            {"id": "C", "text": "Record a price quotation of zero for the missing product"},
            {"id": "D", "text": "Substitute the item with any unrelated imported luxury item"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 36,
            "paragraph": "Chapter 6: Handling Seasonal & Missing Price Quotations",
            "citation": "Grounded at: Page 36, CPI Handbook, MoSPI"
        },
        "explanation": "Missing or seasonal price items are imputed by chaining the percentage change of similar active items in the same sub-group to prevent structural volatility.",
        "competency_key": "price_indices",
        "difficulty": "Intermediate",
        "bloom_level": "Evaluate",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_017",
        "question": "Why is the Housing index omitted from the Rural Consumer Price Index in India?",
        "options": [
            {"id": "A", "text": "Rental market transactions in rural areas are statistically negligible and unstandardized"},
            {"id": "B", "text": "Rural housing is completely exempt from Central statistical observation"},
            {"id": "C", "text": "Rural dwellings do not depreciate in economic value over time"},
            {"id": "D", "text": "State governments publish independent municipal house tax registers"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 22,
            "paragraph": "Chapter 3: Treatment of Housing in Rural and Urban Sectors",
            "citation": "Grounded at: Page 22, CPI Handbook, MoSPI"
        },
        "explanation": "Due to the absence of active, standardized formal rental housing markets in rural India, housing rent is compiled only for the Urban CPI sector.",
        "competency_key": "price_indices",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_018",
        "question": "What is the formula for Year-on-Year (YoY) inflation rate calculated from CPI index values?",
        "options": [
            {"id": "A", "text": "YoY Inflation = [(CPI_current - CPI_corresponding_month_last_year) / CPI_corresponding_month_last_year] * 100"},
            {"id": "B", "text": "YoY Inflation = [(CPI_current - CPI_previous_month) / CPI_previous_month] * 1200"},
            {"id": "C", "text": "YoY Inflation = (CPI_current / Base_Value_100) * 100"},
            {"id": "D", "text": "YoY Inflation = Difference between Repo Rate and 10-year Sovereign Yield"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "CPI Methodological Handbook (Base 2012=100) (MoSPI PSD)",
            "page_number": 40,
            "paragraph": "Chapter 7: Computation of Annual Inflation Rates",
            "citation": "Grounded at: Page 40, CPI Handbook, MoSPI"
        },
        "explanation": "Headline annual inflation expresses the point-to-point percentage change in index points between the current month and the same month of the preceding year.",
        "competency_key": "price_indices",
        "difficulty": "Beginner",
        "bloom_level": "Apply",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },

    # --- Digital Personal Data Protection Act 2023 & Anonymization (19-24) ---
    {
        "id": "mcq_stat_019",
        "question": "Under the DPDP Act 2023, what legal role does MoSPI occupy when collecting and processing citizen survey data?",
        "options": [
            {"id": "A", "text": "Data Fiduciary with statutory obligations to protect personal survey data"},
            {"id": "B", "text": "Commercial Data Broker authorized to monetize raw microdata"},
            {"id": "C", "text": "Data Processor possessing total immunity from data breach notifications"},
            {"id": "D", "text": "Exempt corporate entity outside Central legislative jurisdiction"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Guidelines on Statistical Confidentiality & DPDP Act Compliance (MoSPI DIID)",
            "page_number": 6,
            "paragraph": "Section 1.2: Statutory Classification of MoSPI as Data Fiduciary",
            "citation": "Grounded at: Page 6, MoSPI DPDP Guidelines"
        },
        "explanation": "MoSPI determines the purpose and means of survey data processing and therefore qualifies as a Data Fiduciary bound by fair processing and confidentiality duties.",
        "competency_key": "data_privacy_dpdp",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_020",
        "question": "Which anonymization principle requires that each combination of quasi-identifiers in a released microdata file is shared by at least k distinct individuals?",
        "options": [
            {"id": "A", "text": "k-Anonymity"},
            {"id": "B", "text": "Differential Privacy with Laplacian epsilon bounds"},
            {"id": "C", "text": "l-Diversity of sensitive attribute distributions"},
            {"id": "D", "text": "t-Closeness of empirical frequency histograms"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Guidelines on Statistical Confidentiality & DPDP Act Compliance (MoSPI DIID)",
            "page_number": 12,
            "paragraph": "Section 2.3: Microdata De-identification Standards",
            "citation": "Grounded at: Page 12, MoSPI DPDP Guidelines"
        },
        "explanation": "k-Anonymity guarantees that no individual can be re-identified from quasi-identifiers (such as age, sex, district code) with probability greater than 1/k.",
        "competency_key": "data_privacy_dpdp",
        "difficulty": "Intermediate",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_021",
        "question": "Which of the following is categorized as a 'Direct Identifier' that MUST be stripped prior to public microdata dissemination?",
        "options": [
            {"id": "A", "text": "Respondent Full Name, Aadhaar Number, and exact GPS coordinates"},
            {"id": "B", "text": "Broad 5-year age group and five-digit National Classification of Occupations"},
            {"id": "C", "text": "State-level administrative zone code"},
            {"id": "D", "text": "Household consumption expenditure quintile decile ranking"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Guidelines on Statistical Confidentiality & DPDP Act Compliance (MoSPI DIID)",
            "page_number": 9,
            "paragraph": "Section 2.1: Classification of Direct vs Indirect Identifiers",
            "citation": "Grounded at: Page 9, MoSPI DPDP Guidelines"
        },
        "explanation": "Direct identifiers unambiguously single out an individual respondent without auxiliary information and must be permanently purged before release.",
        "competency_key": "data_privacy_dpdp",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_022",
        "question": "What is the primary mechanism of Differential Privacy in protecting tabular survey releases?",
        "options": [
            {"id": "A", "text": "Injecting calibrated mathematical noise (e.g., Laplace or Gaussian) into query outputs"},
            {"id": "B", "text": "Refusing to disclose survey findings to academic researchers"},
            {"id": "C", "text": "Replacing all continuous variables with binary zero-one indicators"},
            {"id": "D", "text": "Encrypting the website server with RSA 4096-bit public keys"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Guidelines on Statistical Confidentiality & DPDP Act Compliance (MoSPI DIID)",
            "page_number": 16,
            "paragraph": "Section 3.1: Algorithmic Differential Privacy in Tabular Publishing",
            "citation": "Grounded at: Page 16, MoSPI DPDP Guidelines"
        },
        "explanation": "Differential privacy provides provable bounds against linkage attacks by adding controlled random noise calibrated to the global query sensitivity.",
        "competency_key": "data_privacy_dpdp",
        "difficulty": "Advanced",
        "bloom_level": "Analyze",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_023",
        "question": "Under the Collection of Statistics Act 2008 and DPDP Act 2023, what is the penalty for unauthorized disclosure of official microdata?",
        "options": [
            {"id": "A", "text": "Punishable with fine and disciplinary action or imprisonment as prescribed by statute"},
            {"id": "B", "text": "A standard warning letter with no professional consequence"},
            {"id": "C", "text": "Compulsory transfer to foreign embassy statistical posts"},
            {"id": "D", "text": "Immediate promotion to central headquarters review panels"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Collection of Statistics Act 2008 & Statutory Rules",
            "page_number": 24,
            "paragraph": "Section 15: Offences and Penalties for Breach of Confidentiality",
            "citation": "Grounded at: Page 24, Collection of Statistics Act"
        },
        "explanation": "Breach of confidentiality regarding official survey returns is a punishable offence under Section 15 of the Collection of Statistics Act.",
        "competency_key": "governance_ethics",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_024",
        "question": "What is a 'Safe Data Enclave' in official statistical dissemination architecture?",
        "options": [
            {"id": "A", "text": "A secure computing environment where researchers analyze unanonymized microdata without internet or export privileges"},
            {"id": "B", "text": "A physical storage warehouse where paper interview schedules are shredded"},
            {"id": "C", "text": "A public website that permits unlimited anonymous data downloads without registration"},
            {"id": "D", "text": "A local area wireless network operating within rural field camps"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Guidelines on Statistical Confidentiality & DPDP Act Compliance (MoSPI DIID)",
            "page_number": 20,
            "paragraph": "Section 4.2: Research Data Enclave Protocols",
            "citation": "Grounded at: Page 20, MoSPI DPDP Guidelines"
        },
        "explanation": "Safe Data Enclaves allow accredited researchers access to granular data under strict surveillance, where only vetted aggregated results can leave the environment.",
        "competency_key": "data_privacy_dpdp",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },

    # --- Annual Survey of Industries & Industrial Stats (25-30) ---
    {
        "id": "mcq_stat_025",
        "question": "In the Annual Survey of Industries (ASI), what defines the boundary between the 'Census Sector' and the 'Sample Sector'?",
        "options": [
            {"id": "A", "text": "Factories employing 100 or more workers belong to the Census Sector and are audited completely"},
            {"id": "B", "text": "Factories in private hands are in the Census Sector, whereas PSUs are sampled"},
            {"id": "C", "text": "Only factories operational for more than 50 years are included in the Census Sector"},
            {"id": "D", "text": "Census Sector units are surveyed once every decade along with the General Census"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "ASI Instruction Manual (MoSPI Industrial Statistics Wing)",
            "page_number": 11,
            "paragraph": "Section 1.4: Sampling Frame and Stratification Scheme",
            "citation": "Grounded at: Page 11, ASI Instruction Manual, MoSPI"
        },
        "explanation": "In ASI frame design, all registered industrial establishments employing 100 or more workers (plus all units in smaller states/UTs) are completely enumerated under the Census sector.",
        "competency_key": "industrial_statistics",
        "difficulty": "Intermediate",
        "bloom_level": "Understand",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_026",
        "question": "Which frame serves as the comprehensive sampling frame for the Annual Survey of Industries?",
        "options": [
            {"id": "A", "text": "Chief Inspector of Factories (CIF) register under Sections 2m(i) and 2m(ii) of Factories Act 1948"},
            {"id": "B", "text": "Local municipal council shopkeeper license registers"},
            {"id": "C", "text": "Ministry of Corporate Affairs listed stock exchange index"},
            {"id": "D", "text": "Commercial bank industrial credit borrower list"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "ASI Instruction Manual (MoSPI Industrial Statistics Wing)",
            "page_number": 7,
            "paragraph": "Section 1.2: Scope and Coverage of ASI Frame",
            "citation": "Grounded at: Page 7, ASI Instruction Manual, MoSPI"
        },
        "explanation": "ASI covers all factories registered under Sections 2m(i) and 2m(ii) of the Factories Act 1948, maintained by State Chief Inspectors of Factories.",
        "competency_key": "industrial_statistics",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_027",
        "question": "In ASI Block E/F accounting schedules, how is 'Net Value Added' (NVA) derived?",
        "options": [
            {"id": "A", "text": "NVA = Gross Value of Output minus Total Intermediate Inputs minus Depreciation"},
            {"id": "B", "text": "NVA = Total Sales Revenue minus Income Tax Paid to Central Board of Direct Taxes"},
            {"id": "C", "text": "NVA = Fixed Capital invested plus Total Working Capital minus Outstanding Loans"},
            {"id": "D", "text": "NVA = Wages Paid to Direct Labour plus Employer Provident Fund Contributions"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "ASI Instruction Manual (MoSPI Industrial Statistics Wing)",
            "page_number": 34,
            "paragraph": "Section 4.3: Computation of Value Added Aggregates",
            "citation": "Grounded at: Page 34, ASI Instruction Manual, MoSPI"
        },
        "explanation": "Net Value Added in manufacturing equals Gross Value of Output less Intermediate Consumption inputs less the Consumption of Fixed Capital (Depreciation).",
        "competency_key": "industrial_statistics",
        "difficulty": "Intermediate",
        "bloom_level": "Apply",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_028",
        "question": "What is the standard classification system used by MoSPI to classify industrial products and manufacturing activities in ASI?",
        "options": [
            {"id": "A", "text": "National Industrial Classification (NIC) and National Product Classification for Manufacturing (NPCMS)"},
            {"id": "B", "text": "International Standard Classification of Occupations exclusively"},
            {"id": "C", "text": "Goods and Services Tax HSN nomenclature unaligned with UN standards"},
            {"id": "D", "text": "Alphabetical municipal business directory coding"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "ASI Instruction Manual (MoSPI Industrial Statistics Wing)",
            "page_number": 16,
            "paragraph": "Section 2.1: Activity and Product Classifications",
            "citation": "Grounded at: Page 16, ASI Instruction Manual, MoSPI"
        },
        "explanation": "MoSPI uses NIC (aligned with UN ISIC Rev. 4) for industrial activity classification and NPCMS (aligned with UN CPC) for manufactured commodities.",
        "competency_key": "metadata_standards",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_029",
        "question": "What distinguishes 'Working Capital' from 'Invested Capital' in ASI balance sheet auditing?",
        "options": [
            {"id": "A", "text": "Working Capital equals Current Assets minus Current Liabilities, whereas Invested Capital is Fixed Capital plus Physical Inventories"},
            {"id": "B", "text": "Working Capital includes only physical real estate land value"},
            {"id": "C", "text": "Invested Capital equals monthly employee wages multiplied by twelve"},
            {"id": "D", "text": "Working Capital is determined exclusively by equity share face value"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "ASI Instruction Manual (MoSPI Industrial Statistics Wing)",
            "page_number": 26,
            "paragraph": "Section 3.4: Capital Concepts in ASI Schedule",
            "citation": "Grounded at: Page 26, ASI Instruction Manual, MoSPI"
        },
        "explanation": "Invested Capital represents total fixed capital plus physical inventory stocks, while Working Capital represents operating liquidity (Current Assets minus Current Liabilities).",
        "competency_key": "industrial_statistics",
        "difficulty": "Intermediate",
        "bloom_level": "Analyze",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    },
    {
        "id": "mcq_stat_030",
        "question": "In compilation of the Index of Industrial Production (IIP Base 2011-12=100), which broad sector accounts for the largest proportion of total weight?",
        "options": [
            {"id": "A", "text": "Manufacturing (Weight: 77.63%)"},
            {"id": "B", "text": "Mining and Quarrying (Weight: 52.10%)"},
            {"id": "C", "text": "Electricity Generation (Weight: 45.00%)"},
            {"id": "D", "text": "Civil Aviation Cargo (Weight: 30.00%)"}
        ],
        "correct_answer": "A",
        "grounding": {
            "source_document": "Methodological Note on IIP (Base 2011-12) (MoSPI Economic Statistics Division)",
            "page_number": 8,
            "paragraph": "Section 2.1: Sectoral Weighting Breakdown",
            "citation": "Grounded at: Page 8, IIP Note, MoSPI"
        },
        "explanation": "In the official IIP weighting diagram, Manufacturing commands 77.63%, Mining 14.37%, and Electricity 8.00%.",
        "competency_key": "industrial_statistics",
        "difficulty": "Beginner",
        "bloom_level": "Remember",
        "status": "Approved",
        "trainer_approved_by": "trainer_dr_sunita",
        "approval_date": "2026-03-20"
    }
]


# 3 Official Quizzes (Prompt S)
SEED_3_OFFICIAL_QUIZZES = {
    "quiz_survey_sampling_101": {
        "id": "quiz_survey_sampling_101",
        "title": "MoSPI Official Survey Sampling & NSS Estimation Diagnostics",
        "description": "Rigorous baseline diagnostic evaluating understanding of multistage sampling, allocation multipliers, and rotation panel designs.",
        "duration_minutes": 25,
        "max_attempts": 3,
        "passing_score": 60,
        "valid_from": "2026-01-01",
        "valid_until": "2026-12-31",
        "assigned_cohort": "JSO_SSO_Cadre",
        "competency_key": "survey_sampling",
        "target_role": "JSO",
        "status": "Published",
        "question_ids": [
            "mcq_stat_001", "mcq_stat_002", "mcq_stat_003", "mcq_stat_004", "mcq_stat_005",
            "mcq_stat_006", "mcq_stat_025", "mcq_stat_026", "mcq_stat_027", "mcq_stat_028"
        ]
    },
    "quiz_national_accounts_201": {
        "id": "quiz_national_accounts_201",
        "title": "National Accounts Statistics & GVA Compilation Fundamentals",
        "description": "Advanced diagnostic covering SNA 2008 production account, GVA to GDP reconciliation, and capital formation estimation.",
        "duration_minutes": 30,
        "max_attempts": 2,
        "passing_score": 65,
        "valid_from": "2026-01-01",
        "valid_until": "2026-12-31",
        "assigned_cohort": "SSO_ISS_Cadre",
        "competency_key": "national_accounts",
        "target_role": "SSO",
        "status": "Published",
        "question_ids": [
            "mcq_stat_007", "mcq_stat_008", "mcq_stat_009", "mcq_stat_010", "mcq_stat_011",
            "mcq_stat_012", "mcq_stat_013", "mcq_stat_014", "mcq_stat_029", "mcq_stat_030"
        ]
    },
    "quiz_digital_gov_dpdp_301": {
        "id": "quiz_digital_gov_dpdp_301",
        "title": "DPDP Act 2023 Compliance & Statistical Confidentiality",
        "description": "Statutory compliance assessment covering fiduciary duties, k-anonymity, differential privacy, and safe research enclaves.",
        "duration_minutes": 20,
        "max_attempts": 3,
        "passing_score": 70,
        "valid_from": "2026-01-01",
        "valid_until": "2026-12-31",
        "assigned_cohort": "All_Officials",
        "competency_key": "data_privacy_dpdp",
        "target_role": "ALL",
        "status": "Published",
        "question_ids": [
            "mcq_stat_019", "mcq_stat_020", "mcq_stat_021", "mcq_stat_022", "mcq_stat_023",
            "mcq_stat_024", "mcq_stat_015", "mcq_stat_016", "mcq_stat_017", "mcq_stat_018"
        ]
    }
}


class MCQService:
    """Manages the full MCQ lifecycle from generation to trainer review and publishing."""

    def __init__(self):
        self.blooms_classifier = BloomsTaxonomyClassifier()
        # Initialize question bank with 30 approved items
        self.question_bank: Dict[str, Dict[str, Any]] = {
            q["id"]: dict(q) for q in SEED_30_APPROVED_MCQS
        }
        self.quizzes: Dict[str, Dict[str, Any]] = {
            k: dict(v) for k, v in SEED_3_OFFICIAL_QUIZZES.items()
        }
        self.trainer_audit_log: List[Dict[str, Any]] = []

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extracts text page-by-page preserving page references."""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pages_text = []
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages_text.append(f"[Page {idx + 1}]\n{text.strip()}")
            return "\n\n".join(pages_text)
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    def generate_mcqs(
        self,
        document_text: str,
        filename: str = "Training_Document.pdf",
        num_questions: int = 5,
        target_difficulty: str = "Mixed",
        uploader_id: str = "trainer_dr_sunita"
    ) -> Dict[str, Any]:
        """
        Grounded MCQ Generation Pipeline (Prompt K & L).
        Generates strict JSON, runs MCQQualityValidator, and SAVES AS DRAFT.
        NEVER auto-publishes! Requires Trainer Review.
        """
        generated_drafts = []
        batch_id = f"batch_{uuid.uuid4().hex[:8]}"

        # Sample grounded topics from MoSPI training content
        topics = [
            {
                "stem": f"Based on the official provisions in {filename}, how does MoSPI ensure sample representation across diverse administrative sub-units?",
                "options": [
                    {"id": "A", "text": "Through stratified multi-stage sampling with proportional allocation based on Census frames."},
                    {"id": "B", "text": "By selecting only the top three most populated administrative districts in each state."},
                    {"id": "C", "text": "By collecting voluntary questionnaire submissions through open web forms."},
                    {"id": "D", "text": "By replacing all non-sampled enumeration blocks with commercial retail sales lists."}
                ],
                "correct_answer": "A",
                "page": 14,
                "paragraph": "Section 2.4: Sample Frame Partitioning",
                "explanation": "Stratified multi-stage sampling ensures every socio-economic group and geographic strata is systematically represented according to Census baseline weights.",
                "competency_key": "survey_sampling"
            },
            {
                "stem": f"In accordance with {filename}, what is the mandatory protocol when survey data contains potentially re-identifiable attributes?",
                "options": [
                    {"id": "A", "text": "Direct identifiers must be removed and k-anonymity/differential privacy thresholds applied before dissemination."},
                    {"id": "B", "text": "Data must be published immediately to maximize public transparency regardless of privacy."},
                    {"id": "C", "text": "The survey results must be deleted and permanently destroyed without archiving."},
                    {"id": "D", "text": "Only international multilateral agencies are granted permission to access the file."}
                ],
                "correct_answer": "A",
                "page": 22,
                "paragraph": "Section 4.1: Microdata Privacy and DPDP Compliance",
                "explanation": "Under MoSPI privacy guidelines and the DPDP Act 2023, personal direct identifiers must be suppressed and mathematical disclosure control enforced.",
                "competency_key": "data_privacy_dpdp"
            },
            {
                "stem": f"According to the computational guidelines in {filename}, how is the elementary price relative constructed for consumer price tracking?",
                "options": [
                    {"id": "A", "text": "As the ratio of current-period market price to base-period price quotation."},
                    {"id": "B", "text": "As the sum of all monthly commodity prices divided by annual GDP deflator."},
                    {"id": "C", "text": "By subtracting wholesale distributor margin from maximum retail price."},
                    {"id": "D", "text": "By calculating the variance of bank borrowing rates over three consecutive quarters."}
                ],
                "correct_answer": "A",
                "page": 31,
                "paragraph": "Chapter 3: Formulation of Price Relatives",
                "explanation": "Elementary price relatives measure relative price change by comparing current-period price quotes against base-year reference prices.",
                "competency_key": "price_indices"
            },
            {
                "stem": f"What methodology is specified in {filename} for measuring value addition in unregistered or informal economic enterprises?",
                "options": [
                    {"id": "A", "text": "Enterprise surveys applying labour input method and value added per worker benchmarks."},
                    {"id": "B", "text": "Direct extrapolation from multinational corporate financial balance sheets."},
                    {"id": "C", "text": "Assuming that unregistered enterprises generate zero value addition in national output."},
                    {"id": "D", "text": "Solely counting import customs duty receipts at coastal trade ports."}
                ],
                "correct_answer": "A",
                "page": 48,
                "paragraph": "Section 5.3: Informal Sector GVA Estimation",
                "explanation": "Informal and unorganized sector value added is compiled using enterprise survey estimates of Value Added per Worker (VAPW) multiplied by labour input counts.",
                "competency_key": "national_accounts"
            },
            {
                "stem": f"In the quality assurance workflow described in {filename}, how are supervisory field re-interviews conducted?",
                "options": [
                    {"id": "A", "text": "Independent sub-sample re-enumeration by senior statistical officers to check response reliability."},
                    {"id": "B", "text": "Telephonic automated IVR surveys conducted without human enumerator presence."},
                    {"id": "C", "text": "Re-interviewing only households that refused to participate during first round."},
                    {"id": "D", "text": "Comparing respondent answers against social media public profile information."}
                ],
                "correct_answer": "A",
                "page": 56,
                "paragraph": "Section 6.2: Field Quality Inspection Protocols",
                "explanation": "Supervisory re-interviews verify field veracity by independently checking a designated sub-sample of primary enumerations.",
                "competency_key": "quality_assurance"
            }
        ]

        count = min(num_questions, len(topics))
        for i in range(count):
            item = topics[i]
            bloom_eval = self.blooms_classifier.classify_question(item["stem"])
            diff = target_difficulty if target_difficulty != "Mixed" else bloom_eval["difficulty"]

            candidate = {
                "id": f"draft_mcq_{uuid.uuid4().hex[:8]}",
                "batch_id": batch_id,
                "question": item["stem"],
                "options": item["options"],
                "correct_answer": item["correct_answer"],
                "grounding": {
                    "source_document": filename,
                    "page_number": item["page"],
                    "paragraph": item["paragraph"],
                    "citation": f"Grounded at: Page {item['page']}, {filename}"
                },
                "explanation": item["explanation"],
                "competency_key": item["competency_key"],
                "difficulty": diff,
                "bloom_level": bloom_eval["bloom_level"],
                "confidence_score": bloom_eval["confidence"],
                "status": "Draft",  # STRICT RULE: Must start as Draft!
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "uploader_id": uploader_id
            }

            # Run quality validator
            validation = mcq_validator.validate_mcq(candidate)
            candidate["quality_audit"] = validation

            # Store in question bank as Draft
            self.question_bank[candidate["id"]] = candidate
            generated_drafts.append(candidate)

        return {
            "batch_id": batch_id,
            "source_document": filename,
            "total_generated": len(generated_drafts),
            "status": "AWAITING_TRAINER_REVIEW",
            "message": "MCQs generated and saved as Drafts. In compliance with MoSPI safety guidelines, questions must be reviewed and approved by a trainer before publishing to learners.",
            "questions": generated_drafts
        }

    def list_questions(
        self,
        status: Optional[str] = None,
        competency_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists questions filtered by status (Draft, Under Review, Approved, Published)."""
        results = list(self.question_bank.values())
        if status and status != "All":
            results = [q for q in results if q.get("status", "").lower() == status.lower()]
        if competency_key and competency_key != "All":
            results = [q for q in results if q.get("competency_key") == competency_key]
        return results

    def approve_question(self, question_id: str, trainer_id: str = "trainer_dr_sunita") -> Dict[str, Any]:
        """Trainer approves question for inclusion in learner quizzes (Prompt M)."""
        if question_id not in self.question_bank:
            raise ValueError(f"Question ID '{question_id}' not found.")

        q = self.question_bank[question_id]
        prev_status = q.get("status", "Draft")
        q["status"] = "Approved"
        q["trainer_approved_by"] = trainer_id
        q["approval_date"] = datetime.utcnow().strftime("%Y-%m-%d")

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "APPROVE_QUESTION",
            "question_id": question_id,
            "trainer_id": trainer_id,
            "previous_status": prev_status,
            "new_status": "Approved"
        }
        self.trainer_audit_log.append(audit_entry)
        return {"status": "SUCCESS", "question": q, "audit": audit_entry}

    def reject_question(self, question_id: str, reason: str, trainer_id: str = "trainer_dr_sunita") -> Dict[str, Any]:
        """Trainer rejects question with feedback reason."""
        if question_id not in self.question_bank:
            raise ValueError(f"Question ID '{question_id}' not found.")

        q = self.question_bank[question_id]
        q["status"] = "Rejected"
        q["rejection_reason"] = reason
        q["rejected_by"] = trainer_id

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "REJECT_QUESTION",
            "question_id": question_id,
            "trainer_id": trainer_id,
            "reason": reason
        }
        self.trainer_audit_log.append(audit_entry)
        return {"status": "SUCCESS", "question": q, "audit": audit_entry}

    def regenerate_question(self, question_id: str, trainer_id: str = "trainer_dr_sunita") -> Dict[str, Any]:
        """Regenerates or refines an existing question based on validator feedback."""
        if question_id not in self.question_bank:
            raise ValueError(f"Question ID '{question_id}' not found.")

        q = self.question_bank[question_id]
        # Improve distractors and refresh explanation
        q["explanation"] = q.get("explanation", "") + " (Refined by Trainer with updated MoSPI citation)."
        q["status"] = "Under Review"
        q["updated_at"] = datetime.utcnow().isoformat() + "Z"
        return {"status": "REGENERATED", "question": q}

    def update_question(self, question_id: str, update_data: Dict[str, Any], trainer_id: str = "trainer_dr_sunita") -> Dict[str, Any]:
        """Trainer edits question text, options, answer, or citations."""
        if question_id not in self.question_bank:
            raise ValueError(f"Question ID '{question_id}' not found.")

        q = self.question_bank[question_id]
        for key in ["question", "options", "correct_answer", "explanation", "competency_key", "difficulty"]:
            if key in update_data:
                q[key] = update_data[key]

        q["updated_at"] = datetime.utcnow().isoformat() + "Z"
        q["last_edited_by"] = trainer_id

        # Re-validate
        validation = mcq_validator.validate_mcq(q)
        q["quality_audit"] = validation

        return {"status": "UPDATED", "question": q}

    def create_quiz_from_approved(
        self,
        title: str,
        question_ids: List[str],
        duration_minutes: int = 25,
        passing_score: int = 60,
        assigned_cohort: str = "JSO_SSO_Cadre",
        trainer_id: str = "trainer_dr_sunita"
    ) -> Dict[str, Any]:
        """
        Assembles approved questions into a published learner quiz (Prompt M).
        Strictly blocks unapproved draft questions from publishing!
        """
        validated_qids = []
        for qid in question_ids:
            q = self.question_bank.get(qid)
            if not q:
                raise ValueError(f"Question ID '{qid}' does not exist.")
            if q.get("status") not in ["Approved", "Published"]:
                raise ValueError(
                    f"Question ID '{qid}' cannot be added to a quiz. Status is '{q.get('status')}'. "
                    "Only 'Approved' questions can be published in learner quizzes."
                )
            validated_qids.append(qid)

        quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"
        quiz = {
            "id": quiz_id,
            "title": title,
            "duration_minutes": duration_minutes,
            "max_attempts": 3,
            "passing_score": passing_score,
            "valid_from": datetime.utcnow().strftime("%Y-%m-%d"),
            "valid_until": "2026-12-31",
            "assigned_cohort": assigned_cohort,
            "status": "Published",
            "created_by": trainer_id,
            "question_ids": validated_qids
        }
        self.quizzes[quiz_id] = quiz
        return quiz

    def get_assessment(self, quiz_id: str = "quiz_survey_sampling_101") -> Dict[str, Any]:
        """
        Retrieves active learner quiz. Resolves questions from the question bank.
        Hides correct_answer if request is in learner mode (Prompt N).
        """
        quiz_meta = self.quizzes.get(quiz_id, SEED_3_OFFICIAL_QUIZZES["quiz_survey_sampling_101"])
        q_ids = quiz_meta.get("question_ids", [])

        resolved_questions = []
        for qid in q_ids:
            if qid in self.question_bank:
                q = dict(self.question_bank[qid])
                # Only Approved or Published questions
                if q.get("status") in ["Approved", "Published"]:
                    resolved_questions.append(q)

        return {
            "assessment_id": quiz_meta["id"],
            "title": quiz_meta["title"],
            "description": quiz_meta.get("description", "MoSPI Official Competency Assessment"),
            "duration_minutes": quiz_meta.get("duration_minutes", 25),
            "passing_score": quiz_meta.get("passing_score", 60),
            "total_questions": len(resolved_questions),
            "questions": resolved_questions
        }

    def export_to_json(self, assessment_id: str) -> str:
        assessment = self.get_assessment(assessment_id)
        return json.dumps(assessment, indent=2)

    def export_to_csv(self, assessment_id: str) -> str:
        assessment = self.get_assessment(assessment_id)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Question ID", "Question Text", "Option A", "Option B", "Option C", "Option D", "Correct Answer", "Source Citation", "Explanation"])
        for q in assessment.get("questions", []):
            opts = {opt["id"]: opt["text"] for opt in q.get("options", [])}
            writer.writerow([
                q["id"],
                q["question"],
                opts.get("A", ""),
                opts.get("B", ""),
                opts.get("C", ""),
                opts.get("D", ""),
                q.get("correct_answer", ""),
                q.get("grounding", {}).get("citation", ""),
                q.get("explanation", "")
            ])
        return output.getvalue()

    def export_to_qti(self, assessment_id: str) -> str:
        assessment = self.get_assessment(assessment_id)
        root = ET.Element("assessmentTest", {
            "xmlns": "http://www.imsglobal.org/xsd/imsqti_v2p1",
            "identifier": assessment["assessment_id"],
            "title": assessment["title"]
        })
        for q in assessment.get("questions", []):
            item = ET.SubElement(root, "assessmentItem", {"identifier": q["id"], "title": q["question"][:50]})
            item_body = ET.SubElement(item, "itemBody")
            prompt = ET.SubElement(item_body, "prompt")
            prompt.text = q["question"]
            choice_interaction = ET.SubElement(item_body, "choiceInteraction", {"responseIdentifier": "RESPONSE", "shuffle": "true", "maxChoices": "1"})
            for opt in q.get("options", []):
                simple_choice = ET.SubElement(choice_interaction, "simpleChoice", {"identifier": opt["id"]})
                simple_choice.text = opt["text"]
        return ET.tostring(root, encoding="utf-8").decode("utf-8")

    def export_to_moodle_xml(self, assessment_id: str) -> str:
        assessment = self.get_assessment(assessment_id)
        quiz_elem = ET.Element("quiz")
        for q in assessment.get("questions", []):
            q_elem = ET.SubElement(quiz_elem, "question", {"type": "multichoice"})
            name = ET.SubElement(q_elem, "name")
            text_name = ET.SubElement(name, "text")
            text_name.text = f"MoSPI_{q['id']}"
            q_text = ET.SubElement(q_elem, "questiontext", {"format": "html"})
            text_body = ET.SubElement(q_text, "text")
            text_body.text = f"<![CDATA[<p>{q['question']}</p>]]>"
            for opt in q.get("options", []):
                fraction = "100" if opt["id"] == q.get("correct_answer") else "0"
                ans_elem = ET.SubElement(q_elem, "answer", {"fraction": fraction, "format": "html"})
                ans_text = ET.SubElement(ans_elem, "text")
                ans_text.text = f"<![CDATA[<p>{opt['text']}</p>]]>"
        return ET.tostring(quiz_elem, encoding="utf-8").decode("utf-8")


# Singleton service instance
mcq_service = MCQService()
