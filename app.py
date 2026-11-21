
import streamlit as st
import joblib
import pandas as pd
import textwrap
from pathlib import Path
from datetime import datetime


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SpamGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "spam_svm_model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.pkl"


# =====================================================
# 2. HTML RENDERING HELPER
# =====================================================

def render_html(content):
    """Render HTML after removing unwanted indentation."""
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )


# =====================================================
# 3. LOAD SAVED MODELS
# =====================================================

@st.cache_resource
def load_models():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


try:
    model, tfidf = load_models()
    model_ready = True
    model_error = None

except Exception as error:
    model_ready = False
    model_error = str(error)


# =====================================================
# 4. SESSION STATE
# =====================================================

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"

if "history" not in st.session_state:
    st.session_state.history = []

if "sms_result" not in st.session_state:
    st.session_state.sms_result = None

if "email_result" not in st.session_state:
    st.session_state.email_result = None


# =====================================================
# 5. NAVIGATION FUNCTIONS
# =====================================================

def go_to_sms():
    st.session_state.nav_page = "SMS Detection"


def go_to_email():
    st.session_state.nav_page = "Email Detection"


def go_to_dashboard():
    st.session_state.nav_page = "Dashboard"


# =====================================================
# 6. FUTURISTIC EMERALD + CYAN THEME
# =====================================================

st.markdown(textwrap.dedent("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(13, 148, 136, 0.13),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 90%,
            rgba(6, 182, 212, 0.08),
            transparent 25%
        ),
        #07111B;

    color: #E2F3F1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0C1C27 0%,
        #07131D 100%
    );

    border-right: 1px solid #17443F;
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

[data-testid="stHeader"] {
    background: rgba(7, 17, 27, 0.8);
}

/* TEXT */

h1, h2, h3, h4 {
    color: #F0FDFA !important;
}

p, label {
    color: #B7D3D0;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;

    background: linear-gradient(
        90deg,
        #34D399,
        #22D3EE
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 4px;
}

.subtitle {
    color: #8DAEAC;
    font-size: 14px;
    margin-bottom: 25px;
}

.eyebrow {
    color: #34D399;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.brand-name {
    color: #ECFDF5;
    font-size: 22px;
    font-weight: 800;
}

.brand-subtitle {
    color: #7FA7A2;
    font-size: 11px;
    letter-spacing: 1px;
}

/* CARDS */

.tech-card {
    background: linear-gradient(
        145deg,
        #112630,
        #0D1B27
    );

    border: 1px solid #1B4546;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 12px;

    box-shadow: 0 8px 30px rgba(0,0,0,0.18);
}

.metric-card {
    background: linear-gradient(
        145deg,
        #122B35,
        #0D1C29
    );

    border: 1px solid #20504E;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    position: relative;
    overflow: hidden;
}

.metric-label {
    color: #8DB5B0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.metric-value {
    color: #ECFDF5;
    font-size: 28px;
    font-weight: 800;
    margin-top: 13px;
}

.metric-caption {
    color: #6F9B96;
    font-size: 11px;
    margin-top: 5px;
}

/* SERVICE CARDS */

.service-card {
    background: linear-gradient(
        145deg,
        #122A34,
        #0C1B27
    );

    border: 1px solid #20504E;
    border-radius: 16px;
    padding: 24px;
    min-height: 175px;
}

.service-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.service-title {
    color: #ECFDF5;
    font-size: 20px;
    font-weight: 750;
}

.service-description {
    color: #91B3AE;
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.7;
}

.section-heading {
    color: #ECFDF5;
    font-size: 20px;
    font-weight: 750;
    margin-top: 18px;
    margin-bottom: 15px;
}

.section-description {
    color: #83A6A1;
    font-size: 13px;
}

/* BUTTONS */

div.stButton > button,
div.stFormSubmitButton > button {

    background: linear-gradient(
        90deg,
        #059669,
        #0891B2
    );

    color: #FFFFFF;
    border: 1px solid #34D399;
    border-radius: 9px;
    min-height: 45px;
    font-weight: 700;
    width: 100%;

    transition: all 0.2s ease;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {

    background: linear-gradient(
        90deg,
        #047857,
        #0E7490
    );

    border: 1px solid #67E8F9;
    color: #FFFFFF;

    box-shadow: 0 0 15px rgba(34,211,238,0.22);
}

/* INPUTS */

.stTextInput input,
.stTextArea textarea {

    background-color: #0B1A25 !important;
    color: #ECFDF5 !important;
    border: 1px solid #28504F !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {

    border-color: #34D399 !important;
    box-shadow: 0 0 0 1px #34D399 !important;
}

/* FORMS */

[data-testid="stForm"] {

    background: linear-gradient(
        145deg,
        #10232E,
        #0B1924
    );

    border: 1px solid #20504E;
    border-radius: 15px;
    padding: 24px;
}

/* RESULTS */

.result-spam {

    background: linear-gradient(
        135deg,
        #3B1723,
        #27131E
    );

    border: 1px solid #E05270;
    border-radius: 15px;
    padding: 28px;
    text-align: center;

    box-shadow: 0 0 22px rgba(225,29,72,0.10);
}

.result-ham {

    background: linear-gradient(
        135deg,
        #10372C,
        #102820
    );

    border: 1px solid #34D399;
    border-radius: 15px;
    padding: 28px;
    text-align: center;

    box-shadow: 0 0 22px rgba(52,211,153,0.10);
}

.result-title {
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 10px;
}

.result-description {
    font-size: 14px;
    color: #D1E8E2;
}

/* STATUS */

.status-online {
    background: rgba(16,185,129,0.12);
    border: 1px solid #16866A;
    color: #6EE7B7;
    padding: 10px 12px;
    border-radius: 9px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
}

/* TABLES */

[data-testid="stDataFrame"] {
    border: 1px solid #20504E;
    border-radius: 10px;
}

/* SIDEBAR NAVIGATION */

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #C4DEDA;
    font-size: 13px;
}

/* DIVIDERS */

hr {
    border-color: #1D4143;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #628B85;
    font-size: 12px;
    padding: 20px;
    border-top: 1px solid #1D4143;
    margin-top: 30px;
}

/* HIDE DEFAULT BRANDING */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
"""), unsafe_allow_html=True)


# =====================================================
# 7. PREDICTION FUNCTION
# =====================================================

def analyze_message(message):

    message_vector = tfidf.transform([message])

    prediction = model.predict(message_vector)[0]

    return str(prediction).lower()


# =====================================================
# 8. SAVE ANALYSIS HISTORY
# =====================================================

def save_history(message_type, message, prediction):

    record = {
        "Type": message_type,
        "Message": message[:100],
        "Prediction": prediction.upper(),
        "Date & Time": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )
    }

    st.session_state.history.insert(0, record)

    st.session_state.history = (
        st.session_state.history[:20]
    )


# =====================================================
# 9. DISPLAY RESULT
# =====================================================

def display_result(prediction):

    if prediction == "spam":

        render_html("""
            <div class="result-spam">
                <div class="result-title">
                    🚨 SPAM DETECTED
                </div>
                <div class="result-description">
                    This message has been classified as spam.
                    Exercise caution before interacting with it.
                </div>
            </div>
        """)

    else:

        render_html("""
            <div class="result-ham">
                <div class="result-title">
                    🛡️ LEGITIMATE MESSAGE
                </div>
                <div class="result-description">
                    This message has been classified as ham
                    (not spam) by the trained SVM model.
                </div>
            </div>
        """)


# =====================================================
# 10. SIDEBAR
# =====================================================

with st.sidebar:

    render_html("""
        <div style="text-align:center; padding:12px 0 18px;">
            <div style="font-size:36px;">🛡️</div>
            <div class="brand-name">SPAMGUARD AI</div>
            <div class="brand-subtitle">
                INTELLIGENT MESSAGE SECURITY
            </div>
        </div>
    """)

    st.divider()

    render_html("""
        <div class="eyebrow">MAIN MENU</div>
    """)

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "SMS Detection",
            "Email Detection",
            "About Model"
        ],
        key="nav_page",
        label_visibility="collapsed"
    )

    st.divider()

    render_html("""
        <div class="eyebrow">SYSTEM STATUS</div>
    """)

    if model_ready:

        render_html("""
            <div class="status-online">
                ● &nbsp; AI MODEL ONLINE
            </div>
        """)

    else:
        st.error("AI MODEL OFFLINE")

    st.markdown("<br>", unsafe_allow_html=True)

    render_html("""
        <div style="color:#729993; font-size:11px; line-height:2;">
            <b>TECHNOLOGY</b><br>
            Python<br>
            Streamlit<br>
            Scikit-learn<br>
            TF-IDF + Linear SVM
        </div>
    """)

    st.divider()

    st.caption("SPAMGUARD AI • 2026")


# =====================================================
# 11. MAIN HEADER
# =====================================================

render_html("""
    <div class="eyebrow">
        ARTIFICIAL INTELLIGENCE / SECURITY
    </div>
    <div class="main-title">
        🛡️ SpamGuard AI
    </div>
    <div class="subtitle">
        Intelligent Spam Detection for SMS and Emails
    </div>
""")


# =====================================================
# 12. MODEL ERROR HANDLING
# =====================================================

if not model_ready:

    st.error(
        "Unable to load the trained model or TF-IDF vectorizer."
    )

    st.write("Please check your project folder:")

    st.code("""
Spam_Detection_Project/
│
├── app.py
│
└── models/
    ├── spam_svm_model.pkl
    └── tfidf_vectorizer.pkl
    """)

    st.code(model_error)

    st.stop()


# =====================================================
# 13. DASHBOARD
# =====================================================

if page == "Dashboard":

    render_html("""
        <div class="eyebrow">
            OVERVIEW / CONTROL CENTER
        </div>
        <div class="section-heading">
            Welcome to your workspace
        </div>
        <div class="section-description">
            Monitor your spam detection system and analyze suspicious messages.
        </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html("""
            <div class="metric-card">
                <div class="metric-label">MODEL ACCURACY</div>
                <div class="metric-value">97.36%</div>
                <div class="metric-caption">
                    Held-out test accuracy
                </div>
            </div>
        """)

    with col2:

        render_html("""
            <div class="metric-card">
                <div class="metric-label">CLASSIFICATION MODEL</div>
                <div class="metric-value">LINEAR SVM</div>
                <div class="metric-caption">
                    Trained machine learning model
                </div>
            </div>
        """)

    with col3:

        render_html("""
            <div class="metric-card">
                <div class="metric-label">DETECTION MODES</div>
                <div class="metric-value">02</div>
                <div class="metric-caption">
                    SMS + Email
                </div>
            </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    render_html("""
        <div class="section-heading">Detection Center</div>
        <div class="section-description">
            Choose a scanning mode to begin analyzing messages.
        </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        render_html("""
            <div class="service-card">
                <div class="service-icon">📱</div>
                <div class="service-title">SMS Scanner</div>
                <div class="service-description">
                    Analyze short text messages and detect
                    suspicious links, unwanted promotions,
                    and spam content.
                </div>
                <br>
                <div class="eyebrow">
                    TEXT MESSAGE ANALYSIS
                </div>
            </div>
        """)

        st.button(
            "OPEN SMS SCANNER →",
            key="open_sms",
            on_click=go_to_sms
        )

    with col2:

        render_html("""
            <div class="service-card">
                <div class="service-icon">📧</div>
                <div class="service-title">Email Scanner</div>
                <div class="service-description">
                    Analyze email subjects and message bodies
                    to identify potentially unwanted
                    or suspicious emails.
                </div>
                <br>
                <div class="eyebrow">
                    EMAIL CONTENT ANALYSIS
                </div>
            </div>
        """)

        st.button(
            "OPEN EMAIL SCANNER →",
            key="open_email",
            on_click=go_to_email
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    render_html("""
        <div class="section-heading">Recent Analysis</div>
    """)

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "CLEAR ANALYSIS HISTORY",
            key="clear_history"
        ):

            st.session_state.history = []
            st.rerun()

    else:

        st.info(
            "No analysis available yet. "
            "Start by scanning an SMS or Email."
        )


# =====================================================
# 14. SMS DETECTION
# =====================================================

elif page == "SMS Detection":

    render_html("""
        <div class="eyebrow">DETECTION CENTER / SMS</div>
        <div class="section-heading">
            📱 SMS Spam Scanner
        </div>
        <div class="section-description">
            Enter your SMS message below. The trained SVM model
            will classify it as Spam or Ham.
        </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("sms_form"):

        st.markdown("### Message Input")

        sms_message = st.text_area(
            "SMS MESSAGE",
            placeholder=(
                "Example: Congratulations! You have won "
                "a free prize. Click here now!"
            ),
            height=190
        )

        submitted = st.form_submit_button(
            "🔍 ANALYZE SMS MESSAGE"
        )

    if submitted:

        if sms_message.strip():

            try:

                prediction = analyze_message(sms_message)

                st.session_state.sms_result = prediction

                save_history(
                    "SMS",
                    sms_message,
                    prediction
                )

            except Exception as error:

                st.error(f"Prediction error: {error}")

        else:

            st.warning("Please enter an SMS message first.")

    if st.session_state.sms_result is not None:

        st.markdown("<br>", unsafe_allow_html=True)

        render_html("""
            <div class="eyebrow">
                SCAN COMPLETED / RESULTS
            </div>
        """)

        display_result(st.session_state.sms_result)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button(
        "← BACK TO DASHBOARD",
        key="sms_back",
        on_click=go_to_dashboard
    )


# =====================================================
# 15. EMAIL DETECTION
# =====================================================

elif page == "Email Detection":

    render_html("""
        <div class="eyebrow">DETECTION CENTER / EMAIL</div>
        <div class="section-heading">
            📧 Email Spam Scanner
        </div>
        <div class="section-description">
            Enter the email subject and body. Both fields will
            be combined and analyzed by the trained SVM model.
        </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("email_form"):

        st.markdown("### Email Information")

        email_subject = st.text_input(
            "EMAIL SUBJECT",
            placeholder="Enter email subject..."
        )

        email_body = st.text_area(
            "EMAIL BODY",
            placeholder="Paste the email content here...",
            height=240
        )

        submitted = st.form_submit_button(
            "🔍 ANALYZE EMAIL MESSAGE"
        )

    if submitted:

        if email_subject.strip() or email_body.strip():

            try:

                full_email = (
                    email_subject.strip()
                    + " "
                    + email_body.strip()
                ).strip()

                prediction = analyze_message(full_email)

                st.session_state.email_result = prediction

                save_history(
                    "Email",
                    full_email,
                    prediction
                )

            except Exception as error:

                st.error(f"Prediction error: {error}")

        else:

            st.warning(
                "Please enter an email subject or body."
            )

    if st.session_state.email_result is not None:

        st.markdown("<br>", unsafe_allow_html=True)

        render_html("""
            <div class="eyebrow">
                SCAN COMPLETED / RESULTS
            </div>
        """)

        display_result(st.session_state.email_result)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button(
        "← BACK TO DASHBOARD",
        key="email_back",
        on_click=go_to_dashboard
    )


# =====================================================
# 16. ABOUT MODEL
# =====================================================

elif page == "About Model":

    render_html("""
        <div class="eyebrow">
            SYSTEM INFORMATION / ML ENGINE
        </div>
        <div class="section-heading">
            About the AI Model
        </div>
        <div class="section-description">
            Learn how SpamGuard AI processes and classifies messages.
        </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    render_html("""
        <div class="tech-card">
            <h3>01 / TF-IDF VECTORIZATION</h3>
            <p>
                TF-IDF converts text messages into numerical features
                based on the importance of words and word combinations.
            </p>
            <hr>
            <h3>02 / SUPPORT VECTOR MACHINE</h3>
            <p>
                Linear Support Vector Machine learns patterns from
                training data and classifies messages into
                Spam and Ham categories.
            </p>
            <hr>
            <h3>03 / HYPERPARAMETER TUNING</h3>
            <p>
                GridSearchCV was used to find the best SVM parameter
                using cross-validation.
            </p>
        </div>
    """)

    render_html("""
        <div class="section-heading">
            Model Performance
        </div>
    """)

    metrics = pd.DataFrame({
        "Machine Learning Model": [
            "Multinomial Naive Bayes",
            "Logistic Regression",
            "Original SVM",
            "Tuned SVM"
        ],
        "Accuracy": [
            "93.64%",
            "96.78%",
            "97.36%",
            "97.36%"
        ]
    })

    st.dataframe(
        metrics,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Best SVM Parameter", "C = 1")
        st.metric("Cross-Validation Score", "97.21%")

    with col2:

        st.metric("Test Accuracy", "97.36%")
        st.metric("Feature Extraction", "TF-IDF")

    render_html("""
        <div class="section-heading">
            Dataset Information
        </div>
    """)

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Original Records", "204,813")
        st.metric("Cleaned Records", "204,131")

    with col2:

        st.metric("Ham Messages", "110,170")
        st.metric("Spam Messages", "93,961")

    st.info(
        "The same trained SVM model is used for both SMS and "
        "email text. Email subject and body are combined before "
        "prediction. These are two input modes, not separately "
        "trained classifiers."
    )


# =====================================================
# 17. FOOTER
# =====================================================

render_html("""
    <div class="footer">
        <div style="
            color:#34D399;
            font-size:14px;
            font-weight:800;
            letter-spacing:1px;
        ">
            🛡️ SPAMGUARD AI
        </div>
        <br>
        Intelligent Spam Detection System
        <br>
        Built with Python • Streamlit • Scikit-learn • TF-IDF
    </div>
""")
