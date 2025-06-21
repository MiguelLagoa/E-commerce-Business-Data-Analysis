## Data Transformation Report

# 1. Summary

After completing the data quality report, I have confirmed that this dataset is suitable for use in my project. The next step is to apply necessary transformations to the "raw_data" table to maximize analytical potential and improve query accessibility.

For a detailed view of the SQL queries, please refer to: 
    "data_transformation.sql".

All transformations are compiled into a VIEW named "clean_sales_data".

# 2. Transformation Steps

# 2.1. Column Name Standardization

The original column names in raw_data begin with capital letters. In PostgreSQL, this requires using double quotes in every reference, which can be inconvenient. I’ve renamed the columns using snake_case and lowercase for simplicity and consistency.


    Original:                                               Transformed
    2.1.1. InvoiceNo (Text)             |           invoice_no
    2.1.2. StockCode (Text)             |           stock_code
    2.1.3. Description (Text)           |           description
    2.1.4. Quantity (Integer)           |           quantity
    2.1.5. InvoiceDate (String)         |           invoice_date
    2.1.6. UnitPrice (Float)            |           unit_price
    2.1.7. CustomerID (Float)           |           customer_id
    2.1.8. Country (Text)               |           country

# 2.2. Column-Specific Transformations

# 2.2.1. description
Descriptive free-text fields are often inconsistent. I applied "TRIM" to remove extra spaces and "LOWER" to normalize text casing. 

# 2.2.2. invoice_date
Although no inconsistencies were found in the date format during the data quality check, I explicitly converted the values using 'MM/DD/YYYY' to ensure consistent typing, as the original data type was a string.

# 2.2.3. unit_price
To maintain numerical consistency, I applied rounding to 2 decimal places using "ROUND".

# 2.2.4. country
To standardize this field, I used "TRIM" to remove leading/trailing spaces and "INITCAP" to capitalize the first letter of each word.

# 2.3. New Feature

# 2.3.1. transaction_type
As noted in the Data Quality Report, the dataset includes more than just sales—it also contains returns and adjustments. To better support analysis, I engineered a new feature: transaction_type.

I used a CASE statement to assign categories:
    If quantity is less than 0 → 'return'
    If unit_price is less than 0 → 'adjustment'
    Otherwise → 'sale'

This will be useful when doing downstream analytical work.

# 3. Dimensional Modelling (Star Schema)

To support downstream Business Intelligence and dashboarding in Power BI & Tableau, I applied dimensional modelling to transform the cleaned data into fact and dimension tables.

# 3.1. Fact Table

## `fact_sales`
Captures all transactional-level data related to sales events. It includes numerical KPIs and foreign keys to connect with dimension tables.

| Column         | Description                      |
|----------------|----------------------------------|
| invoice_no     | Unique order number              |
| product_id     | FK to dim_product                |
| customer_id    | FK to dim_customer               |
| date           | FK to dim_date                   |
| quantity       | Number of units sold             |
| unit_price     | Price per unit                   |
| total          | Calculated revenue               |
| transaction_type| sale / return / adjustment      |

# 3.2. Dimension Tables

### `dim_customer`
Simplifies customer segmentation and geographic grouping.


### `dim_guest`
Tracks the transactions that were made from guest users.

### `dim_product`
Centralized product catalog table.

### `dim_date`
Supports trend analysis and time-based slicing.
- Year, Month, Day, Weekday, Hour, Minute & Hour and Minute extracted from `invoice_date`

