import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_data(df):
    """
    Attempts to visualize the dataframe based on its contents.
    """
    if df.empty or len(df.columns) < 2:
        st.warning("Not enough data columns to generate a chart.")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Basic logic: Plot first column as X and second as Y
    try:
        x_col = df.columns[0]
        y_col = df.columns[1]
        
        df.plot(kind='bar', x=x_col, y=y_col, ax=ax, color='skyblue')
        plt.title(f"{y_col} by {x_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Visualization error: {e}")
        return None
