import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil
import sys # Import the sys module

def open_directory(path):
    """
    Opens the specified directory using the system's default file explorer.
    Handles different operating systems (Windows, macOS, Linux).
    """
    if os.path.exists(path):
        if os.path.isdir(path):  # Check if it's a directory
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS or Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.call(["open", path])
                else:  # Linux
                    subprocess.call(["xdg-open", path])
        else:
            messagebox.showerror("Error", f"Path is not a directory: {path}")
    else:
        messagebox.showerror("Error", f"Directory not found: {path}")

def convert_mp4():
    mp4_path = mp4_entry.get()
    if not mp4_path:
        messagebox.showerror("Error", "Please select an MP4 file.")
        return

    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        fps = float(fps_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid width, height, or frame rate.")
        return

    if width <= 0 or height <= 0 or fps <= 0:
        messagebox.showerror("Error", "Width, height, and frame rate must be positive.")
        return

    images_dir = 'images'
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
    os.makedirs(images_dir)

    # Use local FFmpeg from bin directory
    # Get the directory of the currently executing script
    # This works even when __file__ is not defined, like in some IDEs or interactive sessions
    try:
        # This will work when run from a file
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # This will work when run in environments where __file__ is not defined, like some IDEs or interactive shells
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) #

    ffmpeg_path = os.path.join(script_dir, 'bin', 'ffmpeg.exe')

    if not os.path.exists(ffmpeg_path):
        messagebox.showerror("Error", f"FFmpeg not found at {ffmpeg_path}. Ensure 'bin\\ffmpeg.exe' exists in the same directory as the script, within a 'bin' folder.")
        return

    command = [
        ffmpeg_path,
        '-i', mp4_path,
        '-vf', f'fps={fps},scale={width}:{height}:flags=spline+accurate_rnd+full_chroma_int+full_chroma_inp,format=rgba',
        '-c:v', 'png',
        '-compression_level', '0',
        f'{images_dir}\\frame_%03d.png'
    ]
    try:
        subprocess.run(command, check=True, capture_output=True)
        num_pngs = len(os.listdir(images_dir))
        messagebox.showinfo("Success", f"Converted to {num_pngs} PNGs in 'images' directory.")
        # Open the 'images' directory after successful conversion
        open_directory(images_dir)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"FFmpeg failed: {e.stderr.decode()}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred during conversion: {e}")

def select_mp4():
    path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if path:
        mp4_entry.delete(0, tk.END)
        mp4_entry.insert(0, path)

try:
    root = tk.Tk()
    root.title("MP4 to PNG Converter")

    tk.Label(root, text="MP4 File:").grid(row=0, column=0, padx=4, pady=2)
    mp4_entry = tk.Entry(root, width=35)
    mp4_entry.grid(row=0, column=1, padx=4, pady=2)
    tk.Button(root, text="Browse", command=select_mp4).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Width:").grid(row=1, column=0, padx=5, pady=5)
    width_entry = tk.Entry(root)
    width_entry.insert(0, "1280")
    width_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Height:").grid(row=2, column=0, padx=5, pady=5)
    height_entry = tk.Entry(root)
    height_entry.insert(0, "720")
    height_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Frame Rate (fps):").grid(row=3, column=0, padx=5, pady=5)
    fps_entry = tk.Entry(root)
    fps_entry.insert(0, "24")
    fps_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(root, text="Convert", command=convert_mp4).grid(row=4, column=1, padx=5, pady=5)

    root.mainloop()
except Exception as e:
    print(f"Failed to initialize Tkinter: {e}")
    print("Ensure Tcl/Tk and Pillow are installed (e.g., 'pip install Pillow') and 'bin\\ffmpeg.exe' is in the script directory.")
