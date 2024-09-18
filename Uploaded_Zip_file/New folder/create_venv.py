import os
import subprocess
import sys


def create_venv(directory):
    venv_path = os.path.join(directory, 'env')
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment in {venv_path}...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print(f"Virtual environment created at: {venv_path}")
    return venv_path


def generate_requirements_file(directory):
    requirements_file = os.path.join(directory, 'requirements.txt')
    if not os.path.exists(requirements_file):
        print(f"{requirements_file} does not exist. Generating it...")
        # Activate the venv to run pip freeze
        venv_path = os.path.join(directory, 'env')
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin',
                                                                                                      'pip')

        # Create a temporary venv to use pip freeze
        temp_venv_path = os.path.join(directory, 'temp_venv')
        subprocess.check_call([sys.executable, '-m', 'venv', temp_venv_path])
        temp_pip_path = os.path.join(temp_venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(
            temp_venv_path, 'bin', 'pip')

        # Install the project in the temporary venv
        subprocess.check_call([temp_pip_path, 'install', 'scrapy'])  # Adjust this if necessary

        # Freeze the installed packages to requirements.txt
        subprocess.check_call([temp_pip_path, 'freeze', '>', requirements_file], shell=True)

        # Clean up the temporary venv
        subprocess.check_call(['rmdir', '/s', '/q', temp_venv_path], shell=True)
        print(f"Generated {requirements_file} with current dependencies.")
    else:
        print(f"{requirements_file} already exists.")


def install_requirements(venv_path):
    requirements_file = os.path.join(os.path.dirname(sys.executable), 'requirements.txt')
    if os.path.exists(requirements_file):
        print(f"Installing requirements from {requirements_file}...")
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin',
                                                                                                      'pip')
        subprocess.check_call([pip_path, 'install', '-r', requirements_file])
        print("Requirements installed.")
    else:
        print(f"{requirements_file} does not exist, but it should have been created.")


def check_and_install():
    # Directory where the script is located
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = r'C:\Siraj\Task\Uploaded_Zip_file\checkers'

    venv_path = os.path.join(script_dir, 'env')
    if not os.path.exists(venv_path):
        # If venv does not exist, create it
        venv_path = create_venv(script_dir)

    generate_requirements_file(script_dir)
    install_requirements(venv_path)


if __name__ == "__main__":
    check_and_install()
