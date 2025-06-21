/* PostgreSQL file that compliments "data_quality_report.md" file. */

/* Total Null values in dataset and column specific null values. */

WITH rows_with_nulls AS (
    SELECT COUNT(*) AS total_rows_with_nulls
    FROM raw_data
     WHERE "InvoiceNo" IS NULL 
         OR "StockCode" IS NULL
         OR "Description" IS NULL
         OR "Quantity" IS NULL
         OR "InvoiceDate" IS NULL
         OR "UnitPrice" IS NULL
         OR "CustomerID" IS NULL
         OR "Country" IS NULL
    )
    SELECT 
    (SELECT total_rows_with_nulls FROM rows_with_nulls) AS total_rows_with_nulls,
    COUNT(*) FILTER (WHERE "InvoiceNo" IS NULL) AS "InvoiceNo_nulls",
    COUNT(*) FILTER (WHERE "StockCode" IS NULL) AS "StockCode_nulls",
    COUNT(*) FILTER (WHERE "Description" IS NULL) AS "Description_nulls",
    COUNT(*) FILTER (WHERE "Quantity" IS NULL) AS "Quantity_nulls",
    COUNT(*) FILTER (WHERE "InvoiceDate" IS NULL) AS "InvoiceDate_nulls",
    COUNT(*) FILTER (WHERE "UnitPrice" IS NULL) AS "UnitPrice_nulls",
    COUNT(*) FILTER (WHERE "CustomerID" IS NULL) AS "CustomerID_nulls",
    COUNT(*) FILTER (WHERE "Country" IS NULL) AS "Country_nulls"
    FROM raw_data;

/* Column Specific Analysis: */

/* "InvoiceDate" */
/* Oldest & Most recent recorded dates */

SELECT 
	MIN("InvoiceDate") AS initial_date,
    MAX("InvoiceDate") AS last_date
FROM raw_data;

/* "Country" */
/* Understanding the possible values in this feature. */

SELECT DISTINCT("Country")
    FROM raw_data;

	


