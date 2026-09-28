
============================================================
CONSTRUCTION INTELLIGENCE HUB
MILESTONE 3 — COMPLIANCE + INSURANCE INTELLIGENCE
VERSION 1.0
============================================================

PURPOSE
-------
This package contains the backend-ready machine learning
artifacts for Milestone 3 of the Construction Intelligence Hub.

COMPONENTS
----------

1. COMPLIANCE INTELLIGENCE
--------------------------
Model:
RandomForestClassifier

Purpose:
Predict compliance risk category from multi-agency violation
and regulatory indicators.

Risk Categories:
- Low
- Medium
- High

5-Fold Cross-Validation:
Accuracy : 0.8421 ± 0.0029
Precision: 0.5830 ± 0.0067
Recall   : 0.7341 ± 0.0116
F1 Score : 0.6240 ± 0.0086

Dataset Records:
76,310

Important:
The risk category was derived from the source dataset's
risk_score using predefined score ranges. The model therefore
approximates the dataset's risk categorization from compliance
indicators.

------------------------------------------------------------

2. INSURANCE INTELLIGENCE
-------------------------
Model:
RandomForestClassifier

Purpose:
Provide insurance claim-risk intelligence and claim likelihood
support.

5-Fold Cross-Validation:
Accuracy : 0.6901 ± 0.0061
Precision: 0.0989 ± 0.0036
Recall   : 0.4741 ± 0.0154
F1 Score : 0.1637 ± 0.0058
ROC-AUC  : 0.6380 ± 0.0096

Dataset Records:
58,592

Important:
The source dataset is a vehicle insurance claims dataset,
not a construction-specific insurance dataset. It is used as
a supporting insurance-risk intelligence model and should not
be represented as construction claims data.

------------------------------------------------------------

BACKEND INTEGRATION
-------------------

Both models are saved as complete Scikit-learn Pipelines.

This means the backend does NOT need to separately implement
the preprocessing logic.

Recommended loading:

    import pickle

    with open("insurance_intelligence_model.pkl", "rb") as f:
        insurance_model = pickle.load(f)

    prediction = insurance_model.predict(input_data)
    probability = insurance_model.predict_proba(input_data)

The same approach can be used for the compliance model.

------------------------------------------------------------

FILES
-----

compliance_intelligence_model/
    compliance_intelligence_model.pkl
    compliance_intelligence_features.pkl
    metadata.json

insurance_intelligence_model/
    insurance_intelligence_model.pkl
    insurance_intelligence_features.pkl
    metadata.json

milestone_3_metadata.json
README.md

------------------------------------------------------------

VERSION
-------

Milestone 3 Package Version: v1.0

Status:
BACKEND READY

============================================================
