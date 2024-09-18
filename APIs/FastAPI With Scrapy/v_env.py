import os
import subprocess
import sys

# def create_venv(directory):
#     venv_path = os.path.join(directory, 'env')
#     if not os.path.exists(venv_path):
#         print(f"Creating virtual environment in {venv_path}...")
#         subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
#         print(f"Virtual environment created at: {venv_path}")
#     return venv_path


# def generate_requirements_file(directory):
#     requirements_file = os.path.join(directory, 'requirements.txt')
#     if not os.path.exists(requirements_file):
#         print(f"{requirements_file} does not exist. Generating it...")
#         # Activate the venv to run pip freeze
#         venv_path = os.path.join(directory, 'env')
#         pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin',
#                                                                                                       'pip')
#
#         # Create a temporary venv to use pip freeze
#         temp_venv_path = os.path.join(directory, 'temp_venv')
#         subprocess.check_call([sys.executable, '-m', 'venv', temp_venv_path])
#         temp_pip_path = os.path.join(temp_venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(
#             temp_venv_path, 'bin', 'pip')
#
#         # Install the project in the temporary venv
#         subprocess.check_call([temp_pip_path, 'install', 'scrapy'])  # Adjust this if necessary
#
#         # Freeze the installed packages to requirements.txt
#         subprocess.check_call([temp_pip_path, 'freeze', '>', requirements_file], shell=True)
#
#         # Clean up the temporary venv
#         subprocess.check_call(['rmdir', '/s', '/q', temp_venv_path], shell=True)
#         print(f"Generated {requirements_file} with current dependencies.")
#     else:
#         print(f"{requirements_file} already exists.")
def create_venv(directory):
    venv_path = os.path.join(directory, 'env')
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment in {venv_path}...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        # subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print(f"Virtual environment created at: {venv_path}")

        # Install pipreqs and pipdeptree in the newly created virtual environment
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin',
                                                                                                      'pip')
        print("Installing pipreqs and pipdeptree...")
        subprocess.check_call([pip_path, 'install', 'pipreqs'])
        print("pipreqs installed.")
        # subprocess.check_call([pip_path, 'install', 'pipdeptree'])

    return venv_path


def generate_requirements_file(directory):
    requirements_file = os.path.join(directory, 'requirements.txt')
    dependency_tree_file = os.path.join(directory, 'dependency_tree.txt')

    # Create virtual environment and ensure tools are installed
    venv_path = create_venv(directory)
    pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin',
                                                                                                  'pip')
    pipreqs_path = os.path.join(venv_path, 'Scripts', 'pipreqs.exe') if os.name == 'nt' else 'pipreqs'
    pipdeptree_path = os.path.join(venv_path, 'Scripts', 'pipdeptree.exe') if os.name == 'nt' else 'pipdeptree'

    # Check if `requirements.txt` already exists
    if not os.path.exists(requirements_file):
        print(f"{requirements_file} does not exist. Generating it...")

        # 1. Generate `requirements.txt` using `pip freeze`
        with open(requirements_file, 'w') as f:
            subprocess.run([pip_path, 'freeze'], stdout=f, check=True)
        print(f"Generated {requirements_file} with current dependencies.")

        # 2. Generate `requirements.txt` using `pipreqs` (overwrites the previous file)
        try:
            print("Generating requirements using pipreqs...")
            subprocess.run([pipreqs_path, directory, '--force'], check=True)
            print(f"Updated {requirements_file} with packages used in the code.")
        except FileNotFoundError:
            print(f"pipreqs not found at {pipreqs_path}. Make sure pipreqs is installed.")
        except subprocess.CalledProcessError as e:
            print(f"Error running pipreqs: {e}")

        # 3. Generate dependency tree file using `pipdeptree`
        # try:
        #     print("Generating dependency tree using pipdeptree...")
        #     with open(dependency_tree_file, 'w') as f:
        #         subprocess.run([pipdeptree_path], stdout=f, check=True)
        #     print(f"Generated {dependency_tree_file} with the dependency tree.")
        # except FileNotFoundError:
        #     print(f"pipdeptree not found at {pipdeptree_path}. Make sure pipdeptree is installed.")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error running pipdeptree: {e}")

    else:
        print(f"{requirements_file} already exists.")


def activate_venv(venv_path):
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path,'env','Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            # Run the activation script in a new shell process
            subprocess.run([activate_script], shell=True, check=True)
            print(f"Virtual environment activate..........")
        else:
            print(f"Virtual environment activation script not found at {activate_script}")


def install_requirements(venv_path):
    # requirements_file = os.path.join(os.path.dirname(sys.executable), 'requirements.txt')
    requirements_file = os.path.join(venv_path, 'requirements.txt')
    if os.path.exists(requirements_file):
        print(f"Installing requirements from {requirements_file}...")
        pip_path = os.path.join(venv_path,'env','Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
        subprocess.check_call([pip_path, 'install', '-r', requirements_file])
        print("Requirements installed.")
    else:
        print(f"{requirements_file} does not exist.")

# if __name__ == "__main__":
#     # Directory where the script is located
#     # script_dir = os.path.dirname(os.path.abspath(__file__))
#     # print(script_dir)
#     script_dir = r'C:\Siraj\Task\Uploaded_Zip_file\checkers'
#
#     venv_path = create_venv(script_dir)
#     generate_requirements_file(script_dir)
#     install_requirements(venv_path)
