import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#load environment details from a local .env file 
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Connect to RDS PostgreSQL using SQLalchemy engine 
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Load CSV. 
# CSV had special characters so had to use 'ISO-8859-1' encoding 
df = pd.read_csv('data.csv', encoding  = 'ISO-8859-1')

# Upload the dataframe to the PostgreSQL database under alias of "raw_data". If file already exists it is updated.
df.to_sql('raw_data', engine, if_exists='replace', index=False)

print( "Done")

