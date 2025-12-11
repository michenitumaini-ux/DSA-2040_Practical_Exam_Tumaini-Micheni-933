# Section 1 — Task 1: Data Warehouse Design

##  Star Schema Diagram  
The star schema used in this retail data warehouse is illustrated in the diagram below.  
(Insert your exported image here)

**File:** `diagrams/star_schema_retail.png`

---

##  Dimension and Fact Tables

### **Fact Table: SalesFact**
- sales_id (PK)
- invoice_no  
- product_id (FK → ProductDim)  
- customer_id (FK → CustomerDim)  
- time_id (FK → TimeDim)  
- quantity  
- unit_price  
- sales_amount  
- country  

### **Dimensions**
#### **CustomerDim**
- customer_id (PK)
- cust_raw_id  
- name  
- gender  
- age  
- country  
- city  
- segment  

#### **ProductDim**
- product_id (PK)
- stock_code  
- product_name  
- category  
- brand  
- unit_price  

#### **TimeDim**
- time_id (PK)
- date  
- day  
- month  
- quarter  
- year  
- is_weekend  

---

##  Explanation: Why Star Schema?
I chose a star schema because it simplifies analytical queries and improves performance by keeping dimension tables denormalized and easy to join with the central fact table. This structure works well for OLAP operations such as roll-ups, drill-downs, slicing, and dicing, making it more intuitive and efficient than a snowflake schema.

---

##  SQL Script  
The full SQL `CREATE TABLE` statements for SQLite are included in:

**File:** `sql/schema_create_tables.ipynb`
