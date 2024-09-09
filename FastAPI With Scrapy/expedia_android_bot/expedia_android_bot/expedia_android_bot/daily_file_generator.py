import json
import datetime
import os

import pandas as pd
from sqlalchemy import create_engine

config_file: str = "C:/project_files/travel_project/expedia/project_configs.json"

if os.path.exists(config_file):
    with open(config_file, 'r') as config:
        configs: dict = json.load(config)
else:
    project_config_path: str = "/".join(config_file.split('/')[:-1])
    os.makedirs(project_config_path)

today_date = datetime.datetime.today().strftime('%Y_%m_%d')

local_output_path = 'C:/project_files/travel_project/expedia/expedia_bot_output/'
file_server_output_path = fr'\\192.168.1.223\File Server\HotelAggregators\Expedia\{today_date}'

output_locations = [local_output_path]

for path in output_locations:
    if not os.path.exists(path):
        os.makedirs(path)

client = create_engine(f"mysql+pymysql://{configs['config']['user']}:{configs['config']['password']}@{configs['config']['host']}/{configs['config']['database']}")

daily_data_table = configs['tables']['data_table'] + '_' + today_date

sql_df = pd.read_sql_table(daily_data_table, client)
sql_df.drop(columns=['page_hash', 'id'], inplace=True)
sql_df.fillna('NA')

for path in output_locations:
    filename = 'expedia' + f'_{today_date}.xlsx'
    writer = pd.ExcelWriter(path=path + filename,
                            engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}})
    sql_df.to_excel(writer)
    writer.close()

a = []
b = 1
print(type(b))
