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

**NOTE:** The commands below use the exact Python executable path that worked successfully on the machine to bypass environment conflicts.

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

**Successful Output Log:**
