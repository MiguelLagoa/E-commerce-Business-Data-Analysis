import pandas as pd
from sqlalchemy import create_engine

# Local PostgreSQL credentials
db_user = 'postgres'
db_pass = 'Oscarinho_69!'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

# Read CSV with correct date parsing
df = pd.read_csv('data.csv', encoding='ISO-8859-1', parse_dates=['InvoiceDate'], dayfirst=False)

# Optional: Format date column explicitly to ensure it's consistent
df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%m/%d/%Y %H:%M')

# Re-convert to datetime object so it uploads correctly to PostgreSQL
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M')

# Create connection
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Upload to PostgreSQL
df.to_sql('raw_data', engine, if_exists='replace', index=False)

print("✅ Upload successful with correct datetime format!")
