# Data-Driven Fiscal Forecasting for India  
### Project: [ArthaSutra-ML](https://github.com/StellarSolutions5/Data-Driven-Fiscal-Forecasting-for-India/projects?query=is%3Aopen)
### Organization: [StellarSolutions5](https://github.com/StellarSolutions5)

---

## Table of Contents  
- [Overview](#overview)
- [Dataset](#dataset)
- [Problem Statement](#problem-statement)
- [Approach](#approach)
- [Results](#results)
- [Future Scope](#future-scope)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Authors](#authors)

---

## Overview

**ArthaSutra-ML** is a deep learning-based fiscal forecasting system designed to modernize the prediction and visualization of India’s Union Budget. By leveraging historical financial data and machine learning models, it delivers accurate, scalable, and visually interactive forecasts for FY 2025–26.

### Unique Features
- End-to-end AI pipeline using RNN/LSTM  
- Trained on 27 years of data from [indiabudget.gov.in](https://www.indiabudget.gov.in)  
- Interactive Dash-based web dashboard  
- Real-time trend analysis with bar, line, and pie charts  
- Enables transparency and smarter fiscal planning  

---

## Dataset

### Source:
[Union Budget of India – Budget Documents](https://www.indiabudget.gov.in)

### Statements Used:
- **Statement I – Consolidated Fund of India**  
  - Revenue Account – Receipts  
  - Revenue Account – Disbursements  
  - Capital Account – Receipts  
  - Capital Account – Disbursements  
- **Statement I-A – Disbursements ‘Charged on the Consolidated Fund of India**  
- **Statement III – Public Account of India (Receipts and Disbursements)**  
- **Receipts and Expenditure of Union Territories without Legislature**

### Datasets Created:
- `budget_at_a_glance_predicted_dataset.xlsx`  
- `consolidated_fund_revenue_predicted_dataset.xlsx`  
- `consolidated_fund_capital_predicted_dataset.xlsx`  
- `public_account_predicted_dataset.xlsx`  
- `union_territories_without_legislature_predicted_dataset.xlsx`  

Each dataset spans from FY 1998 to FY 2024 with predictions for FY 2025–26.

---

## Problem Statement

Traditional fiscal planning in India relies heavily on static analysis and manual interpretations of budget documents. This leads to:

- Time-consuming analysis  
- Lack of interactive insights  
- Difficulty identifying future trends  

**ArthaSutra-ML** aims to:

- Forecast receipts, disbursements, and deficits  
- Provide real-time & data-driven insights  
- Promote transparent & intelligent policy-making  

---

## Approach

### 1. Data Preparation
- Excel files parsed and cleaned using `pandas`, `openpyxl`  
- 10 datasets structured for each budget component  

### 2. Forecasting Models
- Built with `TensorFlow/Keras`  
- RNN and LSTM trained and compared  
- Final deployment uses optimized RNNs  
- Scaled with `scikit-learn` using `scaler.pkl`  

### 3. Visualization & UI
- Web dashboard built with `Plotly Dash`  
- Modules for each dataset  
- Graph types:  
  - Line Charts – Trend forecasts  
  - Bar Charts – Category-wise comparison  
  - Pie Charts – Budget breakdown  

---

## Results

- **Accuracy:** Achieved 91–97% accuracy across categories  
- **Trends Forecasted:** Year-over-year growth, deficit trends, fund flows  
- **Visual Impact:**  
  - Data from 1998–2024 analyzed  
  - Forecasts for FY 2025–26  
  - Dynamic, downloadable graphs for decision-makers  

---

## Future Scope

- Integrate macroeconomic indicators (GDP, inflation, etc.)  
- Enhance with Prophet or Hybrid RNN-GRU models  
- Connect to real-time financial APIs  
- Multi-language, mobile-friendly dashboard  
- Add scenario simulators for policy experimentation  

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/StellarSolutions5/Data-Driven-Fiscal-Forecasting-for-India.git
cd Data-Driven-Fiscal-Forecasting-for-India

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
python app.py
```

---

## Project Structure

```bash
📁 Data-Driven-Fiscal-Forecasting-for-India/
├── 📁 assets/
├── 📁 indian-union-budget-data-statements/
├── 📁 models/
│   ├── 📁 budget_at_a_glance/
│   ├── 📁 consolidated_fund_revenue/
│   ├── 📁 consolidated_fund_capital/
│   ├── 📁 public_account/
│   └── 📁 union_territories_without_legislature/
├── 📁 __pycache__/
├── 📄 app.py
├── 📄 line_chart.py
├── 📄 requirements.txt
└── 📄 README.md
```

---

## Authors

- [Zainab Khan](https://github.com/ZainabKhan9)  
- [Mayuri Lakhotia](https://github.com/iMayuriLakhotia)  
- [Anuja Vaidya](https://github.com/AnujaVaidya15)  
- [Parul Nakhate](https://github.com/ParulNakhate1)  
- [Sakshi Kubitkar](https://github.com/Sakshisk22)  

---

