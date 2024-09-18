import shutil
import zipfile
import os
import time
# from v_env import *
from v_env import create_venv,generate_requirements_file


def upload_and_unzip(zip_file_path, upload_folder):
    try:
        # Ensure the upload folder exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Determine the file name from the zip file path
        zip_file_name = os.path.basename(zip_file_path)

        # Define the destination path for the zip file
        destination_zip_path = os.path.join(upload_folder, zip_file_name)

        # Move the zip file to the upload folder
        shutil.copy(zip_file_path, destination_zip_path)
        print(f"Zip file uploaded to: {destination_zip_path}")

        # Unzip the file
        with zipfile.ZipFile(destination_zip_path, 'r') as zip_ref:
            # Extract all contents into the upload folder
            zip_ref.extractall(upload_folder)
            print(f"Contents extracted to: {upload_folder}")

        # Function to attempt file removal with retries
        def remove_file_with_retry(file_path, retries=5, delay=1):
            for attempt in range(retries):
                try:
                    os.remove(file_path)
                    print(f"Zip file removed: {file_path}")
                    return True
                except PermissionError:
                    print(f"Attempt {attempt + 1}: File is in use, retrying in {delay} seconds...")
                    time.sleep(delay)
            return False

        # Remove the zip file after extraction
        if not remove_file_with_retry(destination_zip_path):
            raise Exception(f"Failed to remove file {destination_zip_path} after multiple attempts.")

        script_dir = destination_zip_path.replace('.zip','')
        print("Checking for environment.............")
        venv_path = create_venv(script_dir)
        print("Checking for requirement.txt.............")
        generate_requirements_file(script_dir)
        # print("Install requirement.txt.............")
        # install_requirements(venv_path)

        return {"Message": "File Upload, Extract, and Cleanup Successful.",
                "Contents extracted to": upload_folder,
                "Extract File Path" : destination_zip_path.replace('.zip','')}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Message": "Something went wrong. Please check the logs for details."}


# Example usage
if __name__ == "__main__":
    # Replace these paths with your actual paths
    # zip_file_path = r'C:\\Siraj\\Task\\FastAPI With Scrapy\\expedia_android_bot.zip'
    zip_file_path = r'C:\Siraj\Task\APIs\expedia_android_bot.zip'
    upload_folder = r'C:\\Siraj\\Task\\Uploaded_Zip_file'

    a = upload_and_unzip(zip_file_path, upload_folder)
    print(a)
