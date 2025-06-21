import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Load environment variables from local .env file
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Create the SQLAlchemy engine to establish a connection to the PostgreSQL database
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Load CSV file using ISO-8859-1 encoding due to special characters
df = pd.read_csv('data.csv', encoding  = 'ISO-8859-1')

# Upload the Dataframe into PostgreSQL (AWS RDS)
df.to_sql('raw_data', engine, if_exists='replace', index=False)

print( "Done")