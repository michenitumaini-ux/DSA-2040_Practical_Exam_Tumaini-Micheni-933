# Section 1: Data Warehousing

## Task 1: Data Warehouse Design

### 1. Data Warehouse Schema Design
The data warehouse is designed using a **Star Schema** architecture centered around a sales fact table. This design was chosen to optimize analytical queries common in retail environments.

#### **Star Schema Diagram**
![Star Schema Diagram](diagrams/star_schema_retail.png)

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
