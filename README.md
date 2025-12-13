# Section 1: Data Warehousing

## Task 1: Data Warehouse Design

### 1. Data Warehouse Schema Design
The data warehouse is designed using a **Star Schema** architecture centered around a sales fact table. This design was chosen to optimize analytical queries common in retail environments.

#### **Star Schema Diagram**
![Star Schema Diagram](Data_warehouse_design/diagrams/star_schema_retail.png)

### 2. Design Explanation
**Why Star Schema over Snowflake?**
I chose a star schema because it simplifies analytical queries and improves performance by keeping dimension tables denormalized. This reduces the complexity of joins required to retrieve data compared to a snowflake schema. This structure is ideal for OLAP operations such as roll-ups, drill-downs, slicing, and dicing, making the data model more intuitive for business intelligence reporting.

### 3. Database Schema Structure
The warehouse consists of one fact table and three dimension tables stored in `retail_dw.db`.

#### **Fact Table**
* **SalesFact**: Stores quantitative sales data.
    * `sales_id` (PK), `invoice_no`
    * Foreign Keys: `product_id`, `customer_id`, `time_id`
    * Measures: `quantity`, `unit_price`, `sales_amount`

#### **Dimension Tables**
* **CustomerDim**: Stores customer details.
    * Attributes: `customer_id` (PK), `cust_raw_id`, `name`, `gender`, `age`, `country`, `city`, `segment`.
* **ProductDim**: Stores product catalog information.
    * Attributes: `product_id` (PK), `stock_code`, `product_name`, `category`, `brand`, `unit_price`.
* **TimeDim**: Stores temporal attributes for analysis.
    * Attributes: `time_id` (PK), `date`, `day`, `month`, `quarter`, `year`, `is_weekend`.

### 4. SQL Implementation
The SQL `CREATE TABLE` statements are implemented in Python using the `sqlite3` library to ensure portability and ease of integration with the ETL pipeline.

**File:** `create_tables.py` (also available in `schema_create_tables.ipynb`)



## **Task 2: ETL Process Implementation**

This task involved creating a modular Python script (`etl_process.py`) to handle the Extraction, Transformation, and Loading of data from the raw source file into the **Star Schema** designed in Task 1.

### **Files and Structure**

| File | Location | Purpose |
| :--- | :--- | :--- |
| `etl_process.py` | `ETL process implementation/` | **Core ETL Script:** Contains all functions for Extract, Transform, and Load. |
| `create_tables.py` | (Moved to a known location) | Creates the empty Star Schema tables in `retail_dw.db`. |
| `Online Retail.xlsx` | `ETL process implementation/` | Source data file. |
| `retail_dw.db` | (Created by `create_tables.py`) | The final SQLite Data Warehouse. |

### **ETL Process Overview**

1.  **Extract:** Reads data from the `'Online Retail'` sheet in `Online Retail.xlsx`.
2.  **Transform:**
    * Cleans data (removes cancelled transactions and rows with missing Customer IDs).
    * Calculates the `sales_amount` (Quantity \* UnitPrice).
    * Generates time attributes (`year`, `quarter`, `month`, `day`) from `InvoiceDate`.
    * Prepares distinct dimension data for loading.
3.  **Load:** Populates the dimension tables (`TimeDim`, `CustomerDim`, `ProductDim`) first, generating surrogate keys. It then uses these keys to populate the central `SalesFact` table, ensuring data integrity and star schema adherence.

### **Execution Instructions**

The script must be run by first deleting and recreating the database to ensure a clean schema, and then running the ETL script from its correct folder.

1.  **Clean and Re-Create Database:**
    *(This assumes `create_tables.py` is in the `Data warehouse design` folder)*
    ```bash
    cd Data\ warehouse\ design
    rm -f retail_dw.db
    /c/Users/USER/AppData/Local/Microsoft/WindowsApps/python3.13.exe create_tables.py
    ```

2.  **Run ETL Script:**
    *(This assumes the terminal is returned to the project root)*
    ```bash
    cd ..
    cd ETL\ process\ implementation
    /c/Users/USER/AppData/Local/Microsoft/WindowsApps/python3.13.exe etl_process.py
    ```
## **Task 3: OLAP Queries and Analysis**
Overview

This task focuses on performing OLAP (Online Analytical Processing) queries on a retail Data Warehouse implemented using a star schema in SQLite. The objective is to analyze sales data across multiple dimensions such as time, customer location, and product information in order to support business decision-making.

The analysis demonstrates core OLAP operations including roll-up, drill-down, and slice, as well as basic data visualization.

Data Warehouse Structure

The Data Warehouse follows a star schema design and consists of the following tables:

Dimension Tables

CustomerDim: Stores customer demographic and geographic details
(e.g., name, gender, age, country, city, segment)

ProductDim: Stores product-related information
(e.g., stock code, product name, category, brand, unit price)

TimeDim: Stores time-based attributes
(e.g., date, day, month, quarter, year, weekend indicator)

Fact Table

SalesFact: Stores transactional sales data
(e.g., invoice number, quantity, unit price, sales amount)
and links to all dimension tables using foreign keys.

Tools and Technologies Used

Python

SQLite (Data Warehouse storage)

Pandas (data querying and analysis)

Matplotlib (data visualization)

Files Included
File Name	Description
create_tables.py	Creates the Data Warehouse schema (fact and dimension tables)
olap_queries.py	Executes OLAP queries and generates analysis outputs
retail_dw.db	SQLite database containing the Data Warehouse
sales_by_country_visualization.png	Output visualization generated from OLAP analysis
OLAP Queries Performed
1. Roll-Up Analysis

Objective:
To analyze total sales aggregated by country and quarter.

Description:
This query groups sales data by country, year, and quarter, allowing analysis at a higher level of time granularity. The results are ordered by total sales and limited to the top 10 highest-performing combinations.

OLAP Operation Used:

Roll-up (from detailed transactions to quarterly summaries)

2. Drill-Down Analysis

Objective:
To examine monthly sales performance for the United Kingdom.

Description:
This query focuses on a single country and breaks down sales from a higher level into monthly totals, including both sales revenue and quantity sold. The top 10 months by sales value are displayed.

OLAP Operation Used:

Drill-down (from country-level data to month-level detail)

3. Slice Analysis

Objective:
To analyze sales trends for a specific subset of products over time.

Description:
This query filters the dataset to include only products whose names contain the keyword “SET”, serving as a proxy for a product category. Sales are then aggregated by year to observe performance trends.

OLAP Operation Used:

Slice (filtering the cube on a specific product condition)

Visualization

Objective:
To visually compare sales performance across different countries.

Description:
A bar chart is generated showing the top 5 countries by total sales. This visualization helps identify the most profitable markets at a glance.

X-axis: Country

Y-axis: Total Sales

Output file: sales_by_country_visualization.png

How to Run the Analysis

Create the Data Warehouse tables

python create_tables.py


Run the OLAP queries and generate analysis

python olap_queries.py


View Results

Query outputs are displayed in the terminal in tabular format

Visualization is saved as an image file in the project directory

Key Insights

OLAP operations enable efficient multi-dimensional analysis of large datasets.

Roll-up, drill-down, and slice operations provide flexibility in analyzing data at different levels of detail.

Visualizations complement OLAP queries by improving interpretability and supporting strategic decision-making.

Conclusion

Task 3 successfully demonstrates the use of OLAP techniques on a retail Data Warehouse. By combining structured SQL queries, Python-based analysis, and visualization, the task highlights how analytical processing can transform raw transactional data into meaningful business insights.


