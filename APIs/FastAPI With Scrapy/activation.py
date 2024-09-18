import os
import subprocess
import sys

venv_path = "C:\\Siraj\\Task\\Uploaded_Zip_file\\expedia_android_bot"

def activate_venv(venv_path):
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path,'env','Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            # Run the activation script in a new shell process
            subprocess.run([activate_script], shell=True, check=True)
        else:
            print(f"Virtual environment activation script not found at {activate_script}")

def install_requirements(venv_path):
    requirements_file = os.path.join(os.path.dirname(sys.executable), 'requirements.txt')
    if os.path.exists(requirements_file):
        print(f"Installing requirements from {requirements_file}...")
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
        subprocess.check_call([pip_path, 'install', '-r', requirements_file])
        print("Requirements installed.")
    else:
        print(f"{requirements_file} does not exist.")

def main():
    # Note: Shell command runs in a new process, so subsequent Python commands won't run in the activated environment.
    # This approach works for running external commands, but for in-script usage, activation is not necessary.

    activate_venv(venv_path)

    # Install requirements should be called after environment activation in a different process
    install_requirements(venv_path)

if __name__ == "__main__":
    main()
