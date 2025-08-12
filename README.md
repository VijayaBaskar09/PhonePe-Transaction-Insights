# 📊 PhonePe Transaction Insights Dashboard

An interactive data analytics dashboard built with **Python**, **SQL**, and **Streamlit** to explore and visualize PhonePe digital transaction trends across India.  
This project extracts, processes, and visualizes data from the **PhonePe Pulse GitHub Dataset**, enabling insights into transaction amounts, counts, and top-performing regions.

---

## 📌 Features

### **Data Extraction & Processing**
- Load JSON data from PhonePe Pulse repository  
- Convert into structured tables  
- Store in PostgreSQL for efficient querying  

### **Interactive Streamlit Dashboard**
- **Home Page**: Overview and project introduction  
- **Data Exploration**: Year-wise & quarter-wise transaction trends  
- **Top Charts**: State & district-level leaders in transaction activity  
- **India Map Visualization**: Pydeck hexagon layer for spatial insights  

### **Key Metrics**
- **Transaction Amount** (₹ in millions)  
- **Transaction Count**  

---

## 🗂 Project Structure
├── phonepe.py              # Main Streamlit app
├── load_data.ipynb         # Data processing and loading scripts
├── requirements.txt        # Dependency list
├── phonepe.png             # Screenshot of dashboard
└── README.md               # Project overview


---

## ⚙️ Tech Stack
- **Python** – Data processing & dashboard backend  
- **PostgreSQL** – Database storage  
- **SQL** – Data querying  
- **Pandas** – Data manipulation  
- **Plotly & Pydeck** – Interactive visualizations  
- **Streamlit** – Web app framework
---

## Data Sources
- PhonePe Pulse dataset (link or reference where to obtain it)
- GeoJSON data for administrative boundaries (states/districts/pincodes)
---
## Usage
Navigate through the interactive visualizations on the Streamlit app
Use filters to explore metrics by timeframe and geography

## 📥 Installation & Setup

### 1️⃣ Clone the repository
    ```bash
git clone https://github.com/VijayaBaskar09/PhonePe-Transaction-Insights.git
cd PhonePe-Transaction-Insights

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Run the dashboard
streamlit run dashboard/app.py

