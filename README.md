# Student Result Prediction System

A Machine Learning-powered web application built with **Python**, **Streamlit**, and **scikit-learn** that predicts whether a student will pass or fail their final examinations based on key academic and lifestyle indicators.

Developed by **Derin Devis** (Reg No: 23F41A3314) in June 2026.

---

## 🚀 Features

### 1. 🔮 Interactive Prediction Engine
- Adjust student parameters in real-time using interactive slider controls:
  - **Daily Study Hours** (1.0 to 12.0 hours)
  - **Class Attendance** (40% to 100%)
  - **Previous Exam Marks** (30 to 100)
  - **Assignments Completed** (0 to 10)
  - **Daily Sleep Hours** (4.0 to 10.0 hours)
- Instantly predicts `PASS` or `FAIL` along with the model's confidence level.
- Generates and allows download of a professional **PDF Student Result Prediction Report** using ReportLab.

### 2. 📊 Interactive Data Analysis
- Displays key KPI metrics: **Total Records**, **Pass Count**, **Fail Count**, and **Pass Rate**.
- Renders four data visualization plots:
  - *Study Hours vs. Final Marks* (Scatter plot with Pass/Fail color codes)
  - *Class Attendance vs. Final Marks* (Scatter plot with Pass/Fail color codes)
  - *Overall Pass vs. Fail Ratio* (Pie chart)
  - *Distribution of Final Marks* (KDE histogram showing the pass threshold line)

### 3. ⚙️ Model Evaluation & Performance
- Standardizes features using `StandardScaler` and makes predictions via a `LogisticRegression` classifier.
- Displays key machine learning metrics: **Accuracy**, **Precision**, **Recall**, and **F1 Score**.
- Shows a **Confusion Matrix Heatmap** and a **Feature Importance Chart** displaying how much each parameter impacts the final result.

---

## 📁 Repository Structure

```
├── project.py                           # Main Streamlit web application
├── generate_dpr_derin.py                # Python script to compile the Detailed Project Report (DPR)
├── Student_Result_Prediction_DPR_Derin.pdf # The generated PDF project report
├── dashboard_tab1.png                   # Screenshot of the Prediction Tab UI
├── dashboard_tab2_1.png                 # Screenshot of Tab 2 (KPIs & Analysis)
├── dashboard_tab2_2.png                 # Screenshot of Tab 2 (Ratio & Marks Distribution)
├── dashboard_tab3_1.png                 # Screenshot of Tab 3 (Metrics & Confusion Matrix)
├── dashboard_tab3_2.png                 # Screenshot of Tab 3 (Feature Importance)
├── requirements.txt                     # List of Python library dependencies
└── README.md                            # Project documentation (this file)
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/derindevis/student-result-prediction.git
   cd student-result-prediction
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Web Application:**
   ```bash
   streamlit run project.py
   ```
