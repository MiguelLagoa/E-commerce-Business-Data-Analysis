/* Create a table with normalized columns and values */

CREATE OR REPLACE VIEW clean_sales_data AS
SELECT
  CAST("InvoiceNo" AS TEXT) AS invoice_no,
  CAST("StockCode" AS TEXT) AS product_id,
  LOWER(TRIM("Description")) AS description,
  CAST("Quantity" AS INT) AS quantity,
  "InvoiceDate" AS invoice_date,
  ROUND("UnitPrice"::numeric, 2) AS unit_price,
  CAST("CustomerID" AS INT) AS customer_id,
  INITCAP(TRIM("Country")) AS country,
  CASE 
    WHEN "Quantity" < 0 THEN 'return'
    WHEN "UnitPrice" < 0 THEN 'adjustment'
    ELSE 'sale'
  END AS transaction_type
FROM raw_data;

/* Dimensional Modelling */

/* Dimensions: */

/* Customer Dimension */

DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer AS
SELECT DISTINCT ON (customer_id)
    customer_id,
    country
FROM clean_sales_data
WHERE customer_id IS NOT NULL
ORDER BY customer_id;

/* Guest Checkout Dimension */

DROP TABLE IF EXISTS dim_guest;
CREATE TABLE dim_guest AS
SELECT DISTINCT
    ROW_NUMBER() OVER () + 100000 AS guest_id,
    invoice_no,
    country,
    MIN(invoice_date) AS first_purchase_date
FROM clean_sales_data
WHERE customer_id IS NULL
GROUP BY invoice_no, country;


/* Product Dimension */

DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product AS
SELECT DISTINCT
  	product_id,
  	description
FROM clean_sales_data;

/* Date Dimension */

DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date AS
SELECT DISTINCT
	invoice_date::date AS date,  
	EXTRACT(YEAR FROM invoice_date) AS year,
	EXTRACT(MONTH FROM invoice_date) AS month,
	EXTRACT(DAY FROM invoice_date) AS day,
	TRIM(TO_CHAR(invoice_date, 'Day')) AS weekday,
	EXTRACT(HOUR FROM invoice_date) AS hour,  
	EXTRACT(MINUTE FROM invoice_date) AS minute,
  	TO_CHAR(invoice_date, 'HH24:MI') AS hour_minute 
FROM clean_sales_data;


/* Fact Table (fact_sales) for PowerBI/ Tableau reporting */

DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales AS
SELECT
  cs.invoice_no,
  cs.product_id,
  CASE
    WHEN cs.customer_id IS NOT NULL THEN cs.customer_id
    ELSE (ROW_NUMBER() OVER (PARTITION BY cs.invoice_no ORDER BY cs.invoice_date) + 200000) -- Unique ID per guest invoice
  END AS user_id,
  CASE
    WHEN cs.customer_id IS NULL THEN 'guest'
    ELSE 'registered'
  END AS user_type,
  cs.invoice_date,
  cs.quantity,
  cs.unit_price,
  ROUND(cs.quantity * cs.unit_price, 2) AS total,
  cs.transaction_type
FROM clean_sales_data cs
WHERE unit_price >= 0;

/* I will also create a table to have all features available when performing deeper analysis in Python */

DROP TABLE IF EXISTS eda_sales_data;
CREATE TABLE eda_sales_data AS
SELECT
  invoice_no,
  product_id,
  description,
  quantity,
  invoice_date,
  unit_price,
  customer_id,
  country,
  transaction_type,
  ROUND(quantity * unit_price, 2) AS total
FROM clean_sales_data;




