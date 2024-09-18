# import os
#
# folder_path = r"C:\Siraj\Task\Uploaded_Zip_file"
# files = os.listdir(folder_path)
# print(files)
#
# project_name = 'expedia_android_bot'
#
# if project_name in files:
#     print("Project availblable")
# else:
#     print("Project not availblable")

import zipfile
import os
import tempfile


# def extract_zip(zip_path, extract_to):
#     """Extracts the zip file to the specified directory."""
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_to)


def find_file(directory, filename):
    """Searches for a specific file in the specified directory and subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    return None

def find_directory(root_dir, target_dir_name):
    """Searches for a specific directory in the specified root directory and subdirectories."""
    for root, dirs, files in os.walk(root_dir):
        if target_dir_name in dirs:
            return os.path.join(root, target_dir_name)
    return None


def find_spider_file(directory: str, spider_name: str) -> str:
    """Searches for a specific spider file in the directory."""
    spider_file_name = f"{spider_name}.py"
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == spider_file_name:
                return os.path.join(root, file)
    return None

def get_file_path(zip_file_path, search_filename):
    # Create a temporary directory to extract the zip file
    # with tempfile.TemporaryDirectory() as temp_dir:
    #     # print(f"Extracting {zip_file_path} to {temp_dir}...")
    #     # extract_zip(zip_file_path, temp_dir)
    #
    #     print(f"Searching for '{search_filename}'...")
    file_path = find_file(zip_file_path, search_filename)

    if file_path:
        print(f"File found: {file_path}")
    else:
        print("File not found.")
    return file_path

# if __name__ == "__main__":
#     # Path to your zip file and the filename you are searching for
#     zip_file_path = r'C:\Siraj\Task\Uploaded_Zip_file\expedia_android_bot'
#     search_filename = 'daily_link_generator.py'
#     get_file_path(zip_file_path,search_filename)
