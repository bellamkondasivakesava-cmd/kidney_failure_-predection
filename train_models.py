import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

def generate_synthetic_data(num_samples=1200, seed=42):
    np.random.seed(seed)
    
    # Continuous features
    age = np.random.normal(55, 12, num_samples).clip(18, 90)
    gender = np.random.binomial(1, 0.55, num_samples) # 1=Male, 0=Female
    height = np.random.normal(168, 10, num_samples).clip(140, 200)
    weight = np.random.normal(75, 15, num_samples).clip(45, 130)
    blood_pressure = np.random.normal(125, 15, num_samples).clip(80, 180) # mmHg
    blood_glucose = np.random.normal(110, 30, num_samples).clip(60, 250) # mg/dL
    serum_creatinine = np.random.normal(1.2, 0.8, num_samples).clip(0.4, 7.0) # mg/dL
    blood_urea = np.random.normal(45, 20, num_samples).clip(10, 150) # mg/dL
    albumin = np.random.choice([0, 1, 2, 3, 4, 5], num_samples, p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02])
    hemoglobin = np.random.normal(13.5, 2.0, num_samples).clip(7.0, 18.0) # g/dL
    sodium = np.random.normal(138, 5, num_samples).clip(115, 150) # mEq/L
    potassium = np.random.normal(4.2, 0.6, num_samples).clip(2.5, 6.5) # mEq/L
    
    # Categorical features (0 or 1)
    hypertension = np.random.binomial(1, 0.35, num_samples)
    diabetes = np.random.binomial(1, 0.30, num_samples)
    smoking = np.random.binomial(1, 0.25, num_samples)
    alcohol = np.random.binomial(1, 0.20, num_samples)
    family_history = np.random.binomial(1, 0.15, num_samples)
    
    # Calculate log-odds (risk score z)
    # Standard values: creatinine normal ~1.0, BP normal ~120, glucose ~90, albumin ~0, hemoglobin ~14, sodium ~140, potassium ~4
    z = (
        -4.0
        + 0.03 * (age - 50)
        + 0.04 * (blood_pressure - 120)
        + 0.01 * (blood_glucose - 100)
        + 2.2 * (serum_creatinine - 1.0)
        + 0.03 * (blood_urea - 40)
        + 0.9 * albumin
        - 0.5 * (hemoglobin - 13.5)
        - 0.1 * (sodium - 138)
        + 0.4 * (potassium - 4.2)
        + 1.3 * hypertension
        + 1.6 * diabetes
        + 0.4 * smoking
        + 0.2 * alcohol
        + 0.8 * family_history
    )
    
    # Sigmoid function for probability
    probs = 1 / (1 + np.exp(-z))
    # Binary labels (1 = Kidney disease/High Risk, 0 = Healthy/Low Risk)
    targets = (probs >= 0.45).astype(int)
    
    df = pd.DataFrame({
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'blood_pressure': blood_pressure,
        'blood_glucose': blood_glucose,
        'serum_creatinine': serum_creatinine,
        'blood_urea': blood_urea,
        'albumin': albumin,
        'hemoglobin': hemoglobin,
        'sodium': sodium,
        'potassium': potassium,
        'hypertension': hypertension,
        'diabetes': diabetes,
        'smoking': smoking,
        'alcohol': alcohol,
        'family_history': family_history,
        'target': targets
    })
    
    return df

def train_and_save_models():
    os.makedirs('models', exist_ok=True)
    
    print("Generating synthetic kidney clinical dataset...")
    df = generate_synthetic_data(1200)
    
    X = df.drop(columns=['target'])
    y = df['target']
    
    # Standard Scaler
    print("Fitting and saving scaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # 1. Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_scaled, y)
    joblib.dump(lr, 'models/Logistic_Regression.pkl')
    
    # 2. Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_scaled, y)
    joblib.dump(rf, 'models/Random_Forest.pkl')
    
    # 3. XGBoost
    print("Training XGBoost...")
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb.fit(X_scaled, y)
    joblib.dump(xgb, 'models/XGBoost.pkl')
    
    # 4. SVM (with probability estimation)
    print("Training SVM...")
    svm = SVC(probability=True, kernel='rbf', random_state=42)
    svm.fit(X_scaled, y)
    joblib.dump(svm, 'models/SVM.pkl')
    
    # 5. KNN
    print("Training KNN...")
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_scaled, y)
    joblib.dump(knn, 'models/KNN.pkl')
    
    # 6. MLP (Neural Network)
    print("Training MLP Neural Network...")
    mlp = MLPClassifier(max_iter=1000, random_state=42)
    mlp.fit(X_scaled, y)
    joblib.dump(mlp, 'models/MLP.pkl')
    
    print("All models and scaler saved in 'models/' directory successfully!")

if __name__ == '__main__':
    train_and_save_models()
