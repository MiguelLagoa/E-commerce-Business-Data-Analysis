CREATE OR REPLACE VIEW clean_sales_data AS
SELECT
  CAST("InvoiceNo" AS TEXT) AS invoice_no,
  CAST("StockCode" AS TEXT) AS stock_code,
  LOWER(TRIM("Description")) AS description,
  CAST("Quantity" AS INT) AS quantity,
  TO_DATE("InvoiceDate", 'MM/DD/YYYY') AS invoice_date,
  ROUND("UnitPrice"::numeric, 2) AS unit_price,
  CAST("CustomerID" AS INT) AS customer_id,
  INITCAP(TRIM("Country")) AS country,
  CASE 
    WHEN "Quantity" < 0 THEN 'return'
    WHEN "UnitPrice" < 0 THEN 'adjustment'
    ELSE 'sale'
  END AS transaction_type
FROM raw_data;

