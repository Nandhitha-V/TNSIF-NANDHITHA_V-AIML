import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train():
    print(" Loading clean data...")
    df = pd.read_csv("loans.csv")

    X = df[['income', 'credit_score', 'loan_amount', 'employment_years']]
    y = df['loan_status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale numeric features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    predictions = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, predictions)
    print(f" Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, predictions))

    # Export model and scaler artifacts
    joblib.dump(model, "model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print(" Saved 'model.pkl' and 'scaler.pkl' successfully!")

if __name__ == "__main__":
    train()