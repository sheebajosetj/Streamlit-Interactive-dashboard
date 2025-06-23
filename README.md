# 📊 Superstore EDA Dashboard

This is a **Streamlit-based interactive dashboard** for performing **Exploratory Data Analysis (EDA)** on Superstore sales data. It allows users to upload data, filter by date/region/state/city, and visualize key metrics through charts, tables, and downloadable reports.

---

## Features

File Upload (CSV, Excel)  
Date Range Filtering  
Region, State, City Filtering  
Category-wise and Region-wise Sales Visualizations  
Monthly Time Series Analysis  
Scatter Plot of Sales vs Profit  
Expandable Data Tables with Gradient Styling  
Download Buttons for Each Section  
Default fallback to local Superstore.csv (if no upload)

---

## Dashboard Preview


---

## File Structure

superstore_dashboard/
├── Superstore.csv
├── app.py
├── README.md
└── requirements.txt

---

## Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/superstore-dashboard.git
   cd superstore-dashboard
   ```
(Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
```
```bash
pip install -r requirements.txt
Run the app
```

```bash
streamlit run app.py
```

View in your browser
Streamlit will open the dashboard automatically. If not, go to http://localhost:8501.

