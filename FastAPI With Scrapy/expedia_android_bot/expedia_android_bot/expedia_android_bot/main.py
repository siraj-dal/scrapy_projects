import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import uvicorn
import pymysql
import datetime
from upload_file import upload_and_unzip

app = FastAPI()


# Define payload models
class RangePayload(BaseModel):
    start: int
    end: int


async def run_command(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error: {stderr.decode()}")
    return stdout.decode()


@app.get("/start_crawl")
async def start_crawl(start: int, end: int):
    global extraction_counts
    extraction_counts['total'] = end - start + 1
    extraction_counts['done'] = 0

    try:
        await run_command(['python', 'daily_link_generator.py'])

        command = [
            'scrapy', 'crawl', 'price_scraper',
            '-a', f'start={start}',
            '-a', f'end={end}'
        ]
        output = await run_command(command)

        return {"status": "Crawl started", "output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/extraction_status")
async def extraction_status():

    config_file = "C:/project_files/travel_project/expedia/project_configs.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            configs = json.load(config)
    else:
        project_config_path = os.path.dirname(config_file)
        os.makedirs(project_config_path)

    # Database connection
    client = pymysql.connect(
        host=configs['config']['host'],
        user=configs['config']['user'],
        password=configs['config']['password'],
        database=configs['config']['database']
    )
    cursor = client.cursor()
    today_date = datetime.datetime.today().strftime('%Y_%m_%d')
    daily_link_table = f"{configs['tables']['link_table']}_{today_date}"

    try:
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
        print(extraction_counts)
        client.close()
        return extraction_counts

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/upload_files")
async def upload_files(zip_file_path:str,upload_folder:str):

    try:
        if zip_file_path and upload_folder:
            return upload_and_unzip(zip_file_path, upload_folder)
        else:
            return "Please provide valid file path..."

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="172.28.151.161", port=8000)
