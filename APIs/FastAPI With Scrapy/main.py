import asyncio
from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel
import json
import os
import uvicorn
import pymysql
import datetime
from upload_file import upload_and_unzip
from find_paths import get_file_path,find_directory
from v_env import install_requirements,activate_venv,generate_requirements_file
import subprocess
import sys
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

@app.get("/file")
async def start_crawl_file(project_name: str,file_name: str):
    project_path = ''
    file_path = None
    try:
        folder_path = r"C:\Siraj\Task\Uploaded_Zip_file"
        file_lists = os.listdir(folder_path)
        if project_name in file_lists:
            project_path = folder_path + f'\\{project_name}'
            file_path = get_file_path(project_path,f'{file_name}.py')
            print(file_path)
            print("Checking for requirement.txt.............")
            generate_requirements_file(project_path)
            print("Active environment.............")
            activate_venv(project_path)
            print("Install requirement.txt.............")
            install_requirements(project_path)
            # output = await run_command(['python', f'daily_link_generator.py'])

            output = await run_command(['python', fr'{file_path}'])

            return {"status": "File Running Process Done....."}
        else:
            return {"status": "Project Details not available upload your project."}

    except Exception as e:
        if 'ModuleNotFoundError' in str(e):
            print("Active environment.............")
            activate_venv(project_path)
            module_name = str(e).split("No module named")[-1].replace("\r","").replace("\n","").replace("'","")
            pip_path = os.path.join(project_path, 'env', 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(
                project_path, 'bin', 'pip')

            subprocess.check_call([pip_path, 'install', module_name])
            print("Requirements installed.")
            python_path = os.path.join(project_path, 'env', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(
                project_path, 'bin', 'python')
            output = await run_command([python_path, fr'{file_path}'])
            return {"status": f"File Running Process Done.....{output}"}
        else:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/data")
async def start_crawl_data(project_name: str,spider_name: str,request:Request):
    params = request.query_params
    start = params.get('start')
    end = params.get('end')
    try:
        folder_path = r"C:\Siraj\Task\Uploaded_Zip_file"
        project_path = os.path.join(folder_path, project_name)

        if os.path.exists(project_path):
            # spider_file_path = get_file_path(project_path,'spiders')
            spider_dir_path = find_directory(project_path, 'spiders')
            if not spider_dir_path:
                raise HTTPException(status_code=404, detail="Spider file not found.")

            os.chdir(spider_dir_path)
            print("Checking for requirement.txt.............")
            generate_requirements_file(project_path)
            print("Active environment.............")
            activate_venv(project_path)
            print("Install requirement.txt.............")
            install_requirements(project_path)
            output = ''
            try:
                if not start and not end:
                    command = [
                        'scrapy', 'crawl', f'{spider_name}'
                    ]

                    # print(command)
                    output = await run_command(command)
                else:
                    command = [
                        'scrapy', 'crawl', f'{spider_name}',
                        '-a', f'start={start}',
                        '-a', f'end={end}'
                    ]
                    output = await run_command(command)
                return {"status": "Crawl started", "output": output}
            except Exception as e:
                if 'ModuleNotFoundError' in str(e):
                    module_name = str(e).split("No module named")[-1].replace("\r", "").replace("\n", "").replace("'",
                                                                                                                  "")
                    pip_path = os.path.join(project_path, 'env', 'Scripts','pip.exe') if os.name == 'nt' else os.path.join(project_path, 'bin', 'pip')

                    subprocess.check_call([pip_path, 'install', module_name])
                    print("Requirements installed.")
                    # await start_crawl_file(project_name,file_name)
                else:
                    raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        a = e
        print(a)
        raise HTTPException(status_code=500, detail=str(e))
        # raise KeyError


@app.get("/extraction_status")
async def extraction_status(host:str,user:str,password:str,database:str,table_name:str):

    config_file = "C:/project_files/travel_project/expedia/project_configs.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            configs = json.load(config)
    else:
        project_config_path = os.path.dirname(config_file)
        os.makedirs(project_config_path)

    # Database connection
    # client = pymysql.connect(
    #     host=configs['config']['host'],
    #     user=configs['config']['user'],
    #     password=configs['config']['password'],
    #     database=configs['config']['database']
    # )
    client = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    cursor = client.cursor()
    today_date = datetime.datetime.today().strftime('%Y_%m_%d')
    # daily_link_table = f"{configs['tables']['link_table']}_{today_date}"
    daily_link_table = table_name

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
    uvicorn.run(app, host="172.28.151.37", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
