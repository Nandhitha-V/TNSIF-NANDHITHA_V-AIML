from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(title="Loan Approval API", version="1.0")

# Load binary artifacts
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

class LoanApplicant(BaseModel):
    income: float = Field(..., example=50000.0)
    credit_score: float = Field(..., example=700.0)
    loan_amount: float = Field(..., example=15000.0)
    employment_years: float = Field(..., example=5.0)

@app.get("/")
def home():
    return {"status": "Online", "message": "Loan Approval API is running."}

@app.post("/predict")
def predict_loan_status(applicant: LoanApplicant):
    try:
        # Prepare input features matching training data shape
        input_data = np.array([[
            applicant.income,
            applicant.credit_score,
            applicant.loan_amount,
            applicant.employment_years
        ]])

        scaled_features = scaler.transform(input_data)
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1]

        return {
            "loan_status": "Approved" if int(prediction) == 1 else "Rejected",
            "approval_probability": float(round(probability, 4)),
            "status_code": 1 if int(prediction) == 1 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))