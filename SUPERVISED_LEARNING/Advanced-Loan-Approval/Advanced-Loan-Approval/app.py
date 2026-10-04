from pathlib import Path
import joblib
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
FEATURES = ["income", "credit_score", "loan_amount", "employment_years"]
TARGET = "loan_status"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PREMIUM 3D UI STYLING
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(70, 105, 255, 0.18),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 16%,
            rgba(111, 78, 255, 0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(25, 90, 180, 0.12),
            transparent 35%
        ),
        #06111f;

    color: #f4f7ff;
    min-height: 100vh;
}

/* STREAMLIT CLEANUP */
[data-testid="stToolbar"] {
    visibility: hidden;
}

[data-testid="stDeployButton"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.main .block-container {
    max-width: 1380px;
    padding: 42px 48px 70px;
}

/* DECORATIVE 3D BACKGROUND */
.orb {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

.orb-one {
    width: 330px;
    height: 330px;
    top: 100px;
    left: -210px;
    background: rgba(57, 101, 255, 0.13);
    box-shadow: 0 0 130px 70px rgba(57, 101, 255, 0.10);
}

.orb-two {
    width: 360px;
    height: 360px;
    right: -230px;
    top: 380px;
    background: rgba(117, 80, 255, 0.10);
    box-shadow: 0 0 140px 70px rgba(117, 80, 255, 0.08);
}

/* HERO */
.hero {
    position: relative;
    z-index: 2;
    padding: 8px 2px 30px;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1fr 430px;
    gap: 45px;
    align-items: center;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    padding: 8px 14px;
    border-radius: 100px;
    background: rgba(82, 119, 255, 0.10);
    border: 1px solid rgba(121, 148, 255, 0.24);
    color: #9eb5ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.15);
}

.eyebrow-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #78a2ff;
    box-shadow: 0 0 13px #78a2ff;
}

.hero-title {
    margin: 18px 0 12px;
    font-size: clamp(40px, 5vw, 66px);
    line-height: 1.02;
    letter-spacing: -3px;
    font-weight: 800;
    color: #ffffff;
}

.hero-title span {
    background: linear-gradient(100deg, #ffffff 5%, #aac2ff 45%, #7f8dff 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 680px;
    color: #8f9eb7;
    font-size: 15px;
    line-height: 1.75;
}

/* 3D LOAN CARD */
.loan-object {
    perspective: 1200px;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 255px;
}

.loan-card {
    position: relative;
    width: 365px;
    height: 215px;
    padding: 25px;
    overflow: hidden;
    border-radius: 26px;
    background: linear-gradient(145deg, #314f9c 0%, #182b5b 48%, #0d1936 100%);
    border: 1px solid rgba(164, 187, 255, 0.28);
    box-shadow: 0 48px 80px rgba(0,0,0,0.45), 0 18px 35px rgba(47, 82, 190, 0.25), inset 0 1px 0 rgba(255,255,255,0.20), inset 0 -2px 0 rgba(0,0,0,0.25);
    transform: rotateX(9deg) rotateY(-13deg) rotateZ(2deg);
    animation: floating-card 5s ease-in-out infinite;
    transition: transform 0.45s ease;
}

.loan-card:hover {
    transform: rotateX(2deg) rotateY(-3deg) rotateZ(0deg) translateY(-8px);
}

.loan-card::before {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    right: -105px;
    top: -120px;
    border-radius: 50%;
    background: rgba(137, 164, 255, 0.25);
    filter: blur(3px);
}

.loan-card::after {
    content: "";
    position: absolute;
    width: 310px;
    height: 65px;
    left: -100px;
    bottom: -28px;
    background: rgba(99, 124, 255, 0.18);
    transform: rotate(-24deg);
    filter: blur(13px);
}

@keyframes floating-card {
    0%, 100% {
        transform: rotateX(9deg) rotateY(-13deg) rotateZ(2deg) translateY(0);
    }
    50% {
        transform: rotateX(7deg) rotateY(-10deg) rotateZ(1deg) translateY(-9px);
    }
}

.card-content {
    position: relative;
    z-index: 2;
}

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chip {
    width: 49px;
    height: 37px;
    border-radius: 9px;
    background: linear-gradient(135deg, #e8eefb, #8c9ab8);
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.65), 0 5px 12px rgba(0,0,0,0.22);
}

.card-logo {
    width: 43px;
    height: 43px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #dce6ff;
    font-size: 20px;
    font-weight: 800;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.20);
    box-shadow: inset 0 1px 8px rgba(255,255,255,0.08);
}

.card-number {
    margin-top: 28px;
    color: #dbe6ff;
    font-size: 13px;
    letter-spacing: 3px;
    font-weight: 600;
}

.card-bottom {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}

.card-label {
    color: #8294bd;
    font-size: 8px;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.card-value {
    margin-top: 4px;
    color: #ffffff;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
}

/* INFO CARDS */
.info-strip {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin: 4px 0 30px;
}

.info-card {
    padding: 17px 20px;
    border-radius: 17px;
    background: rgba(14, 28, 51, 0.70);
    border: 1px solid rgba(135, 160, 213, 0.12);
    box-shadow: 0 16px 30px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.045);
    backdrop-filter: blur(16px);
}

.info-title {
    color: #7083a7;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

.info-value {
    margin-top: 6px;
    color: #dce6fa;
    font-size: 13px;
    font-weight: 600;
}

/* APPLICATION PANEL */
.application-panel {
    position: relative;
    z-index: 2;
    padding: 34px;
    border-radius: 30px;
    background: linear-gradient(145deg, rgba(17, 32, 57, 0.95), rgba(8, 19, 35, 0.95));
    border: 1px solid rgba(148, 174, 229, 0.13);
    box-shadow: 0 45px 90px rgba(0,0,0,0.34), 0 15px 30px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 7px;
}

.section-icon {
    width: 43px;
    height: 43px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: linear-gradient(145deg, rgba(84, 120, 255, 0.25), rgba(53, 72, 143, 0.12));
    border: 1px solid rgba(119, 147, 255, 0.23);
    box-shadow: 0 12px 24px rgba(45, 73, 165, 0.16), inset 0 1px 0 rgba(255,255,255,0.10);
    color: #9db4ff;
    font-size: 21px;
}

.section-title {
    color: #f2f5ff;
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.4px;
}

.section-subtitle {
    margin-left: 56px;
    margin-bottom: 27px;
    color: #71819d;
    font-size: 12px;
}

/* INPUTS */
div[data-testid="stNumberInput"] {
    margin-bottom: 12px;
}

div[data-testid="stNumberInput"] label {
    color: #aebbd1 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 7px;
}

div[data-testid="stNumberInput"] input {
    min-height: 50px !important;
    color: #edf3ff !important;
    background: linear-gradient(145deg, rgba(24, 41, 70, 0.95), rgba(11, 25, 46, 0.95)) !important;
    border: 1px solid rgba(130, 158, 216, 0.16) !important;
    border-radius: 14px !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.20), 0 7px 16px rgba(0,0,0,0.10) !important;
    transition: 0.25s ease;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(104, 139, 255, 0.72) !important;
    box-shadow: 0 0 0 3px rgba(86, 119, 255, 0.10), 0 10px 22px rgba(0,0,0,0.15), inset 0 2px 6px rgba(0,0,0,0.20) !important;
}

div[data-testid="stNumberInput"] button {
    color: #9eb3e2 !important;
    background: transparent !important;
    border: none !important;
}

/* BUTTON */
div[data-testid="stFormSubmitButton"] > button {
    width: 100%;
    min-height: 56px;
    border-radius: 15px !important;
    border: 1px solid rgba(151, 176, 255, 0.28) !important;
    color: #ffffff !important;
    background: linear-gradient(145deg, #597fff 0%, #4567e8 45%, #354fc0 100%) !important;
    font-size: 14px !important;
    font-weight: 750 !important;
    letter-spacing: 0.2px;
    box-shadow: 0 14px 27px rgba(48, 76, 190, 0.30), 0 4px 8px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.22), inset 0 -2px 0 rgba(20,38,110,0.30) !important;
    transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px);
    filter: brightness(1.08);
    box-shadow: 0 20px 36px rgba(48,76,190,0.38), 0 6px 12px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.25) !important;
}

/* RESULT CARD */
.result-card {
    position: relative;
    overflow: hidden;
    margin-top: 30px;
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(20, 38, 69, 0.95), rgba(10, 23, 43, 0.95));
    border: 1px solid rgba(135, 162, 223, 0.16);
    box-shadow: 0 25px 50px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.06);
}

.result-card.approved {
    border-color: rgba(68,214,157,0.26);
    background: radial-gradient(circle at 90% 10%, rgba(56,202,145,0.11), transparent 35%), linear-gradient(145deg, rgba(18,52,52,0.95), rgba(9,29,40,0.95));
}

.result-card.rejected {
    border-color: rgba(255,102,119,0.25);
    background: radial-gradient(circle at 90% 10%, rgba(255,78,101,0.10), transparent 35%), linear-gradient(145deg, rgba(55,30,44,0.95), rgba(31,21,37,0.95));
}

.result-top {
    display: flex;
    align-items: center;
    gap: 16px;
}

.result-icon {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: 800;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 12px 24px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.09);
}

.approved .result-icon {
    color: #68e7b1;
}

.rejected .result-icon {
    color: #ff8390;
}

.result-label {
    color: #74849f;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 700;
}

.result-status {
    margin-top: 3px;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

.approved .result-status {
    color: #71e6b5;
}

.rejected .result-status {
    color: #ff8794;
}

/* PROBABILITY */
.probability-container {
    margin-top: 25px;
    padding-top: 22px;
    border-top: 1px solid rgba(150,170,210,0.10);
}

.probability-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 11px;
}

.probability-title {
    color: #8494af;
    font-size: 10px;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.probability-value {
    color: #eef3ff;
    font-size: 18px;
    font-weight: 800;
}

.probability-bar {
    height: 9px;
    border-radius: 100px;
    background: rgba(255,255,255,0.07);
    overflow: hidden;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.20);
}

.probability-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #5278ff, #79a0ff);
    box-shadow: 0 0 14px rgba(91,129,255,0.42);
}

/* FOOTER */
.footer {
    position: relative;
    z-index: 2;
    text-align: center;
    margin-top: 32px;
    color: #4f607c;
    font-size: 10px;
    letter-spacing: 0.5px;
}

/* RESPONSIVE */
@media (max-width: 900px) {
    .main .block-container {
        padding: 28px 20px 50px;
    }
    .hero-grid {
        grid-template-columns: 1fr;
    }
    .info-strip {
        grid-template-columns: 1fr;
    }
    .application-panel {
        padding: 24px 20px;
    }
}

@media (max-width: 520px) {
    .hero-title {
        font-size: 39px;
        letter-spacing: -1.8px;
    }
    .loan-card {
        width: 300px;
        height: 185px;
    }
    .hero-description {
        font-size: 14px;
    }
}
</style>

<div class="orb orb-one"></div>
<div class="orb orb-two"></div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD EXISTING MODEL
# ============================================================

@st.cache_resource
def load_model_files():
    model_path = ROOT / "model.pkl"
    scaler_path = ROOT / "scaler.pkl"
    data_path = ROOT / "loans.csv"

    missing_files = [
        path.name
        for path in (model_path, scaler_path, data_path)
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing file(s): {', '.join(missing_files)}"
        )

    data = pd.read_csv(data_path)

    required_columns = FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing column(s): {', '.join(missing_columns)}"
        )

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler, data


try:
    model, scaler, dataset = load_model_files()
except Exception as error:
    st.error(f"Could not load the loan model: {error}")
    st.stop()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<section class="hero">
    <div class="hero-grid">
        <div>
            <div class="eyebrow">
                <span class="eyebrow-dot"></span>
                Intelligent Credit Decision System
            </div>
            <div class="hero-title">
                Loan <span>Approval</span><br>
                Intelligence
            </div>
            <div class="hero-description">
                Evaluate applicant financial information through
                a machine-learning powered approval system designed
                to deliver fast, consistent and data-driven
                loan decisions.
            </div>
        </div>
        <div class="loan-object">
            <div class="loan-card">
                <div class="card-content">
                    <div class="card-top">
                        <div class="chip"></div>
                        <div class="card-logo">₹</div>
                    </div>
                    <div class="card-number">CREDIT • FINANCE • TRUST</div>
                    <div class="card-bottom">
                        <div>
                            <div class="card-label">Applicant</div>
                            <div class="card-value">FINANCIAL PROFILE</div>
                        </div>
                        <div>
                            <div class="card-label">Decision</div>
                            <div class="card-value">AI ANALYSIS</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
""",
    unsafe_allow_html=True,
)


# ============================================================
# INFORMATION STRIP
# ============================================================

st.markdown(
    """
<div class="info-strip">
    <div class="info-card">
        <div class="info-title">Decision Engine</div>
        <div class="info-value">Random Forest Classifier</div>
    </div>
    <div class="info-card">
        <div class="info-title">Analysis Type</div>
        <div class="info-value">Predictive Credit Assessment</div>
    </div>
    <div class="info-card">
        <div class="info-title">Output</div>
        <div class="info-value">Approval Status + Probability</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# APPLICATION UI
# ============================================================

st.markdown(
    """
<div class="application-panel">
    <div class="section-heading">
        <div class="section-icon">₹</div>
        <div class="section-title">Applicant Financial Profile</div>
    </div>
    <div class="section-subtitle">
        Enter the applicant's financial information to generate an intelligent loan decision.
    </div>
""",
    unsafe_allow_html=True,
)


with st.form("loan_application"):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        income = st.number_input(
            "Annual income",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
        )

        credit_score = st.number_input(
            "Credit score",
            min_value=0.0,
            max_value=1000.0,
            value=700.0,
            step=1.0,
        )

    with col2:
        loan_amount = st.number_input(
            "Loan amount",
            min_value=0.0,
            value=15000.0,
            step=500.0,
        )

        employment_years = st.number_input(
            "Employment years",
            min_value=0.0,
            value=5.0,
            step=1.0,
        )

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    submitted = st.form_submit_button(
        "Analyze Loan Application  →",
        use_container_width=True,
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# EXISTING PREDICTION LOGIC
# ============================================================

if submitted:
    applicant = pd.DataFrame(
        [[
            income,
            credit_score,
            loan_amount,
            employment_years
        ]],
        columns=FEATURES,
    )

    scaled_applicant = scaler.transform(applicant)
    prediction = int(model.predict(scaled_applicant)[0])
    approval_probability = float(model.predict_proba(scaled_applicant)[0][1])
    percentage = approval_probability * 100

    if prediction == 1:
        st.markdown(
            f"""
<div class="result-card approved">
    <div class="result-top">
        <div class="result-icon">✓</div>
        <div>
            <div class="result-label">Machine Learning Decision</div>
            <div class="result-status">Loan Approved</div>
        </div>
    </div>
    <div class="probability-container">
        <div class="probability-header">
            <div class="probability-title">Approval probability</div>
            <div class="probability-value">{percentage:.1f}%</div>
        </div>
        <div class="probability-bar">
            <div class="probability-fill" style="width:{percentage:.1f}%"></div>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
<div class="result-card rejected">
    <div class="result-top">
        <div class="result-icon">×</div>
        <div>
            <div class="result-label">Machine Learning Decision</div>
            <div class="result-status">Loan Rejected</div>
        </div>
    </div>
    <div class="probability-container">
        <div class="probability-header">
            <div class="probability-title">Approval probability</div>
            <div class="probability-value">{percentage:.1f}%</div>
        </div>
        <div class="probability-bar">
            <div class="probability-fill" style="width:{percentage:.1f}%"></div>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    LOAN APPROVAL INTELLIGENCE • DATA-DRIVEN CREDIT ASSESSMENT
</div>
""",
    unsafe_allow_html=True,
)