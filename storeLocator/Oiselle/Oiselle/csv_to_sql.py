import pandas as pd
from sqlalchemy import create_engine

# Replace with your CSV file path
csv_file = r'C:\Siraj\Work\storeLocator\Reference\state_table.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Database connection URL: 'mysql+pymysql://username:password@host:port/database'
# Replace with your MySQL connection details
database_url = 'mysql+pymysql://root:actowiz@localhost:3306/apparel_store_locator'

# Create an SQLAlchemy engine to connect to the MySQL database
engine = create_engine(database_url)

# Name of the table you want to create in MySQL
table_name = 'state_with_lat_long'

# Write the DataFrame to SQL
df.to_sql(table_name, con=engine, index=False, if_exists='replace')

print(f"Table '{table_name}' created successfully in the MySQL database.")
