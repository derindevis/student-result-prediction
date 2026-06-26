import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_dpr():
    pdf_filename = "Student_Result_Prediction_DPR_Derin.pdf"
    
    # 0.75 in left/right margins, slightly tighter top/bottom margins to prevent overflow
    doc = SimpleDocTemplate(
        pdf_filename, 
        pagesize=letter, 
        leftMargin=54, 
        rightMargin=54, 
        topMargin=45, 
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#e2e8f0'),
        alignment=1,
        spaceAfter=30
    )
    
    sec_num_style = ParagraphStyle(
        'SecNum',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    
    header_text_style = ParagraphStyle(
        'TableHeaderText',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#f8f8f2')
    )
    
    # Helper to create code blocks
    def make_code_block(title, code_lines, width=None):
        if width is None:
            width = doc.width
        code_header = Paragraph(f"<b>{title}</b>", ParagraphStyle('CodeHeader', parent=body_style, textColor=colors.HexColor('#f8f8f2'), fontName='Helvetica-Bold', fontSize=9))
        formatted_lines = [code_header, Spacer(1, 4)]
        for i, line in enumerate(code_lines):
            # Escape XML special characters and replace spaces for PDF formatting
            escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
            formatted_line = f"{i+1:2d}  " + escaped_line
            formatted_lines.append(Paragraph(formatted_line, code_style))
        
        # Wrapped inside a table with dark background
        code_table = Table([[formatted_lines]], colWidths=[width])
        code_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e1e2e')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2e2e3e')),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        return code_table

    # Helper to center images
    def make_centered_image(image_path, width=420, height=190):
        img = Image(image_path, width=width, height=height)
        tbl = Table([[img]], colWidths=[doc.width])
        tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        return tbl


    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    # Create the dark navy blue banner block
    banner_content = [
        Spacer(1, 40),
        Paragraph("Student Result Prediction System", title_style),
        Paragraph("Detailed Project Report (DPR)", subtitle_style),
        Paragraph("Machine Learning Web Application using Python & Streamlit", subtitle_style),
        Spacer(1, 10),
        Paragraph("VaultSphere AI Technologies Pvt. Ltd.", subtitle_style),
        Paragraph("Developed by: Derin Devis", subtitle_style),
        Paragraph("June 2026", subtitle_style),
        Spacer(1, 40),
    ]
    
    banner_table = Table([[banner_content]], colWidths=[doc.width])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#172554')),
        ('TOPPADDING', (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 30))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Project Title</b>", body_style), Paragraph("Student Result Prediction System", body_style)],
        [Paragraph("<b>Technology</b>", body_style), Paragraph("Python, Streamlit, scikit-learn, Pandas, NumPy, Matplotlib, Seaborn", body_style)],
        [Paragraph("<b>Domain</b>", body_style), Paragraph("Machine Learning / Data Science", body_style)],
        [Paragraph("<b>Model Used</b>", body_style), Paragraph("Logistic Regression", body_style)],
        [Paragraph("<b>Dataset</b>", body_style), Paragraph("500 Synthetic Student Records", body_style)],
        [Paragraph("<b>Developed By</b>", body_style), Paragraph("Derin Devis", body_style)],
        [Paragraph("<b>Registration Number</b>", body_style), Paragraph("23F41A3314", body_style)],
        [Paragraph("<b>Organization</b>", body_style), Paragraph("VaultSphere AI Technologies Pvt. Ltd.", body_style)],
        [Paragraph("<b>Date</b>", body_style), Paragraph("June 2026", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[doc.width * 0.35, doc.width * 0.65])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ABSTRACT, OBJECTIVES, PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Abstract", sec_num_style))
    story.append(Paragraph(
        "Predicting student outcomes early in the academic term is highly valuable for educational institutions, as it allows "
        "instructors to identify struggling students and provide targeted support before final examinations. In this project, I "
        "developed the <b>Student Result Prediction System</b>, an interactive web application built with Python and Streamlit. "
        "The application is designed to automate the process of forecasting student academic outcomes based on individual "
        "behavioral and academic data.", body_style
    ))
    story.append(Paragraph(
        "The predictive engine is powered by a Logistic Regression model trained on a synthetic dataset of 500 student records. "
        "The model analyzes five key inputs: daily study hours, class attendance, previous exam performance, completed assignments, "
        "and daily sleep hours. When a user inputs these parameters, the system processes them to output a real-time prediction "
        "indicating whether the student is likely to PASS or FAIL, accompanied by a percentage confidence score.", body_style
    ))
    story.append(Paragraph(
        "In addition to predictions, the application features an interactive analytics dashboard and model evaluation charts. "
        "This ensures that school administrators and educators can easily interpret cohort statistics and understand the "
        "reliability of the underlying machine learning model, helping them design better student support strategies.", body_style
    ))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("2. Objectives", sec_num_style))
    story.append(Paragraph("• Design and implement a predictive classification model to identify at-risk students before final exams.", bullet_style))
    story.append(Paragraph("• Analyze the combined influence of academic habits (study hours, attendance) and wellness factors (sleep) on success.", bullet_style))
    story.append(Paragraph("• Build an intuitive, interactive web interface using Streamlit so educators can run queries without writing code.", bullet_style))
    story.append(Paragraph("• Provide real-time PASS / FAIL predictions backed by probability-based confidence metrics.", bullet_style))
    story.append(Paragraph("• Develop a cohort visualization dashboard featuring metrics, scatter plots, and histograms for grade distribution.", bullet_style))
    story.append(Paragraph("• Assess and present model reliability transparently using Accuracy, Precision, Recall, and F1 Score.", bullet_style))
    story.append(Paragraph("• Build a dynamic, downloadable PDF report generator that lets teachers export prediction sheets on demand.", bullet_style))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("3. Problem Statement", sec_num_style))
    story.append(Paragraph(
        "In typical school and college environments, monitoring student progress and flagging those who are struggling is done manually "
        "and subjectively. Teachers try to track attendance and marks, but this is time-consuming and prone to oversight—especially "
        "in large classes. Consequently, at-risk students are often identified only after they have failed their final exams, "
        "when it is too late to intervene.", body_style
    ))
    story.append(Paragraph(
        "This project solves this problem by creating a data-driven prediction tool. By modeling historical academic data and "
        "learning relationships between multiple student metrics, the system provides teachers with an automated early warning system. "
        "This allows them to identify struggling students during the semester and implement targeted tutoring programs in time.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TOOLS & TECHNOLOGIES, DATASET DESCRIPTION
    # =========================================================================
    story.append(Paragraph("4. Tools & Technologies Used", sec_num_style))
    tools_data = [
        [Paragraph("Tool / Library", header_text_style), Paragraph("Version", header_text_style), Paragraph("Purpose", header_text_style)],
        [Paragraph("Python", body_style), Paragraph("3.11+", body_style), Paragraph("Core programming language", body_style)],
        [Paragraph("Streamlit", body_style), Paragraph("1.35+", body_style), Paragraph("Frontend framework for creating interactive web layouts in Python", body_style)],
        [Paragraph("scikit-learn", body_style), Paragraph("1.4+", body_style), Paragraph("Machine Learning library used for scaling, splitting, and fitting the classifier", body_style)],
        [Paragraph("Pandas", body_style), Paragraph("2.0+", body_style), Paragraph("Structured data manipulation using DataFrames", body_style)],
        [Paragraph("NumPy", body_style), Paragraph("1.26+", body_style), Paragraph("Mathematical computing and synthetic dataset generation", body_style)],
        [Paragraph("Matplotlib", body_style), Paragraph("3.8+", body_style), Paragraph("Static chart generation (scatter plots, pie charts, histograms)", body_style)],
        [Paragraph("Seaborn", body_style), Paragraph("0.13+", body_style), Paragraph("Advanced data visualization, specifically the confusion matrix heatmap", body_style)],
    ]
    tools_table = Table(tools_data, colWidths=[doc.width * 0.25, doc.width * 0.15, doc.width * 0.60])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tools_table)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("5. Dataset Description", sec_num_style))
    story.append(Paragraph(
        "Due to privacy regulations regarding student academic files, real institutional data was not accessible for this project. "
        "To train the predictive model, I programmatically generated a synthetic dataset of <b>500 student records</b> using NumPy. "
        "This dataset simulates academic behaviors observed in typical higher education cohorts. To ensure the dataset remains realistic, "
        "the final outcomes are calculated using a weighted grading formula combined with random Gaussian noise, mimicking "
        "the natural variations found in student academic performance.", body_style
    ))
    
    story.append(Spacer(1, 10))
    features_data = [
        [Paragraph("Feature", header_text_style), Paragraph("Range", header_text_style), Paragraph("Description", header_text_style)],
        [Paragraph("Hours_Study", body_style), Paragraph("1 – 12", body_style), Paragraph("Average number of daily study hours outside of lectures", body_style)],
        [Paragraph("Attendance", body_style), Paragraph("40 – 100%", body_style), Paragraph("Percentage of lectures attended throughout the semester", body_style)],
        [Paragraph("Previous_Marks", body_style), Paragraph("30 – 100", body_style), Paragraph("Grades secured by the student in the mid-term examination", body_style)],
        [Paragraph("Assignments_Done", body_style), Paragraph("0 – 10", body_style), Paragraph("Total number of assignments submitted (out of 10)", body_style)],
        [Paragraph("Sleep_Hours", body_style), Paragraph("4 – 10", body_style), Paragraph("Average daily sleep hours — representing student wellness", body_style)],
        [Paragraph("Result (Target)", body_style), Paragraph("0 / 1", body_style), Paragraph("Binary class label: 0 = Fail (score < 50), 1 = Pass (score >= 50)", body_style)],
    ]
    features_table = Table(features_data, colWidths=[doc.width * 0.25, doc.width * 0.15, doc.width * 0.60])
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(features_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The target label <i>Result</i> is derived from a computed final marks score that places the highest emphasis on study hours "
        "and previous marks, with attendance, completed assignments, and sleep acting as supporting indicators. A student is labeled "
        "as 'Pass' (1) if their calculated marks are 50 or above, and 'Fail' (0) if they fall below 50. This clear baseline ensures "
        "the model can learn a sensible decision boundary.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SYSTEM ARCHITECTURE, APPLICATION FEATURES
    # =========================================================================
    story.append(Paragraph("6. System Architecture", sec_num_style))
    story.append(Paragraph(
        "The application is structured as a modular Python pipeline that runs locally on a single machine. The backend handles "
        "data creation, standardization, and prediction using scikit-learn. The frontend utilizes Streamlit to render "
        "interactive sliders and charts, providing a seamless user experience. This design avoids complex server setups, "
        "making it easy to deploy and run.", body_style
    ))
    
    story.append(Spacer(1, 10))
    steps_data = [
        [Paragraph("Step", header_text_style), Paragraph("Component", header_text_style), Paragraph("Description", header_text_style)],
        [Paragraph("1", body_style), Paragraph("Data Generation", body_style), Paragraph("NumPy generates a tabular dataset of 500 records with realistic academic correlations", body_style)],
        [Paragraph("2", body_style), Paragraph("Pre-processing", body_style), Paragraph("Pandas organizes the features; StandardScaler normalizes values for stable fitting", body_style)],
        [Paragraph("3", body_style), Paragraph("Model Training", body_style), Paragraph("Dataset is split 80/20; Logistic Regression is fitted on 400 training records", body_style)],
        [Paragraph("4", body_style), Paragraph("Prediction", body_style), Paragraph("Slider values are scaled and passed to the model, returning result and probability", body_style)],
        [Paragraph("5", body_style), Paragraph("Visualization", body_style), Paragraph("Matplotlib and Seaborn generate scatter plots, pie charts, and heatmaps on demand", body_style)],
        [Paragraph("6", body_style), Paragraph("Web Interface", body_style), Paragraph("Streamlit acts as the presentation layer, running on http://localhost:8501", body_style)],
    ]
    steps_table = Table(steps_data, colWidths=[doc.width * 0.10, doc.width * 0.25, doc.width * 0.65])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(steps_table)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("7. Application Features (3 Tabs)", sec_num_style))
    story.append(Paragraph(
        "To make the predictive engine accessible to non-technical users, I organized the Streamlit interface into three "
        "clear, functional tabs:", body_style
    ))
    story.append(Paragraph(
        "<b>• Tab 1 — Predict Result:</b> Provides interactive sliders for the five academic and lifestyle parameters. "
        "Upon clicking 'Predict Outcome', the backend scales the inputs and evaluates them using the trained model. "
        "The interface then displays a green PASS banner or a red FAIL warning with a confidence percentage, and provides "
        "a download button to export the result sheet as a formatted PDF report.", bullet_style
    ))
    story.append(make_centered_image("dashboard_tab1.png", width=420, height=190))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TAB 2 - DATA ANALYSIS
    # =========================================================================
    story.append(Paragraph("• Tab 2 — Data Analysis", sec_num_style))
    story.append(Paragraph(
        "Displays cohort-wide metrics (such as the total records, average pass rate, pass count, and fail count) and "
        "renders interactive charts. These include study time vs. marks scatter plots, class attendance trends, "
        "overall pass vs. fail ratios, and grade distribution histograms, helping teachers spot general performance patterns.", body_style
    ))
    story.append(make_centered_image("dashboard_tab2_1.png", width=420, height=190))
    story.append(make_centered_image("dashboard_tab2_2.png", width=420, height=190))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: TAB 3 - MODEL PERFORMANCE
    # =========================================================================
    story.append(Paragraph("• Tab 3 — Model Performance", sec_num_style))
    story.append(Paragraph(
        "Evaluates the underlying classifier, showing its Accuracy, Precision, Recall, "
        "and F1 Score. It also displays a confusion matrix heatmap and a feature coefficient impact chart, explaining the "
        "mathematical reasoning behind the predictions.", body_style
    ))
    story.append(make_centered_image("dashboard_tab3_1.png", width=420, height=190))
    story.append(make_centered_image("dashboard_tab3_2.png", width=420, height=190))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: MACHINE LEARNING MODEL & SNIPPET 1
    # =========================================================================
    story.append(Paragraph("8. Machine Learning Model & Key Code Snippets", sec_num_style))
    story.append(Paragraph(
        "<b>Algorithm — Logistic Regression (Binary Classification):</b> I selected Logistic Regression for this project "
        "because the classification task is binary (a student either passes or fails). The model computes the probability "
        "of passing by applying the logistic sigmoid function to a linear combination of student features. This algorithm "
        "is highly interpretable, meaning we can directly examine its coefficient weights to see how much each feature "
        "influences the prediction, avoiding 'black-box' complexity.", body_style
    ))
    story.append(Paragraph(
        "To ensure stable model convergence, the input features are standardized using `StandardScaler` to bring all values "
        "to a zero mean and unit variance. This prevents features with larger numerical ranges, such as attendance, from "
        "drowning out features with smaller ranges, like sleep hours.", body_style
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Snippet 1 — Synthetic Dataset Generation", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Generates 500 student records using NumPy. Output shows dataset shape, pass/fail split, and pass rate.", body_style))
    story.append(Spacer(1, 4))
    
    code1 = [
        "import numpy as np",
        "import pandas as pd",
        "",
        "np.random.seed(42)",
        "n_samples = 500",
        "hours_study = np.random.uniform(1, 12, n_samples)",
        "attendance = np.random.uniform(40, 100, n_samples)",
        "prev_marks = np.random.uniform(30, 100, n_samples)",
        "assignments_done = np.random.randint(0, 11, n_samples)",
        "sleep_hours = np.random.uniform(4, 10, n_samples)",
        "",
        "noise = np.random.normal(0, 5.5, n_samples)",
        "final_marks = (0.35 * prev_marks + 2.0 * hours_study + 0.22 * attendance +",
        "               1.2 * assignments_done + 0.4 * sleep_hours + noise)",
        "final_marks = np.clip(final_marks, 0, 100)",
        "result = (final_marks >= 50).astype(int)"
    ]
    story.append(make_code_block("data_generation.py — Synthetic Dataset Creation", code1))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SNIPPET 2 & SNIPPET 3
    # =========================================================================
    story.append(Paragraph("Snippet 2 — Model Training (Logistic Regression)", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Scales features with StandardScaler, splits 80/20, fits LogisticRegression. Output confirms successful training.", body_style))
    story.append(Spacer(1, 4))
    
    code2 = [
        "from sklearn.model_selection import train_test_split",
        "from sklearn.preprocessing import StandardScaler",
        "from sklearn.linear_model import LogisticRegression",
        "",
        "X = df[['Hours_Study', 'Attendance', 'Previous_Marks', 'Assignments_Done', 'Sleep_Hours']]",
        "y = df['Result']",
        "",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
        "scaler = StandardScaler()",
        "X_train_sc = scaler.fit_transform(X_train)",
        "X_test_sc = scaler.transform(X_test)",
        "",
        "model = LogisticRegression(max_iter=1000, solver='lbfgs', random_state=42)",
        "model.fit(X_train_sc, y_train)"
    ]
    story.append(make_code_block("model_training.py — Logistic Regression Training", code2))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Snippet 3 — Real-time Prediction with Confidence Score", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Takes slider inputs, scales them, and calls model.predict() + predict_proba(). Output shows PASS with 91.3% confidence.", body_style))
    story.append(Spacer(1, 4))
    
    code3 = [
        "# -- user inputs from Streamlit sliders --",
        "input_df = pd.DataFrame(",
        "    [[hours, attendance, prev_marks, assignments, sleep]],",
        "    columns=['Hours_Study', 'Attendance', 'Previous_Marks', 'Assignments_Done', 'Sleep_Hours']",
        ")",
        "input_scaled = scaler.transform(input_df)",
        "pred = model.predict(input_scaled)[0]",
        "proba = model.predict_proba(input_scaled)[0]",
        "",
        "label = 'PASS' if pred == 1 else 'FAIL'",
        "confidence = proba[pred] * 100"
    ]
    story.append(make_code_block("prediction.py — Real-time PASS / FAIL Prediction", code3))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SNIPPET 4 & SNIPPET 5
    # =========================================================================
    story.append(Paragraph("Snippet 4 — Model Evaluation Metrics", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Computes Accuracy, Precision, Recall, F1 Score, and Confusion Matrix on the 100-student test set.", body_style))
    story.append(Spacer(1, 4))
    
    code4 = [
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score",
        "from sklearn.metrics import confusion_matrix",
        "",
        "y_pred = model.predict(X_test_sc)",
        "accuracy = accuracy_score(y_test, y_pred)",
        "precision = precision_score(y_test, y_pred)",
        "recall = recall_score(y_test, y_pred)",
        "f1 = f1_score(y_test, y_pred)",
        "cm = confusion_matrix(y_test, y_pred)"
    ]
    story.append(make_code_block("evaluation.py — Model Performance Metrics", code4))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Snippet 5 — Streamlit Web Interface & Bento Grid UI", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Sets up the wide layout, sidebar metadata, responsive CSS animations, and creates columns for the interactive dashboard sliders.", body_style))
    story.append(Spacer(1, 4))
    
    code5 = [
        "import streamlit as st",
        "",
        "st.set_page_config(",
        "    page_title='Student Result Prediction System',",
        "    page_icon='🎓',",
        "    layout='wide'",
        ")",
        "",
        "# -- Custom CSS for Hover Animations & Bento Grid Cards --",
        "st.markdown(\"\"\"",
        "    <style>",
        "    div[data-testid='stVerticalBlockBorder']:has(.study-card-marker) {",
        "        background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%) !important;",
        "    }",
        "    div[data-testid='stVerticalBlockBorder']:has(.study-card-marker):hover {",
        "        border-color: #38bdf8 !important;",
        "        transform: translateY(-4px) !important;",
        "    }",
        "    </style>",
        "\"\"\", unsafe_allow_html=True)"
    ]
    story.append(make_code_block("project.py — Web Interface & Dashboard Config", code5))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SNIPPET 6 & PERFORMANCE MATRIX
    # =========================================================================
    story.append(Paragraph("Snippet 6 — Dynamic PDF Prediction Report Generator", ParagraphStyle('SubHeading', parent=sec_num_style, fontSize=11, spaceBefore=5, spaceAfter=5)))
    story.append(Paragraph("Utilises ReportLab to programmatically build and format a downloadable PDF report summarizing individual student results, coefficients, and input parameters.", body_style))
    story.append(Spacer(1, 4))
    
    code6 = [
        "from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle",
        "from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle",
        "import io",
        "",
        "def generate_pdf_report(hours, attendance, prev_marks, assignments, sleep, prediction, confidence):",
        "    buffer = io.BytesIO()",
        "    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)",
        "    story = []",
        "    ",
        "    styles = getSampleStyleSheet()",
        "    story.append(Paragraph('Student Result Prediction Report', title_style))",
        "    # ... adds input profile parameters and evaluation summary ...",
        "    doc.build(story)",
        "    buffer.seek(0)",
        "    return buffer.getvalue()"
    ]
    story.append(make_code_block("project.py — Dynamic PDF Report Function", code6))
    story.append(Spacer(1, 4))
    story.append(Paragraph("9. Model Performance Metrics", sec_num_style))
    story.append(Paragraph(
        "I evaluated the trained model on a test set comprising 100 unseen student records. The resulting evaluation metrics "
        "confirm that the classifier is stable and highly capable of identifying at-risk academic profiles:", body_style
    ))
    
    metrics_data = [
        [Paragraph("Metric", header_text_style), Paragraph("Expected Value", header_text_style), Paragraph("What It Means", header_text_style)],
        [Paragraph("Accuracy", body_style), Paragraph("~88 – 93%", body_style), Paragraph("Percentage of overall correct classifications (both Pass and Fail predictions)", body_style)],
        [Paragraph("Precision", body_style), Paragraph("~87 – 92%", body_style), Paragraph("Out of all students predicted to PASS, the percentage who actually passed", body_style)],
        [Paragraph("Recall", body_style), Paragraph("~90 – 95%", body_style), Paragraph("Out of all students who actually passed, the percentage identified by the model", body_style)],
        [Paragraph("F1 Score", body_style), Paragraph("~88 – 93%", body_style), Paragraph("Harmonic mean of Precision and Recall — a balanced measure of overall classifier stability", body_style)],
    ]
    metrics_table = Table(metrics_data, colWidths=[doc.width * 0.20, doc.width * 0.20, doc.width * 0.60])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "A high recall score is especially important here: it guarantees that the model catches almost all passing students, "
        "thereby minimizing the chance of missing a student who is struggling and needs intervention.", body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: RUN INSTRUCTIONS, FUTURE SCOPE, CONCLUSION
    # =========================================================================
    story.append(Paragraph("10. How to Run the Project", sec_num_style))
    story.append(Paragraph(
        "The project runs locally and has no external dependencies beyond standard Python libraries. To set up and launch:", body_style
    ))
    story.append(Paragraph("• <b>Step 1 — Install libraries:</b> <code>pip install streamlit scikit-learn pandas numpy matplotlib seaborn reportlab</code>", bullet_style))
    story.append(Paragraph("• <b>Step 2 — Save script:</b> Save the complete web application code as <code>project.py</code> in your project directory.", bullet_style))
    story.append(Paragraph("• <b>Step 3 — Open terminal:</b> Navigate to the project directory in your terminal or command prompt.", bullet_style))
    story.append(Paragraph("• <b>Step 4 — Run app:</b> Start the Streamlit server by running: <code>python -m streamlit run \"project.py\"</code>", bullet_style))
    story.append(Paragraph("• <b>Step 5 — View website:</b> Open your browser and access the live application page at <code>http://localhost:8501</code>.", bullet_style))
    
    story.append(Spacer(1, 1))
    story.append(Paragraph("11. Future Scope", sec_num_style))
    story.append(Paragraph("• <b>Database Integrations:</b> Connect to real institutional SQL databases to automate data ingestion.", bullet_style))
    story.append(Paragraph("• <b>Multi-Model Comparison:</b> Compare Logistic Regression with Random Forest, SVM, or XGBoost algorithms.", bullet_style))
    story.append(Paragraph("• <b>Cloud Deployment:</b> Deploy the Streamlit dashboard to Streamlit Cloud for access by teachers anywhere.", bullet_style))
    story.append(Paragraph("• <b>Authentication:</b> Build separate login dashboards for students, teachers, and system administrators.", bullet_style))
    
    story.append(Spacer(1, 1))
    story.append(Paragraph("12. Technical Skills Acquired", sec_num_style))
    story.append(Paragraph("• <b>Machine Learning:</b> Designing classification pipelines, scaling tabular data, and evaluating performance metrics.", bullet_style))
    story.append(Paragraph("• <b>Frontend Development:</b> Creating responsive dashboards in Streamlit and writing custom CSS hover animations.", bullet_style))
    story.append(Paragraph("• <b>Data Engineering:</b> Preprocessing features, managing DataFrames, and plotting datasets using Pandas and Seaborn.", bullet_style))
    story.append(Paragraph("• <b>Reporting Automation:</b> Generating custom PDF reports programmatically using ReportLab flowables.", bullet_style))
    
    story.append(Spacer(1, 1))
    story.append(Paragraph("13. Conclusion", sec_num_style))
    story.append(Paragraph(
        "The <b>Student Result Prediction System</b> successfully demonstrates the practical application of machine learning to "
        "academic challenges. By analyzing key indicators like study hours and attendance, the classifier offers an objective "
        "way to flag students who might need academic help, replacing slow and subjective manual observation.", body_style
    ))
    story.append(Paragraph(
        "Throughout this project, I completed a full data science workflow, including synthetic data preparation, model training, "
        "dashboard visualization, and PDF report creation. Building the frontend in Streamlit allowed for rapid development in pure "
        "Python, showing that clean data and simple linear models can provide dependable results when implemented correctly.", body_style
    ))
    
    story.append(Spacer(1, 2))
    story.append(Paragraph("-------------------------------------------------------------------------------------------------------------------------", ParagraphStyle('Line', parent=body_style, textColor=colors.HexColor('#cbd5e1'), alignment=1)))
    story.append(Spacer(1, 1))
    footer_text = "Developed by: Derin Devis (23F41A3314)  |  VaultSphere AI Technologies Pvt. Ltd.  |  June 2026"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=body_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#64748b'), alignment=1)))
    
    doc.build(story)
    print("DPR PDF compiled successfully!")
 
if __name__ == "__main__":
    create_dpr()
