import pandas as pd
from sqlalchemy import create_engine

# Define your file path and sheet name
# excel_path = r"C:\Users\jaimin.gurjar\Downloads\states_usa.xlsx"
excel_path = r"C:\Users\jaimin.gurjar\Downloads\states_store_locator.xlsx"
sheet_name = 'Sheet1'  # Replace with the sheet name you want to read from

# Read the Excel file into a pandas DataFrame
# df = pd.read_excel(excel_path, sheet_name=sheet_name)
# amz_df = pd.read_excel(amz_excel_path, engine='calamine')
# bb_df = pd.read_excel(bb_excel_path, engine='calamine')
# blk_df = pd.read_excel(blk_excel_path, engine='calamine')
# dmt_df = pd.read_excel(dmt_excel_path, engine='calamine')
df = pd.read_excel(excel_path, engine='calamine')


# Database connection details
db_type = 'mysql+pymysql'  # Example for MySQL; adjust for your database type (e.g., 'sqlite', 'postgresql')
username = 'root'
password = 'actowiz'
host = 'localhost'  # 'localhost' if running on your local machine
port = '3306'  # Default for MySQL is '3306'
database = 'storeLocator'

# Create the SQLAlchemy engine to connect to the SQL database
engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database}')

# Define the table name where you want to store the data
# amz_table_name = 'mapped_amazon_input_new'
# bb_table_name = 'mapped_bb_input_new'
# blk_table_name = 'mapped_blk_input_new'
# dmt_table_name = 'mapped_dmt_input_new'

# Store the DataFrame in the SQL table
# amz_df.to_sql(amz_table_name, con=engine, if_exists='replace', index=False)
# print(f"Data from {amz_excel_path} has been successfully stored in the {amz_table_name} table in the {database} database.")
# bb_df.to_sql(bb_table_name, con=engine, if_exists='replace', index=False)
# print(f"Data from {bb_excel_path} has been successfully stored in the {bb_table_name} table in the {database} database.")
# blk_df.to_sql(blk_table_name, con=engine, if_exists='replace', index=False)
# print(f"Data from {blk_excel_path} has been successfully stored in the {blk_table_name} table in the {database} database.")
# dmt_df.to_sql(dmt_table_name, con=engine, if_exists='replace', index=False)
# print(f"Data from {dmt_excel_path} has been successfully stored in the {dmt_table_name} table in the {database} database.")

df.to_sql('states_store_locator', con=engine, if_exists='replace', index=False)
print(f"Data from {excel_path} has been successfully stored in the states_usa table in the {database} database.")
