import os
import zipfile
import shutil


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

        return {"Message" : "File Upload and Extract Successful.","Zip file uploaded to":destination_zip_path,"Contents extracted to":upload_folder}

    except Exception as e:
        print(e)
        return {"Message": "Something went wrong please check...."}


# Example usage
# if __name__ == "__main__":
#     # Replace these paths with your actual paths
#     zip_file_path = r'C:\\Siraj\\Task\\FastAPI With Scrapy\\expedia_android_bot.zip'
#     upload_folder = r'C:\\Siraj\\Task\\Uploaded_Zip_file'
#
#     upload_and_unzip(zip_file_path, upload_folder)
