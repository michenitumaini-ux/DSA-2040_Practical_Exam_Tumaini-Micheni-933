
import pandas as pd
import sqlite3
from datetime import datetime

# --- Configuration ---
DATA_FILE = 'Online Retail.xlsx'
DB_NAME = 'retail_dw.db'

SHEET_NAME = 'Online Retail' 

def extract_data(file_path, sheet_name):
    """
    Extracts data from the raw Excel file.
    """
    print(f"Extracting data from {file_path}...")
    try:
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Original shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"ERROR: Data file not found at '{file_path}'. Please check the filename.")
        return None
    except ValueError as e:
        print(f"ERROR reading Excel sheet: {e}. Check if the sheet name '{sheet_name}' is correct.")
        return None

def transform_data(df):
    """
    Cleans and transforms the data for loading into the Data Warehouse (DW).
    """
    print("Starting data transformation...")
    
    # 1. Clean Column Names (Standardize to lowercase)
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # 2. Drop rows with missing CustomerID (essential for CustomerDim)
    df.dropna(subset=['customerid'], inplace=True)
    df['customerid'] = df['customerid'].astype(int) # Convert ID to integer

    # 3. Filter out cancelled transactions (InvoiceNo starting with 'C')
    # These are usually represented by negative quantities as well, but this is a good check
    df = df[~df['invoiceno'].astype(str).str.startswith('C')]
    
    # 4. Filter out zero or negative Quantity/UnitPrice (invalid transactions)
    df = df[(df['quantity'] > 0) & (df['unitprice'] > 0)]
    
    # 5. Calculate Total Sales Amount (Key fact measure)
    df['sales_amount'] = df['quantity'] * df['unitprice']
    
    # 6. Time and Product Cleaning
    df.rename(columns={'description': 'product_name'}, inplace=True)
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])
    
    print(f"Transformed shape: {df.shape}")
    return df

def load_data(df, db_name):
    """
    Loads transformed data into the Star Schema tables.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(f"Connected to database '{db_name}'.")

    # --- 1. Load TimeDim ---
    print("Loading TimeDim...")
    time_df = df[['invoicedate']].drop_duplicates().sort_values(by='invoicedate').reset_index(drop=True)
    time_df['date'] = time_df['invoicedate'].dt.date.astype(str)
    time_df['day'] = time_df['invoicedate'].dt.day
    time_df['month'] = time_df['invoicedate'].dt.month
    time_df['quarter'] = time_df['invoicedate'].dt.quarter
    time_df['year'] = time_df['invoicedate'].dt.year
    time_df['is_weekend'] = time_df['invoicedate'].dt.dayofweek.apply(lambda x: 1 if x >= 5 else 0)
    time_df['time_id'] = time_df.index + 1 # Simple sequence ID
    
    time_df[['date', 'day', 'month', 'quarter', 'year', 'is_weekend']].to_sql(
        'TimeDim', conn, if_exists='append', index=False
    )
    # Create a mapping for easy lookup later
    time_map = time_df.set_index('date')['time_id'].to_dict()

    # --- 2. Load CustomerDim ---
    print("Loading CustomerDim...")
    customer_df = df[['customerid', 'country']].drop_duplicates().reset_index(drop=True)
    customer_df.rename(columns={'customerid': 'cust_raw_id'}, inplace=True)
    # Note: Other columns (name, age, etc.) are missing in the source data and are not loaded, 
    # but the schema allows for them if we were to enrich the data later.
    
    customer_df[['cust_raw_id', 'country']].to_sql(
        'CustomerDim', conn, if_exists='append', index=False
    )
    # Create a mapping for easy lookup later
    customer_map = pd.read_sql("SELECT customer_id, cust_raw_id FROM CustomerDim", conn).set_index('cust_raw_id')['customer_id'].to_dict()


    # --- 3. Load ProductDim ---
    print("Loading ProductDim...")
    product_df = df[['stockcode', 'product_name', 'unitprice']].drop_duplicates(subset=['stockcode']).reset_index(drop=True)
    product_df.rename(columns={'unitprice': 'unit_price'}, inplace=True)
    # Placeholder values for Category/Brand not available in the source data
    product_df['category'] = 'Giftware'
    product_df['brand'] = 'N/A'
    
    product_df[['stockcode', 'product_name', 'unit_price', 'category', 'brand']].to_sql(
        'ProductDim', conn, if_exists='append', index=False
    )
    # Create a mapping for easy lookup later
    product_map = pd.read_sql("SELECT product_id, stock_code FROM ProductDim", conn).set_index('stock_code')['product_id'].to_dict()


    # --- 4. Load SalesFact ---
    print("Loading SalesFact...")
    fact_df = df.copy()

    # Map the foreign keys using the generated dimension IDs
    fact_df['time_id'] = fact_df['invoicedate'].dt.date.astype(str).map(time_map)
    fact_df['customer_id'] = fact_df['customerid'].map(customer_map)
    fact_df['product_id'] = fact_df['stockcode'].map(product_map)

    # Select and rename columns for the fact table
    sales_fact_data = fact_df[[
        'invoiceno', 'product_id', 'customer_id', 'time_id', 'quantity', 'unitprice', 'sales_amount', 'country'
    ]]
    sales_fact_data.rename(columns={'invoiceno': 'invoice_no', 'unitprice': 'unit_price'}, inplace=True)

    # Load into the Fact table
    sales_fact_data.to_sql(
        'SalesFact', conn, if_exists='append', index=False
    )
    
    conn.commit()
    conn.close()
    print("ETL process complete! Data loaded into the data warehouse.")


if __name__ == '__main__':
    # 1. Extraction
    raw_data_df = extract_data(DATA_FILE, SHEET_NAME)
    
    if raw_data_df is not None:
        # 2. Transformation
        transformed_df = transform_data(raw_data_df)
        
        # 3. Loading
        load_data(transformed_df, DB_NAME)