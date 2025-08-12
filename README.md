# PhonePe Transaction Insights

A dynamic **Streamlit dashboard** that visualizes and analyzes transaction trends across India using the **PhonePe Pulse dataset**.

##  Features

-  Interactive map-based visualizations (India state/district/pincode levels)  
-  Insights segmented by quarter and year  
-  Identify top-performing states, districts, and pincodes  
-  Interactive filters for in-depth exploration

##  Tech Stack

- **Python** • **Streamlit** • **Plotly** • **PostgreSQL** • **GeoJSON**

##  Demo

![Dashboard Preview](phonepe.png)

##  Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/VijayaBaskar09/PhonePe-Transaction-Insights.git
   cd PhonePe-Transaction-Insights

## Install dependencies
pip install -r requirements.txt

## Set up the database

Create a PostgreSQL database

Import the PhonePe Pulse dataset (add instructions or link the source)

Place GeoJSON files in the designated folder (if required)

## Run the dashboard
streamlit run phonepe.py

## Data Sources
PhonePe Pulse dataset (link or reference where to obtain it)

GeoJSON data for administrative boundaries (states/districts/pincodes)

## Usage
Navigate through the interactive visualizations on the Streamlit app

Use filters to explore metrics by timeframe and geography
