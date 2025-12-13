import sqlite3
import pandas as pd
from datetime import datetime, date
import os

# --- Configuration ---
# Point directly to the database file in the project root
DB_PATH = 'retail_dw.db' 
OUTPUT_FILE = 'rfm_features.csv'

def calculate_rfm(db_path, output_file):
    """
    Calculates Recency, Frequency, and Monetary values for each customer 
    from the Data Warehouse and saves the result to a CSV.
    """
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found at '{db_path}'. Please ensure it exists.")
        return

    conn = sqlite3.connect(db_path)
    print("Connected to Data Warehouse. Starting RFM calculation...")

    # Define a snapshot date (the day after the last transaction date in the data)
    SNAPSHOT_DATE = datetime(2011, 12, 10) 

    # --- SQL Query to pull necessary data ---
    sql_query = """
    SELECT
        f.customer_id,
        f.sales_amount,
        f.invoice_no,
        t.date 
    FROM SalesFact f
    JOIN TimeDim t ON f.time_id = t.time_id;
    """
    
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    
    # Calculate RFM metrics
    rfm_df = df.groupby('customer_id').agg({
        'date': lambda x: (SNAPSHOT_DATE - pd.to_datetime(x).max()).days,  # Recency
        'invoice_no': 'nunique',  # Frequency
        'sales_amount': 'sum'  # Monetary
    }).reset_index()
    
    rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    # Save the resulting features to a CSV
    rfm_df.to_csv(output_file, index=False)

    print("\n--- RFM Feature Engineering Complete ---")
    print(f"Total Customers Processed: {len(rfm_df)}")
    print(f"RFM Features saved to: {output_file}")
    print("\nSample Data:")
    print(rfm_df.head().to_markdown(index=False))


if __name__ == '__main__':
    calculate_rfm(DB_PATH, OUTPUT_FILE)