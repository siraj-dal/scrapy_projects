from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import os
import uvicorn
import pymysql
import datetime

app = FastAPI()

config_file: str = "C:/project_files/travel_project/expedia/project_configs.json"

if os.path.exists(config_file):
    with open(config_file, 'r') as config:
        configs: dict = json.load(config)
else:
    project_config_path: str = "/".join(config_file.split('/')[:-1])
    os.makedirs(project_config_path)

client = pymysql.connect(host=configs['config']['host'],
                         user=configs['config']['user'],
                         password=configs['config']['password'],
                         database=configs['config']['database'])
cursor = client.cursor()


# Define the payload models
class RangePayload(BaseModel):
    start: int
    end: int

# Placeholder for storing the extraction count
extraction_counts = {
    'total': 0,
    'done': 0,
}

# @app.post("/start_crawl/")
# async def start_crawl(payload: RangePayload):
#     global extraction_counts
#     # Set the extraction counts
#     extraction_counts['total'] = payload.end - payload.start + 1
#     extraction_counts['done'] = 0
#
#     try:
#         # Run the link extraction script
#         link_extract_path = 'C:\Siraj\Task\FastAPI With Scrapy\expedia_android_bot\expedia_android_bot\expedia_android_bot\daily_link_generator.py'
#         subprocess.Popen(['python', link_extract_path])
#
#         # Run the Scrapy spider
#         price_spider_path = 'C:\Siraj\Task\FastAPI With Scrapy\expedia_android_bot\expedia_android_bot\expedia_android_bot\spiders\price_scraper.py'
#         subprocess.Popen(['scrapy', 'crawl', price_spider_path, str(payload.start), str(payload.end)])
#
#         return {"status": "Crawl started"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/start_crawl")
async def start_crawl(start: int, end: int):
    global extraction_counts
    # Set the extraction counts
    extraction_counts['total'] = end - start + 1
    extraction_counts['done'] = 0
    try:
        # Run the Link Extraction File
        subprocess.Popen(['python', 'daily_link_generator.py'])

        # Construct the command with arguments
        command = [
            'scrapy',
            'crawl',
            'price_scraper',
            '-a', f'start={start}',
            '-a', f'end={end}'
        ]

        # Run the Scrapy spider
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # This makes stdout and stderr return as strings, not bytes
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Error running Scrapy spider: {stderr}"
            )

        return {"status": "Crawl started", "output": stdout}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/extraction_status")
async def extraction_status():
    global extraction_counts
    today_date = datetime.datetime.today().strftime('%Y_%m_%d')
    daily_link_table = configs['tables']['link_table'] + '_' + today_date

    cursor.execute(f"SELECT count(*) FROM {daily_link_table}")
    fetched_total_count = cursor.fetchone()[0]
    cursor.execute(f"SELECT count(*) FROM {daily_link_table} where status='Done'")
    fetched_done_count = cursor.fetchone()[0]
    cursor.execute(f"SELECT count(*) FROM {daily_link_table} where status='Pending'")
    fetched_pending_count = cursor.fetchone()[0]
    cursor.execute(f"SELECT count(*) FROM {daily_link_table} where status='Not Available'")
    fetched_na_count = cursor.fetchone()[0]

    extraction_counts = {
        'Total': fetched_total_count,
        'Done': fetched_done_count,
        'Pending': fetched_pending_count,
        'Not Available': fetched_na_count,
    }
    return extraction_counts

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="172.28.151.161", port=8000)

