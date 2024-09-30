import pandas as pd
import pymysql

# # Creating a connection to SQL Database
connection = pymysql.connect(host='localhost', user='root', database='storeLocator', password='actowiz', charset='utf8mb4', autocommit=True)

table_name = 'apple_18_09_2024'

fetch_query = f'''SELECT * FROM {table_name};'''  # Query that will retrieve all data from Database table

excel_path = r"C:\Users\jaimin.gurjar\Downloads"
# Create Excel file form SQL data
dataframe = pd.read_sql(sql=fetch_query, con=connection).drop(columns='index_id')


filename = table_name + '_states' + '.xlsx'
writer = pd.ExcelWriter(
    path=excel_path + fr"\{filename}",
    engine='xlsxwriter',
    engine_kwargs={'options': {'strings_to_urls': False}}
)
dataframe.to_excel(excel_writer=writer, index=False)

# dataframe.to_excel(writer)
writer.close()
