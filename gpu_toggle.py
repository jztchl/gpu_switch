import tkinter as tk
from tkinter import ttk
import subprocess
import json
import threading
import pystray
import sys
import os
from pystray import MenuItem as item
from PIL import Image


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev & PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def run_powershell(command):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True, text=True
    )
    return result

def get_display_adapters():
    command = """
    Get-PnpDevice -Class Display |
    Where-Object { $_.InstanceId -ne $null } |
    Select-Object -Property FriendlyName, InstanceId |
    ConvertTo-Json
    """
    result = run_powershell(command)
    try:
        parsed = json.loads(result.stdout)
        return parsed if isinstance(parsed, list) else [parsed]
    except:
        return []

def get_gpu_status(instance_id):
    try:
        result = run_powershell(f"(Get-PnpDevice -InstanceId '{instance_id}').Status")
        code = result.stdout.strip()
        return "ENABLED" if code == "OK" else "DISABLED"
    except:
        return "UNKNOWN"

def refresh_status():
    selected = selected_gpu.get()
    instance_id = gpu_map.get(selected)
    if not instance_id:
        status_var.set("NO GPU ❌")
        return
    status = get_gpu_status(instance_id)
    status_var.set(f"{status} ✅" if status == "ENABLED" else f"{status} ❌")
    toggle_var.set(status.lower())

def toggle_gpu():
    def toggle():
        selected = selected_gpu.get()
        instance_id = gpu_map.get(selected)
        if not instance_id:
            output_text.set("❌ No GPU selected.")
            return
        loading_var.set(True)
        root.update()

        choice = toggle_var.get()
        if choice == "enabled":
            result = run_powershell(f'Enable-PnpDevice -InstanceId "{instance_id}" -Confirm:$false')
        elif choice == "disabled":
            result = run_powershell(f'Disable-PnpDevice -InstanceId "{instance_id}" -Confirm:$false')

        output_text.set(f"✅ GPU {choice.upper()}!\n\n" + result.stdout + result.stderr)
        refresh_status()
        loading_var.set(False)

    threading.Thread(target=toggle).start()

def update_loading_indicator():
    def loop():
        if loading_var.get():
            current = loading_label.cget("text")
            next_text = {
                "": "LOADING.",
                "LOADING.": "LOADING..",
                "LOADING..": "LOADING...",
                "LOADING...": "LOADING."
            }.get(current, "LOADING.")
            loading_label.config(text=next_text)
        else:
            loading_label.config(text="")
        root.after(300, loop)
    loop()

def create_tray_icon():
    def on_exit():
        icon.stop()
        root.quit()

    def show_window():
        root.deiconify()
        root.lift()
    icon_path = resource_path("gamer.ico")
    icon_img = Image.open(icon_path)
    menu = (item('Show', show_window), item('Exit', on_exit))
    icon = pystray.Icon("GPU_Toggler", icon_img, "GPU Toggler", menu)
    threading.Thread(target=icon.run, daemon=True).start()

gpus = get_display_adapters()
gpu_map = {gpu["FriendlyName"]: gpu["InstanceId"] for gpu in gpus}

root = tk.Tk()
root.title("🧠 GPU Toggler: GAMER MODE 🔥")
root.geometry("600x500")
root.configure(bg="#0F0F0F")

selected_gpu = tk.StringVar()
selected_gpu.set(next(iter(gpu_map), "NO GPU FOUND"))
toggle_var = tk.StringVar()
status_var = tk.StringVar()
output_text = tk.StringVar()
loading_var = tk.BooleanVar(value=False)

def on_gpu_select(*args):
    refresh_status()
selected_gpu.trace("w", on_gpu_select)

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#0F0F0F", foreground="#08F7FE", font=("Consolas", 12))
style.configure("TButton", font=("Consolas", 12), background="#1A1A1A", foreground="#08F7FE", padding=6)
style.configure("TRadiobutton", background="#0F0F0F", foreground="#08F7FE", font=("Consolas", 12))
style.configure("TFrame", background="#0F0F0F")

ttk.Label(root, text="🎮 SELECT GPU TO TOGGLE ⚙️", font=("Consolas", 16, "bold"), foreground="#00FFAA", background="#0F0F0F").pack(pady=15)

option_menu = tk.OptionMenu(root, selected_gpu, *gpu_map.keys())
option_menu.config(
    font=("Consolas", 12),
    bg="#1A1A1A",
    fg="#08F7FE",
    activebackground="#222",
    activeforeground="#00FFAA",
    highlightthickness=2,
    highlightbackground="#08F7FE"
)
option_menu.pack(pady=5)

status_label = ttk.Label(root, textvariable=status_var, font=("Consolas", 14, "bold"))
status_label.pack(pady=10)

radio_frame = ttk.Frame(root)
radio_frame.pack(pady=10)

ttk.Radiobutton(radio_frame, text="🟢 ENABLE GPU", variable=toggle_var, value="enabled", command=toggle_gpu).pack(pady=5)
ttk.Radiobutton(radio_frame, text="🔴 DISABLE GPU", variable=toggle_var, value="disabled", command=toggle_gpu).pack(pady=5)

loading_label = ttk.Label(root, text="", font=("Consolas", 12), foreground="#08F7FE", background="#0F0F0F")
loading_label.pack(pady=5)

ttk.Button(root, text="🔄 REFRESH STATUS", command=refresh_status).pack(pady=15)

output_label = ttk.Label(
    root, textvariable=output_text,
    wraplength=550, justify="left",
    font=("Consolas", 10), background="#0F0F0F", foreground="#DDDDDD"
)
output_label.pack(pady=10)

update_loading_indicator()
create_tray_icon()
refresh_status()

root.mainloop()
