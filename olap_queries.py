import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
DB_NAME = 'retail_dw.db'
OUTPUT_IMAGE = 'sales_by_country_visualization.png'

def run_olap_analysis():
    # 1. Connect to the Data Warehouse
    if not os.path.exists(DB_NAME):
        print(f"Error: Database '{DB_NAME}' not found. Please run the ETL script first.")
        return

    conn = sqlite3.connect(DB_NAME)
    print("Connected to Data Warehouse. Running OLAP Queries...")

    # =========================================================================
    # QUERY 1: ROLL-UP (Simulated - Top 10)
    # Goal: Total sales by Country and Quarter
    # =========================================================================
    print("\n--- Query 1: Roll-up Top 10 (Sales by Country and Quarter) ---")
    sql_rollup = """
    SELECT 
        c.country,
        t.year,
        t.quarter,
        SUM(f.sales_amount) as total_sales
    FROM SalesFact f
    JOIN TimeDim t ON f.time_id = t.time_id
    JOIN CustomerDim c ON f.customer_id = c.customer_id
    GROUP BY c.country, t.year, t.quarter
    ORDER BY total_sales DESC
    LIMIT 10;
    """
    df_rollup = pd.read_sql(sql_rollup, conn)
    print(df_rollup.to_markdown(index=False))

    # =========================================================================
    # QUERY 2: DRILL-DOWN (Top 10 monthly sales for United Kingdom)
    # =========================================================================
    print("\n--- Query 2: Drill-down Top 10 (Monthly Sales for United Kingdom) ---")
    sql_drilldown = """
    SELECT 
        t.year,
        t.month,
        SUM(f.sales_amount) as total_sales,
        SUM(f.quantity) as total_quantity
    FROM SalesFact f
    JOIN TimeDim t ON f.time_id = t.time_id
    JOIN CustomerDim c ON f.customer_id = c.customer_id
    WHERE c.country = 'United Kingdom'
    GROUP BY t.year, t.month
    ORDER BY total_sales DESC
    LIMIT 10;
    """
    df_drilldown = pd.read_sql(sql_drilldown, conn)
    print(df_drilldown.to_markdown(index=False))

    # =========================================================================
    # QUERY 3: SLICE (Sales for 'SET' Products by Year - Proxy for Product Category Slice)
    # =========================================================================
    print("\n--- Query 3: Slice (Sales for 'SET' Products by Year) ---")
    sql_slice = """
    SELECT 
        t.year,
        SUM(f.sales_amount) as total_sales
    FROM SalesFact f
    JOIN ProductDim p ON f.product_id = p.product_id
    JOIN TimeDim t ON f.time_id = t.time_id
    WHERE p.product_name LIKE '%SET%'
    GROUP BY t.year
    ORDER BY t.year;
    """
    df_slice = pd.read_sql(sql_slice, conn)
    print(df_slice.to_markdown(index=False))

    # =========================================================================
    # VISUALIZATION
    # Goal: Bar chart of Top 5 Countries by Sales
    # =========================================================================
    print("\n--- Generating Visualization ---")
    
    sql_viz = """
    SELECT c.country, SUM(f.sales_amount) as total_sales
    FROM SalesFact f
    JOIN CustomerDim c ON f.customer_id = c.customer_id
    GROUP BY c.country
    ORDER BY total_sales DESC
    LIMIT 5;
    """
    df_viz = pd.read_sql(sql_viz, conn)

    plt.figure(figsize=(10, 6))
    plt.bar(df_viz['country'], df_viz['total_sales'], color='skyblue')
    plt.title('Top 5 Countries by Total Sales')
    plt.xlabel('Country')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_IMAGE)
    print(f"Visualization saved as '{OUTPUT_IMAGE}'")

    conn.close()

if __name__ == "__main__":
    run_olap_analysis()