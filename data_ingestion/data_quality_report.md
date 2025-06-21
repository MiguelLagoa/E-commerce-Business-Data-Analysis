## Data Quality Report

# 1. Summary 

This report documents the quality checks applied during the ingestion of "data.csv" into a cloud-hosted PostgreSQL database. For this I am using pgAdmin4 to run the queries and I am hosting the data into AWS RDS.

This initial verification of data quality is just meant to understand if there are any major obstacles to move the project further.

The first step taken was to load the "data.csv" file into pgAdmin4 (or is it AWS RDS ? where does my file currently sit? I believe its in AWS RDS but i am accessing it through pgAdmin4 -- please confirm). This was done using "data loading.py" which after uploading it to AWS was renamed to "raw_data"

# 2. Dataset Characteristics

    2.1. Columns:
        2.1.1. InvoiceNo (Text)
        2.1.2. StockCode (Text)
        2.1.3. Description (Text)
        2.1.4. Quantity (Integer)
        2.1.5. InvoiceDate (String)
        2.1.6. UnitPrice (Float)
        2.1.7. CustomerID (Float)
        .1.8. Country (Text)


## 3. Data Quality Checks: 

# 3.1. Null Values 

First I will check if there are any missing values in my dataset:

* PostgreSQL Query*

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


Results:
"total_rows_with_nulls"  135080

"Description_nulls"  1454

"CustomerID_nulls"  135080


This query shows a total of 135080 NA (approximately 25% of the dataset).


# 3.2. Quality of column specific results:

#   3.2.1.    "Quantity"

This feature also comprises negative quantity entries from the dataset.

    SELECT COUNT(*) AS negative_qty_entries
    FROM raw_data 
    WHERE "Quantity" < 0;

"negative_qty_entries"
10624

The majority of these negative values refer to returns made by customers. 
There are also negative values referring to "POSTAGE", "AMAZON FEE", "Bank Charges", "CRUK Commission", and so on. This initial grasp of the dataset is helpful as later I will use Python to examine the dataset with more depth. 

#   3.2.2.    "Country"

To investigate all the possible countries present in the dataset: 

* PostgreSQL Query*

    SELECT DISTINCT("Country")
    FROM raw_data;

Considering that this columns refers to countries, there are a few entries which are incorrect or have unusual description such as: 
European Community; EIRE; Channel Islands; Hong Kong.
Nonetheless, this does not affect the integrity of the database enough to render it useless.

#   3.2.3.    "InvoiceDate"

First I will understand the timeframe of dataset using this query:

* PostgreSQL Query*
    SELECT 
        MIN("InvoiceDate") AS initial_date,
        MAX("InvoiceDate") AS last_date
    FROM raw_data;

Now I know that the oldest recorded date in my dataset is 01/12/2010 08:26 and the newer recorded date is 09/12/2011 12:50.
This reassures the validity of the timestamps, allowing me to proceed.  
