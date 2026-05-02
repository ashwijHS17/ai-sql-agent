import streamlit as st
import os
import sqlite3
import pandas as pd
from database import csv_to_sqlite
from agent import initialize_agent
from chart import plot_data

st.set_page_config(page_title="AI SQL Analyst", layout="wide")

st.title("🚀 AI SQL Data Analyst Agent")
st.markdown("### CSV → SQL → Insights")

# Sidebar for Setup
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password")
    uploaded_file = st.file_uploader("Upload CSV Data", type="csv")

if uploaded_file and api_key:
    # 1. Process CSV
    db_path, table_info = csv_to_sqlite(uploaded_file)
    
    if db_path:
        st.sidebar.success("CSV converted to SQLite successfully!")
        
        # 2. User Query Input
        query = st.text_input("Ask a question about your data (e.g., 'What is the average price?')")
        
        if query:
            agent = initialize_agent(db_path, api_key)
            
            with st.spinner("Analyzing data..."):
                # Run the Agent
                response = agent.invoke({"input": query})
                
                # Display Results
                st.subheader("🎯 Final Answer")
                st.write(response["output"])
                
                # Manual Data Retrieval for Visualization
                # Note: This executes the last logical query to show a table/chart
                conn = sqlite3.connect(db_path)
                preview_df = pd.read_sql_query(f"SELECT * FROM {table_info} LIMIT 10", conn)
                conn.close()
                
                st.subheader("📊 Data Preview & Visualization")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("Top 10 Rows:")
                    st.dataframe(preview_df)
                
                with col2:
                    chart_fig = plot_data(preview_df)
                    if chart_fig:
                        st.pyplot(chart_fig)
    else:
        st.error("Failed to process CSV file.")
else:
    st.info("Please provide a Groq API Key and upload a CSV to get started.")
