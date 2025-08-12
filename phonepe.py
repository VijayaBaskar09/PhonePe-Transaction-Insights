import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import psycopg2
import requests
import json

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="phonepe_insights",
        user="postgres",
        password="mblaze0912"
    )

st.set_page_config(layout= "wide")

st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
st.write("")
with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])

if select == "Home":
    
    col1,col2= st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
    with col2:
        st.video("C:\Users\user\OneDrive\Desktop\Capstone_Project\Phonepe Ad.mp4")

elif select == "Top Charts":
    st.header("📊 Top Charts")
  
    def run_query(query):
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
        
    case_study = st.selectbox(
                "Choose a Business Case Study",
                [
                    "Transaction Dynamics",
                    "Device Engagement",
                    "Insurance Growth",
                    "State/District Performance",
                    "Insurance Engagement",
                    "Insurance Transactions"
                ]
            )
        

    # --- Common Selection ---
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024])
    quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])

        # --- Case Logic ---
    if case_study == "Transaction Dynamics":
        st.header("📊 Transaction Dynamics Across States and Quarters")
        query = f'''
                SELECT states, years, quarter,
                    SUM(transaction_amount) AS total_amount,
                    SUM(transaction_count) AS total_count
                FROM aggregated_transaction
                WHERE years = {year} AND quarter = {quarter}
                GROUP BY states, years, quarter
                ORDER BY states;
            '''
        df = run_query(query)
        fig = px.bar(df, x="states", y="total_amount", color="states")
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

    elif case_study == "Device Engagement":
        st.header("📱 Device Brand vs App Engagement")
        query = f'''
                SELECT Brands AS device_brand,
                    SUM(Transaction_count) AS total_users,
                    SUM(Percentage) AS total_opens
                FROM aggregated_user
                WHERE Years = {year} AND Quarter = {quarter}
                GROUP BY Brands
                ORDER BY total_opens DESC;
            '''
        df = run_query(query)
        if df.empty:
            st.warning(f"No data available for Year {year} and Quarter {quarter}.")
        else:
            fig = px.bar(df, x="device_brand", y=["total_users", "total_opens"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)

    elif case_study == "Insurance Growth":
        st.warning("Note: This chart ignores the selected Quarter and shows all quarters for selected year.")

        st.header("📈 Insurance Transactions by State")
        query = f'''
                    SELECT states, years, quarter,
                        SUM(insurance_count) AS count,
                        SUM(insurance_amount) AS amount
                    FROM aggregated_insurance
                    WHERE years = {year}
                    GROUP BY states, years, quarter
                    ORDER BY states, quarter;
                '''
        df = run_query(query)
        fig = px.line(df, x="quarter", y="count", color="states", title=f"Insurance Count Across Quarters in {year}")
        st.plotly_chart(fig, use_container_width=True)

    elif case_study == "State/District Performance":
        st.header("📌 Top Transaction Locations")
        query = f'''
                SELECT States, Pincodes,
                    SUM(Transaction_amount) AS total_amount,
                    SUM(Transaction_count) AS total_count
                FROM top_transaction
                WHERE Years = {year} AND Quarter = {quarter}
                GROUP BY States, Pincodes
                ORDER BY total_amount DESC;
            '''
        df = run_query(query)
        df["pincodes"] = df["pincodes"].astype(str)
        fig = px.scatter(df, x="states", y="total_amount", size="total_amount",
        color="pincodes", hover_name="pincodes", size_max=40)
        st.plotly_chart(fig, use_container_width=True)

    elif case_study == "Insurance Engagement":
        st.header("🛡️ District-wise Insurance Performance")
        query = f'''
                SELECT States, Pincodes,
                    SUM(Transaction_count) AS total_count,
                    SUM(Transaction_amount) AS total_amount
                FROM top_insurance
                WHERE Years = {year} AND Quarter = {quarter}
                GROUP BY States, Pincodes
                ORDER BY total_count DESC;
            '''
        df = run_query(query)
        fig = px.treemap(df, path=["states", "pincodes"], values="total_count")
        st.plotly_chart(fig, use_container_width=True)


    elif case_study == "Insurance Transactions":
        st.header("💼 Insurance Transaction Trends")
        query = f'''
                SELECT States, Pincodes,
                    SUM(Transaction_count) AS total_count
                FROM top_insurance
                WHERE Years = {year} AND Quarter = {quarter}
                GROUP BY States, Pincodes
                ORDER BY total_count DESC;
            '''
        df = run_query(query)
        fig = px.pie(df, names="states", values="total_count", hole=0.4)
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

elif select   == "Data Exploration":
    st.title("📊:violet[ Compare All PhonePe Metrics by State]")

    def run_query(query):
        conn = psycopg2.connect(
            host="localhost",
            database="phonepe_insights",
            user="postgres",
            password="mblaze0912"
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    # --- Inputs ---
    data_type = st.selectbox("Select Data Table", [
        "aggregated_transaction",
        "aggregated_insurance",
        "aggregated_user",
        "map_transaction",
        "map_insurance",
        "map_user",
        "top_transaction",
        "top_insurance",
        "top_user"
    ])

    metric = st.radio("Select Metric", ["Amount", "Count"], horizontal=True)
    chart_type = st.radio("Select Chart Type", ["Map", "Bar Chart"], horizontal=True)
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024])
    quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])

    # --- Metric Column Mapping ---
    column_map = {
        "aggregated_transaction": ("transaction_amount", "transaction_count"),
        "aggregated_insurance": ("insurance_amount", "insurance_count"),
        "aggregated_user": (None, "transaction_count"),
        "map_transaction": ("transaction_amount", "transaction_count"),
        "map_insurance": ("transaction_amount", "transaction_count"),
        "map_user": (None, "AppOpens"),
        "top_transaction": ("transaction_amount", "transaction_count"),
        "top_insurance": ("transaction_amount", "transaction_count"),
        "top_user": (None, "registered_users"),
    }

    amount_col, count_col = column_map[data_type]
    if metric == "Amount":
        if amount_col is None:
            st.error(f"❌ 'Amount' metric is not available for the '{data_type}' table.")
            st.stop()
        color_col = amount_col
    else:
        if count_col is None:
            st.error(f"❌ 'Count' metric is not available for the '{data_type}' table.")
            st.stop()
        color_col = count_col

    color_col = amount_col if metric == "Amount" else count_col


    # --- Construct SQL Query ---
    if data_type.startswith("aggregated"):
        query = f'''
            SELECT states, SUM({color_col}) AS value
            FROM {data_type}
            WHERE years = {year} AND quarter = {quarter}
            GROUP BY states;
        '''
    elif data_type.startswith("map"):
        query = f'''
            SELECT states, SUM({color_col}) AS value
            FROM {data_type}
            WHERE years = {year} AND quarter = {quarter}
            GROUP BY states;
        '''
    elif data_type.startswith("top"):
        query = f'''
            SELECT states, SUM({color_col}) AS value
            FROM {data_type}
            WHERE years = {year} AND quarter = {quarter}
            GROUP BY states;
        '''

    df = run_query(query)
    df["states"] = df["states"].str.title()

    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_states = requests.get(geo_url).json()

    # --- Plotting ---
    if chart_type == "Map":
        if metric == 'Amount':
            # Convert value column to millions for display
            df["value_in_millions"] = df["value"] / 1_000_000

            fig = px.choropleth(
                df,
                geojson=india_states,
                featureidkey="properties.ST_NM",
                locations="states",
                color="value",  # actual value still used for coloring
                hover_name="states",
                custom_data=["value_in_millions"],  # use for hover template
                color_continuous_scale="Viridis",
                title=f"{metric} from {data_type} - {year} Q{quarter}"
            )

            fig.update_geos(fitbounds="locations", visible=False)

            fig.update_traces(
                    hovertemplate="<b>%{location}</b><br>" + metric + ": ₹ %{customdata[0]:.2f}M<extra></extra>"
                )

            fig.update_coloraxes(colorbar_title="₹ (Full Value)")

            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.choropleth(
                df,
                geojson=india_states,
                featureidkey="properties.ST_NM",
                locations="states",
                color="value",
                color_continuous_scale="Viridis",
                title=f"{metric} from {data_type} - {year} Q{quarter}"
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)
        

    else:
        fig = px.bar(
            df.sort_values("value", ascending=False),
            x="states", y="value", color="states",
            title=f"{metric} from {data_type} - {year} Q{quarter}"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # --- Download Option ---
    st.download_button("Download CSV", df.to_csv(index=False), file_name=f"{data_type}_{year}_Q{quarter}.csv")