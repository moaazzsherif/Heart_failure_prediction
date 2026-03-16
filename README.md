# 🫀 Heart Failure Prediction

> A machine learning project for predicting heart disease using clinical patient data, featuring a full interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4%2B-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📊 Results

| Metric | Score |
|--------|-------|
| ✅ Accuracy | **94.6%** |
| ⚡ F1 Score | **95.1%** |
| 🔬 Precision | **95.1%** |
| 🩺 Recall | **95.1%** |
| 📈 ROC-AUC | **0.961** |

> Best model: **Gradient Boosting** · Tuned threshold: **0.39** · 918 patients

---

## 🗂 Project Structure

```
heart-failure-prediction/
│
├── Heart_failure_clean.ipynb   # Main notebook — EDA, preprocessing, modeling
├── heart.csv                   # Dataset (918 patients, 12 features)
├── app_final.py                # Streamlit dashboard
├── requirements.txt            # Python dependencies
├── heart_model.pkl             # Saved model (generated after running notebook)
├── scaler.pkl                  # Saved scaler (generated after running notebook)
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/heart-failure-prediction.git
cd heart-failure-prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run app_final.py
```

### 4. Or open the notebook
```bash
jupyter notebook Heart_failure_clean.ipynb
```

---

## 📋 Dataset

**Source:** [Heart Failure Prediction Dataset — Kaggle](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction)

918 patients · 12 features · Binary classification (Heart Disease: 0 / 1)

| Feature | Type | Description |
|---------|------|-------------|
| Age | Numerical | Patient age in years |
| Sex | Categorical | M / F |
| ChestPainType | Categorical | ASY / ATA / NAP / TA |
| RestingBP | Numerical | Resting blood pressure (mmHg) |
| Cholesterol | Numerical | Serum cholesterol (mg/dL) |
| FastingBS | Binary | Fasting blood sugar > 120 mg/dL |
| RestingECG | Categorical | Normal / ST / LVH |
| MaxHR | Numerical | Maximum heart rate achieved |
| ExerciseAngina | Binary | Exercise-induced angina Y / N |
| Oldpeak | Numerical | ST depression induced by exercise |
| ST_Slope | Categorical | Up / Flat / Down |
| **HeartDisease** | **Target** | **0 = No Disease · 1 = Disease** |

---

## 🔬 Notebook Pipeline

```
1. Data Loading & EDA
      ↓
2. Data Cleaning
   · RestingBP = 0  → replaced with min per class
   · Cholesterol = 0 → replaced with min per class
   · Oldpeak outliers → clipped
      ↓
3. Feature Engineering
   · AgeGroup  (Young / Middle / Senior / Elder)
   · ST_Level  (Low / Normal / High based on Oldpeak)
      ↓
4. Encoding
   · Label Encoding  → Sex, ExerciseAngina, ST_Slope, AgeGroup, ST_Level
   · One-Hot Encoding → ChestPainType, RestingECG
      ↓
5. Train / Test Split  (80% / 20%, stratified)
      ↓
6. Scaling  (StandardScaler on numerical features)
      ↓
7. Model Comparison  (8 models via Pipeline)
      ↓
8. Cross Validation  (StratifiedKFold, k=5)
      ↓
9. Hyperparameter Tuning  (RandomizedSearchCV, 50 iterations)
      ↓
10. Feature Importance + SHAP Values
      ↓
11. Threshold Tuning  (optimized for Recall ≥ 95%)
      ↓
12. Final Evaluation + Save Model
```

---

## 🤖 Model Comparison

| Model | Accuracy | F1 | ROC-AUC |
|-------|----------|----|---------|
| **Gradient Boosting ✅** | **92.9%** | **93.5%** | **96.1%** |
| Random Forest | 91.3% | 92.2% | 95.0% |
| AdaBoost | 90.2% | 91.2% | 95.5% |
| Naive Bayes | 88.6% | 90.0% | 92.9% |
| SVM | 88.0% | 89.4% | 91.9% |
| Logistic Regression | 87.0% | 88.4% | 90.5% |
| KNN | 85.9% | 87.5% | 92.2% |
| Decision Tree | 82.1% | 84.5% | 81.3% |

---

## ⚙️ Best Hyperparameters

```python
GradientBoostingClassifier(
    n_estimators    = 200,
    max_depth       = 3,
    learning_rate   = 0.1,
    subsample       = 1.0,
    min_samples_split = 2,
    max_features    = 'sqrt',
    random_state    = 42
)
```

---

## 🌐 Streamlit Dashboard

The app has 4 pages:

| Page | Description |
|------|-------------|
| 📊 Dashboard | Model KPIs, demographic charts, correlation heatmap |
| 🫀 Predict | Enter patient data and get risk score instantly |
| 📋 History | Last 5 assessments with trend chart |
| ⚖️ Compare | Compare two patients side by side |

**Key features:**
- Real-time risk score with animated gauge
- Loading animation on prediction
- Downloadable patient report (.txt)
- Risk factor breakdown with color coding
- Fully responsive design

---

## 🔑 Key Findings

- **ST_Slope** is the strongest predictor — Flat/Down slope = 78–83% disease rate
- **Exercise Angina** — 85% disease rate when present vs 35% when absent
- **ASY Chest Pain** — 79% disease rate (most dangerous type)
- **Age** — risk jumps significantly after 50, peaks at 60s (74%)
- **Cholesterol** — negative correlation due to zero values in original data
- **Oldpeak** — strongest numerical correlation with disease (+0.40)

---

## 📦 Requirements

```
streamlit>=1.32.0
plotly>=5.19.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.4.0
joblib>=1.3.0
shap>=0.44.0
scipy>=1.11.0
```

---

## 👤 Author

**Moaaz** — Heart Failure Prediction Project

---

## 📄 License

MIT License — feel free to use and modify.
