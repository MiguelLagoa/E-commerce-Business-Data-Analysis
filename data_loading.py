import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()


db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Step 2: Connect to RDS PostgreSQL
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Step 3: Load your CSV
df = pd.read_csv('data.csv', encoding  = 'ISO-8859-1')

# Step 4: Upload to database
df.to_sql('raw_data', engine, if_exists='replace', index=False)

print("✅ Upload successful!")

