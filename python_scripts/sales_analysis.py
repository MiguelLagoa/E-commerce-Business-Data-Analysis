import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style for better visualization
plt.style.use('ggplot')
sns.set_palette('husl')

# Set pandas display options to show normal numbers
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the data
df = pd.read_csv('eda_data.csv', on_bad_lines='skip')
print(f"Dataset Shape: {df.shape}")

# Create customer/guest classification
df['user_type'] = np.where(df['customer_id'].notna(), 'customer', 'guest')

#####################
# 1. Initial Data Overview
print("\n1. Initial Data Overview")
print("=" * 50)
print(f"Dataset Shape: {df.shape}")
print("\nColumns in the dataset:")
print(df.columns)
print("\nBasic Statistics for Numerical Columns:")
pd.set_option('display.float_format', '{:.2f}'.format)
print(df[["quantity","unit_price","total"]].describe())

# Define keyword sets outside the function for better performance
DAMAGED_KEYWORDS = {'wet', 'crushed', 'damages?', 'damages/', 'damages', 'damaged', 'dagamed',
                    'breakages', 'broken', 'smashed', 'damage', 'mould', 'mouldy', 'cracked', 'faulty'}
ADJUSTMENT_KEYWORDS = {'adjust', 'dotcom', 'postage', 'discount', 'amazon fee', 'amazon adjust', 
                      'amazon sold sets', 'bank charges', 're-adjustment', 'adjustment', 'sale error', 
                      'incorrectly credited c550456 see 47', 'did a credit and did not tick ret'}
MISSING_KEYWORDS = {'lost', '?', 'missing', 'mia', 'find', 'not rcvd', 'check?', 'check'}
WRONG_PRODUCT_ID_KEYWORDS = {'wrong', 'barcode problem', 'sold as 22467', 'wrongly', 'coded', 
                            'came coded as 20713', 'incorrect stock entry', 'marked as 23343', 
                            'mixed up', 'mix up', '20713', 'mix up with c'}
BINNED_KEYWORDS = {'thrown away', 'throw away', 'unsaleable', 'given away', 'had been put aside'}
COMMISSION_KEYWORDS = {'cruk commission', 'commission'}
INVENTORY_ADJUSTMENT_KEYWORDS = {'found', 'returned', 'counted', 'michel oops', 're dotcom quick fix', 
                                "dotcom sold in 6's", 'stock check', 'sold as set/6 by dotcom', 
                                'on cargo order', 'mailout', 'sold as set on dotcom',
                                'sold as set on dotcom and amazon', 'sold as set by dotcom',
                                'add stock to allocate online orders', 'allocate stock for dotcom orders ta',
                                'dotcomstock', 'found in w/hse'}
SAMPLES_KEYWORDS = {'sample', 'display', 'showroom', 'samples', 'test', '?display?'}

# Define exceptions as sets
DAMAGED_EXCEPTIONS = {'cracked glaze','set of 4 pantry jelly moulds', 'baking mould', 'jungle popsicles ice lolly moulds'}
ADJUSTMENT_EXCEPTIONS = {'mug , dotcomgiftshop.com'}
MISSING_EXCEPTIONS = {'bohemian collage stationery set', 'sunset check hammock', 
                     'brown check cat doorstop', 'pair padded hangers pink check'}
SAMPLES_EXCEPTIONS = {'crystal stud earrings clear display', 'robot mug in display box'}

def replace_description(x):
    if not isinstance(x, str):
        return x
        
    # Normalize text: lowercase and remove extra spaces
    x_norm = ' '.join(x.lower().strip().split())
    
    # Check exceptions first
    if any(exc in x_norm for exc in DAMAGED_EXCEPTIONS):
        return x
        
    # Check for damaged items
    if ('cracked' in x_norm or 'mould' in x_norm or 
        any(keyword in x_norm for keyword in DAMAGED_KEYWORDS)):
        return 'damaged'
    
    # Check adjustment exceptions
    if any(exc in x_norm for exc in ADJUSTMENT_EXCEPTIONS):
        return x
        
    # Check other categories
    if any(keyword in x_norm for keyword in ADJUSTMENT_KEYWORDS):
        return 'adjustments'
        
    # Check missing exceptions
    if any(exc in x_norm for exc in MISSING_EXCEPTIONS):
        return x
        
    # Check remaining categories
    if any(keyword in x_norm for keyword in MISSING_KEYWORDS):
        return 'missing'
    if any(keyword in x_norm for keyword in WRONG_PRODUCT_ID_KEYWORDS):
        return 'wrong product id'
    if any(keyword in x_norm for keyword in BINNED_KEYWORDS):
        return 'binned items'
    if any(keyword in x_norm for keyword in COMMISSION_KEYWORDS):
        return 'commissions'
    if any(keyword in x_norm for keyword in INVENTORY_ADJUSTMENT_KEYWORDS):
        return 'inventory adjustments'
        
    # Check samples exceptions and keywords
    if any(exc in x_norm for exc in SAMPLES_EXCEPTIONS):
        return x
    if any(keyword in x_norm for keyword in SAMPLES_KEYWORDS):
        return 'samples'
        
    return x

#Since I had to manually search and apply labelling to my results I want to save the original descriptions 
# to validate if no mistake was made during this groupping process
#  
original_descriptions = df['description'].copy()

#Replacing my new descriptions with the old ones
df['description'] = df['description'].apply(replace_description)


#Cross checking between old vs new descriptions
changed_rows = pd.DataFrame({
    'original_description': original_descriptions,
    'new_description': df['description']
})

changed_rows = changed_rows[
    (changed_rows['original_description'].notna()) & 
    (changed_rows['new_description'].notna()) & 
    (changed_rows['original_description'] != changed_rows['new_description'])
]

print(changed_rows)

# Export the modified DataFrame to a new CSV file
df.to_csv('modified_eda_data.csv', index=False)




############################         ABOVE DONE


total_sales = sales_df['total']

plt.figure(figsize=(12, 6))
n, bins, patches = plt.hist(total_sales, bins=50, color='skyblue', edgecolor='black')
plt.yscale('log')
plt.title('Histogram of Total Sale Amounts')
plt.xlabel('Total Sale Amount (£)')
plt.ylabel('Frequency (Log)')
plt.tight_layout()
plt.show()




# Box plot of total sales
plt.figure(figsize=(8, 6))
sns.boxplot(x=total_sales)
plt.title('Box Plot of Total Sale Amounts')
plt.xlabel('Total Sale Amount (£)')
plt.xscale('log')  # Log scale for better visualization
plt.tight_layout()
plt.show()

# Filter total sales for the range 0-50
total_sales_0_50 = total_sales[(total_sales >= 0) & (total_sales <= 50)]

plt.figure(figsize=(8, 6))
sns.boxplot(x=total_sales_0_50)
plt.title('Box Plot of Total Sale Amounts (£0–50)')
plt.xlabel('Total Sale Amount (£)')
plt.tight_layout()
plt.show()



# Plot histogram of total returns
plt.figure(figsize=(12, 6))

# Filter returns and remove outliers
total_returns = abs(df[df['transaction_type'] == 'return']['total'])
# Remove top 3 outliers
outliers = total_returns.nlargest(3)
total_returns_filtered = total_returns[~total_returns.isin(outliers)]

# Create histogram with log scale on y-axis only
n, bins, patches = plt.hist(total_returns_filtered, bins=50, color='lightcoral', edgecolor='black')
plt.yscale('log')  # Set y-axis to log scale

plt.title('Distribution of Total Returns Amount (Excluding Top 3 Outliers)')
plt.xlabel('Total Returns Amount')
plt.ylabel('Frequency (Log Scale)')
plt.tight_layout()
plt.show()


# Create box plot for returns
plt.figure(figsize=(10, 6))
sns.boxplot(x=total_returns_filtered)
plt.title('Box Plot of Total Returns Amount (Excluding Top 3 Outliers)')
plt.xlabel('Total Returns Amount')
plt.tight_layout()
plt.show()

# Create violin plot for returns
plt.figure(figsize=(10, 6))
sns.violinplot(x=total_returns_filtered)
plt.title('Violin Plot of Total Returns Amount (Excluding Top 3 Outliers)')
plt.xlabel('Total Returns Amount')
plt.tight_layout()
plt.show()

############################         DONE



######################
# 2. Data Quality Analysis
print("\n2. Data Quality Analysis")
print("=" * 50)
print("\nData Types:")
print(df.dtypes)
######################


# 3. Transaction Analysis
print("\n3. Transaction Analysis")
print("=" * 50)
print("Transaction Types Distribution:")
print(df['transaction_type'].value_counts())




######################

# Plot transaction types
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='transaction_type')
plt.title('Distribution of Transaction Types')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 4. Temporal Analysis
print("\n4. Temporal Analysis")
print("=" * 50)
df['invoice_date'] = pd.to_datetime(df['invoice_date'])
print("Date Range of Transactions:")
print(f"Start Date: {df['invoice_date'].min()}")
print(f"End Date: {df['invoice_date'].max()}")

# Plot monthly sales
df['month'] = df['invoice_date'].dt.to_period('M')
monthly_sales = df.groupby('month')['total'].sum()

plt.figure(figsize=(15, 8))
plt.plot(range(len(monthly_sales)), monthly_sales.values, marker='o', linestyle='-', linewidth=2, markersize=8)

# Add value labels on top of points with better positioning
for i, value in enumerate(monthly_sales.values):
    plt.text(i, value * 1.05, f'${value:,.0f}', ha='center', va='bottom', 
             fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Format x-axis labels as "Month (Year)"
x_labels = [f"{x.strftime('%B')} ({x.strftime('%Y')})" for x in monthly_sales.index]

plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(range(len(monthly_sales)), x_labels, rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 5. Product Analysis
print("\n5. Product Analysis")
print("=" * 50)
print(f"Number of Unique Products: {df['product_id'].nunique()}")
print("\nTop 10 Products by Total Sales:")
top_products = df.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(10)
print(top_products)

# Plot top products
plt.figure(figsize=(12, 6))
top_products.plot(kind='bar')
plt.title('Top 10 Products by Quantity Sold')
plt.xlabel('Product ID')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Customer vs Guest Analysis
print("\n6. Customer vs Guest Analysis")
print("=" * 50)
print("User Type Distribution:")
user_type_counts = df['user_type'].value_counts()
print(user_type_counts)

# Plot user type distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='user_type')
plt.title('Distribution of User Types')
plt.xlabel('User Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Compare spending patterns
print("\nAverage Spending by User Type:")
print(df.groupby('user_type')['total'].agg(['mean', 'sum']))

# Plot spending comparison
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='user_type', y='total')
plt.title('Spending Distribution by User Type')
plt.xlabel('User Type')
plt.ylabel('Total Spending')
plt.yscale('log')  # Using log scale for better visualization
plt.tight_layout()
plt.show()

# 7. Country Analysis
print("\n7. Country Analysis")
print("=" * 50)
print("Top 10 Countries by Number of Transactions:")
country_counts = df['country'].value_counts().head(10)
print(country_counts)

# Plot country distribution
plt.figure(figsize=(12, 6))
country_counts.plot(kind='bar')
plt.title('Top 10 Countries by Number of Transactions')
plt.xlabel('Country')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 8. Product Description Analysis
print("\n8. Product Description Analysis")
print("=" * 50)
print("Top 10 Most Common Product Descriptions:")
top_descriptions = df['description'].value_counts().head(10)
print(top_descriptions)

# Plot top descriptions
plt.figure(figsize=(12, 6))
top_descriptions.plot(kind='bar')
plt.title('Top 10 Most Common Product Descriptions')
plt.xlabel('Product Description')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 9. Price and Quantity Analysis
print("\n9. Price and Quantity Analysis")
print("=" * 50)
print("Price Distribution Statistics:")
print(df['unit_price'].describe())
print("\nQuantity Distribution Statistics:")
print(df['quantity'].describe())

# Plot price distribution
plt.figure(figsize=(12, 6))
# Define custom bins for price ranges
price_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, float('inf')]
price_labels = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-20', '20+']

# Create price ranges and count products in each range
df['price_range'] = pd.cut(df['unit_price'], bins=price_bins, labels=price_labels)
price_counts = df['price_range'].value_counts().sort_index()

# Create bar plot
plt.bar(price_counts.index, price_counts.values)
plt.title('Distribution of Unit Prices')
plt.xlabel('Unit Price Range')
plt.ylabel('Number of Products')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Plot quantity distribution
plt.figure(figsize=(12, 6))

# Filter for sales only and get the quantity distribution
sales_quantities = df[df['transaction_type'] == 'sale']['quantity'].value_counts().sort_index()

# Print the distribution
print("\nQuantity Distribution (Sales Only):")
print(sales_quantities)

# Create bar plot for quantities up to 50 (most common range)
common_quantities = sales_quantities[sales_quantities.index <= 50]
plt.bar(common_quantities.index, common_quantities.values)
plt.title('Distribution of Quantities per Sale (Up to 50 items)')
plt.xlabel('Quantity')
plt.ylabel('Number of Sales')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Print summary statistics
print("\nSummary of quantities:")
print(f"Most common quantity: {sales_quantities.index[0]} items ({sales_quantities.iloc[0]} sales)")
print(f"Total number of sales: {sales_quantities.sum()}")
print(f"Number of unique quantities: {len(sales_quantities)}")

######################
# Returns Analysis
print("\nReturns Analysis")
print("=" * 50)

# Filter for returns
returns_df = df[df['transaction_type'] == 'return']

# 1. Basic Returns Statistics
print("\n1. Basic Returns Statistics:")
print(f"Total number of returns: {len(returns_df)}")
print(f"Total value of returns: ${returns_df['total'].sum():,.2f}")
print(f"Average return value: ${returns_df['total'].mean():,.2f}")
print(f"Median return value: ${returns_df['total'].median():,.2f}")

# 2. Returns by Quantity
plt.figure(figsize=(12, 6))

# Debug prints
print("\nDebug Information:")
print(f"Total rows in dataset: {len(df)}")
print(f"Unique transaction types: {df['transaction_type'].unique()}")
print(f"Number of returns: {len(returns_df)}")
print("\nSample of returns data:")
print(returns_df[['quantity', 'total']].head())

# Define custom bins for return quantities
quantity_bins = [0, 1, 2, 3, 4, 5, 10, 20, 50, float('inf')]
quantity_labels = ['1', '2', '3', '4', '5', '6-10', '11-20', '21-50', '50+']

# Create quantity ranges and count returns in each range using absolute values
returns_df['quantity_range'] = pd.cut(abs(returns_df['quantity']), bins=quantity_bins, labels=quantity_labels)
quantity_counts = returns_df['quantity_range'].value_counts().sort_index()

# Debug print the quantity counts
print("\nQuantity distribution before plotting:")
print(quantity_counts)

# Create bar plot
plt.bar(range(len(quantity_counts)), quantity_counts.values)
plt.title('Distribution of Return Quantities')
plt.xlabel('Quantity Range')
plt.ylabel('Number of Returns')
plt.xticks(range(len(quantity_counts)), quantity_counts.index, rotation=0)
plt.tight_layout()
plt.show()

# Print summary statistics
print("\nReturns Quantity Distribution:")
print(quantity_counts)
print(f"\nTotal number of returns: {quantity_counts.sum()}")
print(f"Number of unique quantity ranges: {len(quantity_counts)}")


# 3. Returns Over Time
plt.figure(figsize=(15, 8))

# Filter for returns and calculate monthly totals
returns_df = df[df['transaction_type'] == 'return'].copy()
returns_df['invoice_date'] = pd.to_datetime(returns_df['invoice_date'])
returns_df['month'] = returns_df['invoice_date'].dt.to_period('M')
monthly_returns = returns_df.groupby('month')['total'].sum()



plt.plot(range(len(monthly_returns)), monthly_returns.values, marker='o', linestyle='-', linewidth=2, markersize=8)

# Add value labels on top of points with better positioning
for i, value in enumerate(monthly_returns.values):
    plt.text(i, value * 1.05, f'${value:,.0f}', ha='center', va='bottom', 
             fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Format x-axis labels as "Month (Year)"
x_labels = [f"{x.strftime('%B')} ({x.strftime('%Y')})" for x in monthly_returns.index]

plt.title('Monthly Returns Value Trend')
plt.xlabel('Month')
plt.ylabel('Total Returns Value ($)')
plt.xticks(range(len(monthly_returns)), x_labels, rotation=0)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 4. Returns by Country
plt.figure(figsize=(12, 6))
country_returns = returns_df.groupby('country')['total'].sum().sort_values(ascending=False).head(10)
plt.bar(country_returns.index, country_returns.values)
plt.title('Top 10 Countries by Returns Value')
plt.xlabel('Country')
plt.ylabel('Total Returns Value')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 5. Returns Value Distribution
plt.figure(figsize=(12, 6))

# Filter returns and remove outliers
total_returns = abs(df[df['transaction_type'] == 'return']['total'])  # Using absolute values
# Remove top 3 outliers
outliers = total_returns.nlargest(3)
total_returns_filtered = total_returns[~total_returns.isin(outliers)]

# Apply log transformation
log_total_returns = np.log1p(total_returns_filtered)

# Create histogram
n, bins, patches = plt.hist(log_total_returns, bins=50, weights=total_returns_filtered, color='skyblue', edgecolor='black')

# Define and set custom tick labels
log_ticks = np.arange(0, np.ceil(log_total_returns.max()), 1)
actual_ticks = np.expm1(log_ticks)
plt.xticks(log_ticks, [f'{x:,.0f}' for x in actual_ticks])

plt.title('Distribution of Total Returns Amount (Excluding Top 3 Outliers)')
plt.xlabel('Total Returns Amount')
plt.ylabel('Total Returns Value')
plt.tight_layout()
plt.show()

# 6. Returns by Customer Type
plt.figure(figsize=(10, 6))
customer_returns = returns_df.groupby('user_type')['total'].agg(['sum', 'count'])
# Convert sum to absolute values
customer_returns['sum'] = customer_returns['sum'].abs()
print("\nReturns by Customer Type:")
print(customer_returns)

plt.bar(customer_returns.index, customer_returns['sum'])
plt.title('Total Returns Value by Customer Type')
plt.xlabel('Customer Type')
plt.ylabel('Total Returns Value')
plt.tight_layout()
plt.show()

# 7. Most Returned Products
plt.figure(figsize=(12, 6))
top_returned = returns_df.groupby('description')['quantity'].sum().abs().sort_values(ascending=False).head(10)
plt.bar(top_returned.index, top_returned.values)
plt.title('Top 10 Most Returned Products')
plt.xlabel('Product Description')
plt.ylabel('Total Quantity Returned')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 8. Return Rate Analysis
total_sales = len(df[df['transaction_type'] == 'sale'])
total_returns = len(returns_df)
return_rate = (total_returns / total_sales) * 100
print(f"\nOverall Return Rate: {return_rate:.2f}%")

# 9. Returns Value by Product Category
plt.figure(figsize=(12, 6))
category_returns = returns_df.groupby('description')['total'].sum().sort_values(ascending=False).head(10)
plt.bar(category_returns.index, category_returns.values)
plt.title('Top 10 Product Categories by Returns Value')
plt.xlabel('Product Category')
plt.ylabel('Total Returns Value')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 10. Returns Summary Statistics
print("\nReturns Summary Statistics:")
print(returns_df[['quantity', 'unit_price', 'total']].describe())

######################

# Key Findings:

# 1. Data Quality: Analysis of missing values and data types across all columns.

# 2. Transaction Patterns: Distribution of different transaction types and their frequencies.

# 3. Temporal Trends: Monthly sales patterns and seasonality in the data.

# 4. Product Performance: Top performing products and their sales volumes.

# 5. Customer Behavior: Comparison between registered customers and guest users.

# 6. Geographic Distribution: Sales distribution across different countries.

# 7. Product Categories: Most common product descriptions and their popularity.

# 8. Pricing Strategy: Distribution of unit prices and their impact on sales.

# Recommendations:

# 1. Focus on top-performing products and consider expanding their inventory.
# 2. Implement strategies to convert guest users to registered customers.
# 3. Analyze seasonal patterns to optimize inventory management.
# 4. Consider geographic expansion based on country performance.
# 5. Review pricing strategy based on price distribution analysis.
# 6. Investigate any unusual patterns in transaction types or quantities.
# 7. Use product description analysis to identify popular product categories.
# 8. Develop targeted marketing strategies for different user types.

######################
# Advanced Analysis
print("\nAdvanced Analysis")
print("=" * 50)

# 1. Detailed Customer Type Analysis
print("\n1. Detailed Customer Type Analysis")
print("=" * 50)

# Calculate metrics for customers and guests
customer_metrics = df[df['user_type'] == 'customer']
guest_metrics = df[df['user_type'] == 'guest']

# Calculate sales and returns for each user type
customer_sales = len(customer_metrics[customer_metrics['transaction_type'] == 'sale'])
customer_returns = len(customer_metrics[customer_metrics['transaction_type'] == 'return'])
customer_return_rate = (customer_returns / customer_sales * 100) if customer_sales > 0 else 0

guest_sales = len(guest_metrics[guest_metrics['transaction_type'] == 'sale'])
guest_returns = len(guest_metrics[guest_metrics['transaction_type'] == 'return'])
guest_return_rate = (guest_returns / guest_sales * 100) if guest_sales > 0 else 0

# Print results
print("\nCustomer Analysis:")
print(f"Total Sales: {customer_sales}")
print(f"Total Returns: {customer_returns}")
print(f"Return Rate: {customer_return_rate:.2f}%")

print("\nGuest Analysis:")
print(f"Total Sales: {guest_sales}")
print(f"Total Returns: {guest_returns}")
print(f"Return Rate: {guest_return_rate:.2f}%")

# Visualize customer vs guest metrics
plt.figure(figsize=(15, 10))

# Create subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Sales comparison
sales_data = [customer_sales, guest_sales]
ax1.bar(['Customers', 'Guests'], sales_data)
ax1.set_title('Total Sales by User Type')
ax1.set_ylabel('Number of Sales')

# Returns comparison
returns_data = [customer_returns, guest_returns]
ax2.bar(['Customers', 'Guests'], returns_data)
ax2.set_title('Total Returns by User Type')
ax2.set_ylabel('Number of Returns')

# Return rate comparison
return_rates = [customer_return_rate, guest_return_rate]
ax3.bar(['Customers', 'Guests'], return_rates)
ax3.set_title('Return Rate by User Type')
ax3.set_ylabel('Return Rate (%)')

# Box plot of transaction values
sns.boxplot(data=df, x='user_type', y='total', ax=ax4)
ax4.set_title('Transaction Value Distribution by User Type')
ax4.set_ylabel('Transaction Value')
ax4.set_yscale('log')

plt.tight_layout()
plt.show()

# 2. Type of Movements Analysis
print("\n2. Type of Movements Analysis")
print("=" * 50)

# Calculate total sales and returns by country
sales_by_country = df[df['transaction_type'] == 'sale'].groupby('country')['total'].sum().sort_values(ascending=False)
returns_by_country = df[df['transaction_type'] == 'return'].groupby('country')['total'].sum().sort_values(ascending=False)

# Print top 10 countries for sales and returns
print("\nTop 10 Countries by Sales:")
print(sales_by_country.head(10))
print("\nTop 10 Countries by Returns:")
print(returns_by_country.head(10))

# Visualize sales and returns by country
plt.figure(figsize=(15, 10))

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Sales by country
sales_by_country.head(10).plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Countries by Sales')
ax1.set_ylabel('Total Sales Value')
ax1.tick_params(axis='x', rotation=45)

# Returns by country
returns_by_country.head(10).plot(kind='bar', ax=ax2)
ax2.set_title('Top 10 Countries by Returns')
ax2.set_ylabel('Total Returns Value')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 3. Invoice Analysis
print("\n3. Invoice Analysis")
print("=" * 50)

# Calculate unique invoices
unique_invoices = df['invoice_no'].nunique()
print(f"Total Unique Invoices: {unique_invoices}")

# Calculate average items per invoice
sales_per_invoice = df[df['transaction_type'] == 'sale'].groupby('invoice_no').size().mean()
returns_per_invoice = df[df['transaction_type'] == 'return'].groupby('invoice_no').size().mean()

print(f"Average Items per Sales Invoice: {sales_per_invoice:.2f}")
print(f"Average Items per Returns Invoice: {returns_per_invoice:.2f}")

# Calculate average invoices per customer
customer_invoices = df[df['user_type'] == 'customer'].groupby('customer_id')['invoice_no'].nunique()
avg_sales_invoices_per_customer = customer_invoices.mean()
avg_returns_invoices_per_customer = df[
    (df['user_type'] == 'customer') & 
    (df['transaction_type'] == 'return')
].groupby('customer_id')['invoice_no'].nunique().mean()

print(f"Average Sales Invoices per Customer: {avg_sales_invoices_per_customer:.2f}")
print(f"Average Returns Invoices per Customer: {avg_returns_invoices_per_customer:.2f}")

# Visualize invoice metrics
plt.figure(figsize=(15, 10))

# Create subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Distribution of items per sales invoice
sns.histplot(data=df[df['transaction_type'] == 'sale'], 
             x=df[df['transaction_type'] == 'sale'].groupby('invoice_no')['quantity'].sum(),
             bins=30, ax=ax1)
ax1.set_title('Distribution of Items per Sales Invoice')
ax1.set_xlabel('Number of Items')
ax1.set_ylabel('Frequency')

# Distribution of items per returns invoice
sns.histplot(data=df[df['transaction_type'] == 'return'], 
             x=df[df['transaction_type'] == 'return'].groupby('invoice_no')['quantity'].sum(),
             bins=30, ax=ax2)
ax2.set_title('Distribution of Items per Returns Invoice')
ax2.set_xlabel('Number of Items')
ax2.set_ylabel('Frequency')

# Distribution of sales invoices per customer
sns.histplot(data=customer_invoices, bins=30, ax=ax3)
ax3.set_title('Distribution of Sales Invoices per Customer')
ax3.set_xlabel('Number of Invoices')
ax3.set_ylabel('Frequency')

# Box plot of items per invoice by transaction type
sns.boxplot(data=df, x='transaction_type', y='quantity', ax=ax4)
ax4.set_title('Items per Invoice by Transaction Type')
ax4.set_xlabel('Transaction Type')
ax4.set_ylabel('Number of Items')

plt.tight_layout()
plt.show()

# 4. Product Analysis
print("\n4. Product Analysis")
print("=" * 50)

# Calculate most sold and returned products
most_sold_quantity = df[df['transaction_type'] == 'sale'].groupby('description')['quantity'].sum().sort_values(ascending=False)
most_returned_quantity = df[df['transaction_type'] == 'return'].groupby('description')['quantity'].sum().sort_values(ascending=False)
most_sold_value = df[df['transaction_type'] == 'sale'].groupby('description')['total'].sum().sort_values(ascending=False)
most_returned_value = df[df['transaction_type'] == 'return'].groupby('description')['total'].sum().sort_values(ascending=False)

print("\nTop 10 Most Sold Products by Quantity:")
print(most_sold_quantity.head(10))
print("\nTop 10 Most Returned Products by Quantity:")
print(most_returned_quantity.head(10))
print("\nTop 10 Most Sold Products by Value:")
print(most_sold_value.head(10))
print("\nTop 10 Most Returned Products by Value:")
print(most_returned_value.head(10))

# Visualize product metrics
plt.figure(figsize=(20, 15))

# Create subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))

# Most sold products by quantity
most_sold_quantity.head(10).plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Most Sold Products by Quantity')
ax1.set_xlabel('Product')
ax1.set_ylabel('Quantity Sold')
ax1.tick_params(axis='x', rotation=45)

# Most returned products by quantity
most_returned_quantity.head(10).plot(kind='bar', ax=ax2)
ax2.set_title('Top 10 Most Returned Products by Quantity')
ax2.set_xlabel('Product')
ax2.set_ylabel('Quantity Returned')
ax2.tick_params(axis='x', rotation=45)

# Most sold products by value
most_sold_value.head(10).plot(kind='bar', ax=ax3)
ax3.set_title('Top 10 Most Sold Products by Value')
ax3.set_xlabel('Product')
ax3.set_ylabel('Total Sales Value')
ax3.tick_params(axis='x', rotation=45)

# Most returned products by value
most_returned_value.head(10).plot(kind='bar', ax=ax4)
ax4.set_title('Top 10 Most Returned Products by Value')
ax4.set_xlabel('Product')
ax4.set_ylabel('Total Returns Value')
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 5. Country Analysis
print("\n5. Country Analysis")
print("=" * 50)

# Calculate return rates by country
country_sales = df[df['transaction_type'] == 'sale'].groupby('country').size()
country_returns = df[df['transaction_type'] == 'return'].groupby('country').size()
country_return_rates = (country_returns / country_sales * 100).sort_values(ascending=False)

print("\nReturn Rates by Country:")
print(country_return_rates)

# Visualize country metrics
plt.figure(figsize=(15, 10))

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Return rates by country
country_return_rates.head(10).plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Countries by Return Rate')
ax1.set_xlabel('Country')
ax1.set_ylabel('Return Rate (%)')
ax1.tick_params(axis='x', rotation=45)

# Sales vs Returns by country
top_countries = country_sales.nlargest(10).index
country_comparison = pd.DataFrame({
    'Sales': country_sales[top_countries],
    'Returns': country_returns[top_countries]
})
country_comparison.plot(kind='bar', ax=ax2)
ax2.set_title('Sales vs Returns for Top 10 Countries')
ax2.set_xlabel('Country')
ax2.set_ylabel('Number of Transactions')
ax2.tick_params(axis='x', rotation=45)
ax2.legend()

plt.tight_layout()
plt.show()

# Additional Analysis: Product Return Rate
print("\n6. Product Return Rate Analysis")
print("=" * 50)

# Calculate return rates for products
product_sales = df[df['transaction_type'] == 'sale'].groupby('description')['quantity'].sum()
product_returns = df[df['transaction_type'] == 'return'].groupby('description')['quantity'].sum()
product_return_rates = (product_returns / product_sales * 100).sort_values(ascending=False)

# Filter for products with significant sales (e.g., more than 100 units sold)
significant_products = product_sales[product_sales > 100]
significant_return_rates = product_return_rates[significant_products.index]

print("\nTop 10 Products by Return Rate (min 100 units sold):")
print(significant_return_rates.head(10))

# Visualize product return rates
plt.figure(figsize=(15, 10))

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Top return rate products
significant_return_rates.head(10).plot(kind='bar', ax=ax1)
ax1.set_title('Top 10 Products by Return Rate (min 100 units sold)')
ax1.set_xlabel('Product')
ax1.set_ylabel('Return Rate (%)')
ax1.tick_params(axis='x', rotation=45)

# Distribution of return rates
sns.histplot(data=significant_return_rates, bins=30, ax=ax2)
ax2.set_title('Distribution of Product Return Rates')
ax2.set_xlabel('Return Rate (%)')
ax2.set_ylabel('Number of Products')

plt.tight_layout()
plt.show()
 