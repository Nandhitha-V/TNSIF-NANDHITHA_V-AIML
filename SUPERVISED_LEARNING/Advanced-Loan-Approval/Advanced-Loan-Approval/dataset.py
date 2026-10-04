import pandas as pd

def process_data(input_path="loans - loans.csv", output_path="loans.csv"):
    print(" Loading dataset...")
    df = pd.read_csv(input_path)

    # Validate required columns
    expected_cols = ['income', 'credit_score', 'loan_amount', 'employment_years', 'loan_status']
    for col in expected_cols:
        if col not in df.columns:
            raise KeyError(f"Missing expected column: {col}")

    # Save standardized copy
    df.to_csv(output_path, index=False)
    print(f" Dataset validated and saved to '{output_path}'.")
    print(f" Dataset Shape: {df.shape}")
    print(df.head())

if __name__ == "__main__":
    process_data()