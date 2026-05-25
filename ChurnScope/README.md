# ChurnScope — Telco Customer Churn Prediction

A machine learning project that predicts customer churn probability using the IBM Watson Telco Customer Churn dataset. The project focuses on feature engineering, model comparison, and churn risk analysis using classical ML techniques.

---

## Overview

This project analyzes telecom customer behavior and predicts the likelihood of churn based on customer account details, subscription services, tenure, and billing information.

The workflow includes:

- Data cleaning and preprocessing
- Feature engineering
- Model training and evaluation
- Churn probability prediction
- Feature importance analysis

---

## Dataset

- **Source:** IBM Watson Telco Customer Churn Dataset
- **Records:** 7,043 customers
- **Features:** 21 customer attributes
- **Final Dataset:** 7,032 rows after removing missing values from `TotalCharges`

Dataset link:  
https://www.kaggle.com/datasets/blastchar/telco-customer-churn

---

## Models Evaluated

| Model | ROC-AUC | Recall (Churn) |
|---|---|---|
| Logistic Regression | 83.7% | 79% |
| Random Forest | 83.7% | 76% |
| **Gradient Boosting** 🏆 | **84.0%** | **78%** |
| XGBoost | 83.9% | 78% |

Gradient Boosting was selected as the final model based on the best overall ROC-AUC performance while maintaining strong churn recall.


---

## Feature Engineering

Custom engineered features were created to improve churn prediction performance, including:

- `ChargesPerTenure`
- `FiberNoAddons`
- `HighRiskCombo`
- `EasyLeaver`
- Contract and service interaction features

Preprocessing pipeline includes:

- `StandardScaler` for numerical features
- `OneHotEncoder` for categorical features
- `ColumnTransformer` integration for end-to-end preprocessing

---

## Model Performance

- **Production Model:** `GradientBoostingClassifier`
- **Evaluation Metric:** ROC-AUC
- **Final ROC-AUC:** **84.0%**
- **Focus:** High churn recall to minimize missed churners

Feature importances from the trained model are used to identify the most influential churn drivers.


---

## Project Structure

```bash
├── data/                    # IBM Watson Telco dataset
├── notebooks/               # EDA, preprocessing, feature engineering, model training
└── README.md
```

---

## Key Learnings

- Handling imbalanced classification problems
- Feature engineering using domain knowledge
- Comparing classical ML algorithms
- Evaluating models using ROC-AUC and recall
- Building preprocessing pipelines with scikit-learn

---

## Future Improvements

- Hyperparameter optimization
- SHAP-based explainability
- Deployment as a web application
- Real-time prediction API
- Automated retraining pipeline

---

## Author

Built by Kanan as a machine learning and data science project focused on customer churn analytics.