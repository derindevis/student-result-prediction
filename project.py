import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Helper function to generate prediction report PDF
def generate_pdf_report(hours, attendance, prev_marks, assignments, sleep, prediction, confidence):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=15,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#334155')
    )

    verdict_style_pass = ParagraphStyle(
        'VerdictPass',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#065f46')
    )

    verdict_style_fail = ParagraphStyle(
        'VerdictFail',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#991b1b')
    )

    story.append(Paragraph("Student Result Prediction Report", title_style))
    story.append(Paragraph("Developed by Derin Devis | 23F41A3314", subtitle_style))
    
    story.append(Paragraph("Prediction Verdict", heading_style))
    verdict_text = "PASS" if prediction == 1 else "FAIL"
    verdict_desc = (
        f"Based on the input parameters, the student is predicted to <b>{verdict_text}</b> the final examination "
        f"with a confidence score of <b>{confidence:.2f}%</b>."
    )
    
    verdict_para = Paragraph(verdict_desc, verdict_style_pass if prediction == 1 else verdict_style_fail)
    verdict_table = Table([[verdict_para]], colWidths=[doc.width])
    bg_color = colors.HexColor('#d1fae5') if prediction == 1 else colors.HexColor('#fee2e2')
    border_color = colors.HexColor('#10b981') if prediction == 1 else colors.HexColor('#ef4444')
    
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Input Parameters Profile", heading_style))
    
    data = [
        [Paragraph("<b>Student Parameter</b>", body_style), Paragraph("<b>Value Entered</b>", body_style)],
        [Paragraph("Daily Study Hours", body_style), Paragraph(f"{hours} hours", body_style)],
        [Paragraph("Class Attendance Percentage", body_style), Paragraph(f"{attendance}%", body_style)],
        [Paragraph("Previous Exam Marks", body_style), Paragraph(f"{prev_marks} / 100", body_style)],
        [Paragraph("Assignments Completed", body_style), Paragraph(f"{assignments} / 10", body_style)],
        [Paragraph("Daily Sleep Hours", body_style), Paragraph(f"{sleep} hours", body_style)],
    ]
    
    param_table = Table(data, colWidths=[doc.width * 0.6, doc.width * 0.4])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("Model & Training Details", heading_style))
    model_text = (
        "The prediction was generated using a <b>Logistic Regression</b> binary classification model, trained on "
        "500 synthetic student records. The features were normalized using a <b>StandardScaler</b>. "
        "During evaluation on an 80/20 train/test split, the model achieved the following performance:<br/>"
        "• <b>Accuracy:</b> 88.00%<br/>"
        "• <b>Precision:</b> 90.36%<br/>"
        "• <b>Recall:</b> 94.94%<br/>"
        "• <b>F1 Score:</b> 92.59%"
    )
    story.append(Paragraph(model_text, body_style))
    story.append(Spacer(1, 40))
    
    sig_text = (
        "<i>This is a computer-generated report created by the Student Result Prediction System "
        "developed by Derin Devis (23F41A3314)</i>"
    )
    story.append(Paragraph(sig_text, ParagraphStyle('Sig', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#94a3b8'), alignment=1)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# Set page configuration
st.set_page_config(
    page_title="Student Result Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and premium styling
st.markdown("""
    <style>
    /* Custom background & font settings */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Animation Keyframes */
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(-15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.97); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Elegant Title and Subtitle styling with animations */
    .main-title {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
        text-align: center;
        animation: fadeInSlide 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .sub-title {
        color: #64748b;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
        animation: fadeInSlide 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Bento Grid container override styling */
    div[data-testid="stVerticalBlockBorder"] {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01) !important;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease !important;
        padding: 1.5rem !important;
    }
    div[data-testid="stVerticalBlockBorder"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 24px -10px rgba(99, 102, 241, 0.15) !important;
        border-color: #c7d2fe !important; /* Soft indigo highlight on hover */
    }

    /* Metric card text formatting */
    .bento-metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .bento-metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
    }
    
    /* Input label styling */
    .bento-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Prediction banner styles with pop-in animations */
    .prediction-card-pass {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 8px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        color: #065f46;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
        animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .prediction-card-fail {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 8px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        color: #991b1b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
        animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Custom buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px -8px rgba(99, 102, 241, 0.4) !important;
    }
    .stButton>button:active {
        transform: translateY(0px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache data generation for performance
@st.cache_data
def generate_student_data():
    np.random.seed(42)
    n_samples = 500
    
    hours_study = np.random.uniform(1, 12, n_samples)
    attendance = np.random.uniform(40, 100, n_samples)
    prev_marks = np.random.uniform(30, 100, n_samples)
    assignments_done = np.random.randint(0, 11, n_samples)
    sleep_hours = np.random.uniform(4, 10, n_samples)
    
    # Generate realistic Final Marks based on inputs + normal noise
    noise = np.random.normal(0, 5.5, n_samples)
    final_marks = (
        0.35 * prev_marks + 
        2.0 * hours_study + 
        0.22 * attendance + 
        1.2 * assignments_done + 
        0.4 * sleep_hours + 
        noise
    )
    final_marks = np.clip(final_marks, 0, 100)
    
    # 1 = Pass (marks >= 50), 0 = Fail (marks < 50)
    result = (final_marks >= 50).astype(int)
    
    df = pd.DataFrame({
        'Hours_Study': hours_study,
        'Attendance': attendance,
        'Previous_Marks': prev_marks,
        'Assignments_Done': assignments_done,
        'Sleep_Hours': sleep_hours,
        'Final_Marks': final_marks,
        'Result': result
    })
    return df

# Load data
df = generate_student_data()

# Prepare Data and Train Model
X = df[['Hours_Study', 'Attendance', 'Previous_Marks', 'Assignments_Done', 'Sleep_Hours']]
y = df['Result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, solver='lbfgs', random_state=42)
model.fit(X_train_sc, y_train)

# Calculate performance metrics
y_pred = model.predict(X_test_sc)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# Sidebar - Brand & Settings
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #4f46e5; margin-bottom: 5px;">🎓 Success Predictor</h2>
        <p style="color: #64748b; font-size: 0.9rem;">Student Success Prediction</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader("Dataset Info")
st.sidebar.write(f"📂 **Total Dataset Size:** {len(df)} records")
st.sidebar.write(f"📈 **Train Set:** {len(X_train)} records")
st.sidebar.write(f"📉 **Test Set:** {len(X_test)} records")
st.sidebar.write("---")
st.sidebar.markdown(
    """
    <div style="font-size: 0.8rem; color: #94a3b8; text-align: center;">
        Developed by <b>Derin Devis</b><br>
        Reg No: 23F41A3314<br>
        June 2026
    </div>
    """,
    unsafe_allow_html=True
)

# Header Title
st.markdown('<h1 class="main-title">Student Result Prediction System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">A Machine Learning Web Application using Python, Streamlit & Logistic Regression</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔮 Predict Result", "📊 Data Analysis", "⚙️ Model Performance"])

# ==================== TAB 1: PREDICT RESULT ====================
with tab1:
    st.markdown("### 🎛️ Interactive Student Profile")
    st.markdown("Adjust the parameter cards below to create the student's profile, then click **Predict Outcome**.")
    
    # Bento Grid for inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">📚 Study Hours</div>', unsafe_allow_html=True)
            hours = st.slider("Daily Study Hours", min_value=1.0, max_value=12.0, value=6.0, step=0.5, label_visibility="collapsed")
            st.markdown(f"**Target:** {hours} hrs/day")
            
    with col2:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">🏫 Attendance</div>', unsafe_allow_html=True)
            attendance = st.slider("Class Attendance Percentage (%)", min_value=40.0, max_value=100.0, value=75.0, step=1.0, label_visibility="collapsed")
            st.markdown(f"**Target:** {attendance}%")
            
    with col3:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">📝 Previous Marks</div>', unsafe_allow_html=True)
            prev_marks = st.slider("Previous Exam Marks (out of 100)", min_value=30.0, max_value=100.0, value=65.0, step=1.0, label_visibility="collapsed")
            st.markdown(f"**Target:** {prev_marks} / 100")
            
    col4, col5, col6 = st.columns(3)
    with col4:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">✅ Assignments</div>', unsafe_allow_html=True)
            assignments = st.slider("Number of Assignments Completed", min_value=0, max_value=10, value=5, step=1, label_visibility="collapsed")
            st.markdown(f"**Target:** {assignments} / 10")
            
    with col5:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">😴 Sleep Hours</div>', unsafe_allow_html=True)
            sleep = st.slider("Average Daily Sleep Hours", min_value=4.0, max_value=10.0, value=7.0, step=0.5, label_visibility="collapsed")
            st.markdown(f"**Target:** {sleep} hours")
            
    with col6:
        with st.container(border=True):
            st.markdown('<div class="bento-card-title">🔮 Engine</div>', unsafe_allow_html=True)
            st.markdown("Compute outcome using Logistic Regression.")
            predict_btn = st.button("Predict Outcome")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    if predict_btn:
        with st.container(border=True):
            col_res, col_sum = st.columns([1.2, 1], gap="large")
            with col_res:
                st.markdown("#### **Prediction Verdict**")
                
                # Scale input and run prediction
                input_df = pd.DataFrame(
                    [[hours, attendance, prev_marks, assignments, sleep]], 
                    columns=['Hours_Study', 'Attendance', 'Previous_Marks', 'Assignments_Done', 'Sleep_Hours']
                )
                input_data = scaler.transform(input_df)
                prediction = model.predict(input_data)[0]
                prob = model.predict_proba(input_data)[0]
                
                pass_prob = prob[1] * 100
                fail_prob = prob[0] * 100
                
                if prediction == 1:
                    st.markdown(
                        f"""
                        <div class="prediction-card-pass">
                            <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                                🎉 PASS
                            </h2>
                            <p style="margin-top: 10px; margin-bottom: 0; font-size: 1.15rem;">
                                The student is predicted to <b>PASS</b> the final examination.<br>
                                Confidence: <b>{pass_prob:.2f}%</b>
                            </p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="prediction-card-fail">
                            <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                                ⚠️ FAIL
                            </h2>
                            <p style="margin-top: 10px; margin-bottom: 0; font-size: 1.15rem;">
                                The student is predicted to <b>FAIL</b> (At Risk).<br>
                                Confidence: <b>{fail_prob:.2f}%</b>
                            </p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Generate and allow PDF Download
                pdf_data = generate_pdf_report(
                    hours, 
                    attendance, 
                    prev_marks, 
                    assignments, 
                    sleep, 
                    prediction, 
                    pass_prob if prediction == 1 else fail_prob
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download PDF Prediction Report",
                    data=pdf_data,
                    file_name=f"student_prediction_{'pass' if prediction == 1 else 'fail'}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            with col_sum:
                st.markdown("#### **Input Summary**")
                input_summary = pd.DataFrame({
                    "Parameter": [
                        "Daily Study Hours", 
                        "Class Attendance", 
                        "Previous Exam Marks", 
                        "Assignments Completed", 
                        "Daily Sleep Hours"
                    ],
                    "Value": [
                        f"{hours} hours", 
                        f"{attendance}%", 
                        f"{prev_marks} / 100", 
                        f"{assignments} completed", 
                        f"{sleep} hours"
                    ]
                })
                st.table(input_summary)
    else:
        st.info("👈 Adjust parameters above and click 'Predict Outcome' to see results.")

# ==================== TAB 2: DATA ANALYSIS ====================
with tab2:
    st.markdown("### Interactive Dataset Insights")
    
    # KPI metrics row
    total_students = len(df)
    pass_count = df['Result'].sum()
    fail_count = total_students - pass_count
    pass_rate = (pass_count / total_students) * 100
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Total Records</div><div class="bento-metric-val">{total_students}</div>', unsafe_allow_html=True)
    with col_kpi2:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Pass Count</div><div class="bento-metric-val" style="color: #10b981;">{pass_count}</div>', unsafe_allow_html=True)
    with col_kpi3:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Fail Count</div><div class="bento-metric-val" style="color: #ef4444;">{fail_count}</div>', unsafe_allow_html=True)
    with col_kpi4:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Pass Rate</div><div class="bento-metric-val" style="color: #4f46e5;">{pass_rate:.1f}%</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4 Graphs Layout
    sns.set_theme(style="whitegrid")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        with st.container(border=True):
            # Chart 1: Study Hours vs Marks Scatter
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(
                data=df, 
                x='Hours_Study', 
                y='Final_Marks', 
                hue='Result', 
                palette={0: '#ef4444', 1: '#10b981'},
                alpha=0.7,
                ax=ax1
            )
            ax1.set_title("Study Hours vs Final Marks", fontsize=12, fontweight='bold', pad=10)
            ax1.set_xlabel("Hours of Study (Daily)")
            ax1.set_ylabel("Final Marks")
            ax1.legend(title="Outcome", labels=["Fail", "Pass"])
            st.pyplot(fig1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            # Chart 2: Pass/Fail Pie Chart
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            df['Result'].value_counts().plot.pie(
                autopct='%1.1f%%', 
                colors=['#10b981', '#ef4444'], 
                labels=['Pass', 'Fail'],
                startangle=90, 
                explode=[0.05, 0],
                ax=ax2
            )
            ax2.set_title("Overall Pass vs Fail Ratio", fontsize=12, fontweight='bold', pad=10)
            ax2.set_ylabel("")
            st.pyplot(fig2)
        
    with col_chart2:
        with st.container(border=True):
            # Chart 3: Attendance vs Marks Scatter
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(
                data=df, 
                x='Attendance', 
                y='Final_Marks', 
                hue='Result', 
                palette={0: '#ef4444', 1: '#10b981'},
                alpha=0.7,
                ax=ax3
            )
            ax3.set_title("Attendance vs Final Marks", fontsize=12, fontweight='bold', pad=10)
            ax3.set_xlabel("Class Attendance (%)")
            ax3.set_ylabel("Final Marks")
            ax3.legend(title="Outcome", labels=["Fail", "Pass"])
            st.pyplot(fig3)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            # Chart 4: Marks Distribution Histogram
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            sns.histplot(
                data=df, 
                x='Final_Marks', 
                kde=True, 
                color='#6366f1',
                bins=20,
                ax=ax4
            )
            ax4.axvline(50, color='#ef4444', linestyle='--', linewidth=2, label="Pass Threshold (50)")
            ax4.set_title("Distribution of Final Marks", fontsize=12, fontweight='bold', pad=10)
            ax4.set_xlabel("Final Marks")
            ax4.set_ylabel("Student Count")
            ax4.legend()
            st.pyplot(fig4)

# ==================== TAB 3: MODEL PERFORMANCE ====================
with tab3:
    st.markdown("### Model Evaluation Metrics")
    st.markdown("Logistic Regression Classifier trained on an 80/20 train/test split.")
    
    # Metrics Cards
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Accuracy</div><div class="bento-metric-val">{accuracy:.2%}</div>', unsafe_allow_html=True)
    with col_m2:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Precision</div><div class="bento-metric-val">{precision:.2%}</div>', unsafe_allow_html=True)
    with col_m3:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">Recall</div><div class="bento-metric-val">{recall:.2%}</div>', unsafe_allow_html=True)
    with col_m4:
        with st.container(border=True):
            st.markdown(f'<div class="bento-metric-label">F1 Score</div><div class="bento-metric-val">{f1:.2%}</div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_perf1, col_perf2 = st.columns(2, gap="large")
    
    with col_perf1:
        with st.container(border=True):
            st.markdown("#### **Confusion Matrix Heatmap**")
            fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
            sns.heatmap(
                cm, 
                annot=True, 
                fmt='d', 
                cmap='Blues', 
                xticklabels=['Predicted FAIL', 'Predicted PASS'],
                yticklabels=['Actual FAIL', 'Actual PASS'],
                cbar=False,
                ax=ax_cm
            )
            ax_cm.set_title("Confusion Matrix Heatmap", fontsize=12, fontweight='bold', pad=10)
            st.pyplot(fig_cm)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### **Feature Importance**")
            coefficients = model.coef_[0]
            feature_names = X.columns
            coef_df = pd.DataFrame({
                'Feature': feature_names,
                'Coefficient': coefficients
            }).sort_values(by='Coefficient', ascending=False)
            
            fig_imp, ax_imp = plt.subplots(figsize=(5, 3.5))
            sns.barplot(
                data=coef_df, 
                x='Coefficient', 
                y='Feature', 
                hue='Feature',
                palette='viridis',
                legend=False,
                ax=ax_imp
            )
            ax_imp.set_title("Feature Impact on Passing Probability", fontsize=12, fontweight='bold', pad=10)
            ax_imp.set_xlabel("Coefficient Weight (Scaled Inputs)")
            ax_imp.set_ylabel("Student Parameter")
            st.pyplot(fig_imp)
        
    with col_perf2:
        with st.container(border=True):
            st.markdown("#### **Metric Explanations**")
            st.markdown(
                """
                *   **Accuracy:** The percentage of overall correct predictions (both Pass and Fail) out of the total test set.
                *   **Precision:** Out of all students predicted to **PASS**, how many actually passed. High precision means low false alarm rate.
                *   **Recall (Sensitivity):** Out of all students who actually **passed**, how many did the model correctly identify. High recall means the model successfully captures most passing students.
                *   **F1 Score:** The harmonic mean of Precision and Recall. It provides a balanced assessment of model performance, especially when there is class imbalance.
                """
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### **Model Insights**")
            primary_feat = coef_df.iloc[0]['Feature']
            secondary_feat = coef_df.iloc[1]['Feature']
            st.markdown(
                f"""
                - **Primary Predictor:** Based on the model coefficients shown on the left, **{primary_feat}** has the highest positive impact on student success, followed by **{secondary_feat}**.
                - **Secondary Predictor:** A negative coefficient or a lower positive coefficient means that feature plays a smaller or inverse role when all other parameters are constant.
                """
            )
            st.markdown(
                """
                - **Linear Decision Boundary:** Logistic Regression fits a linear decision boundary on the scaled feature space, modeling success probability via the sigmoid function:
                  $$P(Y=1|X) = \\frac{1}{1 + e^{-\\theta^T X}}$$
                """
            )
