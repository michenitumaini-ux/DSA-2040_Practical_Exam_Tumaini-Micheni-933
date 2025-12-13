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

# Section 2: Data Mining  

## Task 1: Data Preprocessing and Exploration (RFM)

##  Goal

The primary goal of this task is to extract, transform, and prepare the customer transactional data from the Data Warehouse (`retail_dw.db`) into meaningful **Recency, Frequency, and Monetary (RFM)** features, which serve as the foundation for customer segmentation (Clustering) and classification.

##  Relevant Files

| Type | File Name | Purpose |
| :--- | :--- | :--- |
| **Script** | `rfm_feature_engineering.py` | Connects to the DW, calculates the raw R, F, M scores. |
| **Output** | `rfm_features.csv` | Intermediate CSV containing the raw RFM features for each customer. |
| **Script** | `rfm_clustering.py` | Handles subsequent data scaling and the exploratory Elbow Method. |

##  Methodology: RFM Feature Engineering (`rfm_feature_engineering.py`)

The script connects to the `retail_dw.db` and calculates the metrics based on a **snapshot date** of **2011-12-10** (the day after the last transaction in the data).

1.  **Recency (R):** Days since the customer's last purchase.
    * *Calculation:* `(Snapshot Date - Max(Transaction Date))`
2.  **Frequency (F):** Total number of unique orders (invoices).
    * *Calculation:* `COUNT(DISTINCT invoice_no)`
3.  **Monetary (M):** Total sales amount spent by the customer.
    * *Calculation:* `SUM(sales_amount)`

### Execution (Feature Generation)

python rfm_feature_engineering.py

## Task 2: Customer Segmentation Using Clustering

This task focuses on segmenting customers using **RFM (Recency, Frequency, Monetary) analysis** and **K-Means clustering**. The objective is to group customers with similar purchasing behavior to support targeted marketing and business decision-making.

---

###  Input Files
- **`rfm_features.csv`**  
  Contains engineered RFM features for each customer:
  - `customer_id`
  - `recency` – days since last purchase
  - `frequency` – number of transactions
  - `monetary` – total amount spent

---

### 📤 Output Files
- **`rfm_scaled_features.csv`**  
  Contains scaled and transformed RFM variables used for clustering:
  - `recency_scaled`
  - `frequency_scaled`
  - `monetary_scaled`

- **`rfm_clusters_with_scores.csv`**  
  Final output containing customer segmentation results:
  - `customer_id`
  - `recency`
  - `frequency`
  - `monetary`
  - `Cluster` – assigned cluster label from K-Means

- **`elbow_method_visualization.png`**  
  Visualization used to help determine the optimal number of clusters (K).

---

###  Methodology

#### 1. Data Loading and Validation
The RFM dataset is loaded from `rfm_features.csv`.  
If the dataset is empty or too small, a dummy dataset is generated to allow the pipeline to continue without failure.

#### 2. Data Preparation
Only the RFM variables (`recency`, `frequency`, `monetary`) are selected for clustering.

To handle skewness commonly present in transactional data:
- A **logarithmic transformation** is applied to all RFM variables.
- Values are clipped to avoid log(0) errors.

#### 3. Feature Scaling
The transformed RFM variables are standardized using **StandardScaler** to ensure that all features contribute equally to the distance calculations used by K-Means.

The scaled features are saved to `rfm_scaled_features.csv`.

#### 4. Determining the Optimal Number of Clusters
The **Elbow Method** is used to evaluate cluster performance for values of K ranging from 1 to 10:
- The **Sum of Squared Errors (SSE)** is computed for each K.
- An elbow plot is generated and saved as `elbow_method_visualization.png`.

For this project, **K = 4** is selected, which is a commonly accepted choice for RFM-based customer segmentation.

#### 5. K-Means Clustering
K-Means clustering is applied using:
- `K = 4`
- A fixed random state for reproducibility

Each customer is assigned to a cluster based on similarity in purchasing behavior.

#### 6. Saving Results
The final clustered dataset is saved as `rfm_clusters_with_scores.csv`, which contains both the original RFM values and the assigned cluster labels.

---

###  Interpretation
The resulting clusters represent distinct customer segments, such as:
- High-value and frequent customers
- Recent but low-spending customers
- Infrequent or inactive customers

These segments can be used for targeted marketing, loyalty programs, and strategic business insights.

---

###  Tools and Libraries Used
- Python
- pandas
- numpy
- scikit-learn
- matplotlib

---

###  Outcome
This task successfully transforms RFM features into meaningful customer segments using unsupervised machine learning, enabling data-driven customer analysis and personalization strategies.


# Task 3: Classification and Association Rule Mining

##  Task 3A: Customer Segment Classification

The goal of this task is to build a predictive model that can classify new or unsegmented customers into one of the established RFM segments (Clusters 0, 1, 2, 3) based on their Recency, Frequency, and Monetary scores. This enables fast, automated targeting.

###  Relevant Files

| Type | File Name | Purpose |
| :--- | :--- | :--- |
| **Input** | `rfm_clusters_with_scores.csv` | The output from clustering, containing RFM features and the assigned `Cluster` labels (target variable). |
| **Script** | `classification.py` | Implementation for training, evaluating, and comparing the two classification models. |
| **Output** | `decision_tree_visualization.png` | Visualization of the trained Decision Tree structure. |

###  Methodology (`classification.py`)

The script loads the clustered RFM data, splits it into training and testing sets (33% test size), and trains two models: a Decision Tree and a K-Nearest Neighbors (KNN) classifier.

1.  **Decision Tree Classifier:** Trained to maximize class purity at each split.
2.  **KNN Classifier:** Trained with $k=1$ (as observed in the code) for direct instance-based prediction.
3.  **Evaluation:** Both models are evaluated on the test set, computing standard metrics (Accuracy, Precision, Recall, F1-Score).

#### Execution (Model Training and Evaluation)
python classification.py


##  Task 3B: Association Rule Mining

The goal of this task is to perform Market Basket Analysis to discover strong item relationships ("co-occurrence") using the Apriori algorithm. These relationships inform merchandising, product bundling, and cross-selling strategies.

###  Relevant Files

| Type | File Name | Purpose |
| :--- | :--- | :--- |
| **Script** | `association_rules.py` | Implementation for finding frequent itemsets and generating rules based on Support, Confidence, and Lift. |
| **Input** | *`synthetic_transactions.csv`* | Assumed file containing transactional data (list of items per invoice) for Apriori input. |

###  Methodology (`association_rules.py`)

The script uses the `mlxtend` library to find rules in the transactional data.

1.  **Data Encoding:** The transactional data is converted into a **One-Hot Encoded DataFrame**, where each column represents an item and each row is a transaction, marking item presence (1) or absence (0).
2.  **Apriori Application:**
    * The Apriori algorithm is applied to efficiently identify **Frequent Itemsets**.
    * **Minimum Support:** $\text{min\_support} = 0.2$ is used to filter out itemsets that occur in less than 20% of all transactions.
3.  **Rule Generation:**
    * Association rules are generated from the frequent itemsets.
    * **Minimum Confidence:** $\text{min\_confidence} = 0.5$ is enforced to ensure high reliability ($P(B|A) \ge 50\%$).
4.  **Reporting:** The resulting rules are sorted by the **Lift** metric, and the **top 5 rules** are displayed in a formatted table.

#### Execution (Rule Generation)
```bash
python association_rules.py

