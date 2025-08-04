import tkinter as tk
import subprocess

def run_powershell(command):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True, text=True
    )
    return result

def get_display_adapters():
    """Fetch all GPUs with their name and instance ID"""
    command = """
    Get-PnpDevice -Class Display | 
    Where-Object { $_.InstanceId -ne $null } |
    Select-Object -Property FriendlyName, InstanceId |
    ConvertTo-Json
    """
    result = run_powershell(command)
    try:
        import json
        parsed = json.loads(result.stdout)
        return parsed if isinstance(parsed, list) else [parsed]
    except Exception as e:
        return []

def get_gpu_status(instance_id):
    try:
        result = run_powershell(f"(Get-PnpDevice -InstanceId '{instance_id}').Status")
        code = result.stdout.strip()
        return "ENABLED ✅" if code == "OK" else "DISABLED ❌"
    except Exception as e:
        return f"ERROR: {e}"

def refresh_status():
    selected = selected_gpu.get()
    instance_id = gpu_map.get(selected)
    if not instance_id:
        status_var.set("No GPU Selected ❌")
        return
    status_var.set(get_gpu_status(instance_id))
    if "ENABLED" in status_var.get():
        toggle_var.set("enable")
    elif "DISABLED" in status_var.get():
        toggle_var.set("disable")

def toggle_gpu():
    selected = selected_gpu.get()
    instance_id = gpu_map.get(selected)
    if not instance_id:
        output_text.set("No GPU selected.")
        return
    choice = toggle_var.get()
    if choice == "enable":
        result = run_powershell(f'Enable-PnpDevice -InstanceId "{instance_id}" -Confirm:$false')
        output_text.set("✅ GPU Enabled!\n\n" + result.stdout + result.stderr)
    elif choice == "disable":
        result = run_powershell(f'Disable-PnpDevice -InstanceId "{instance_id}" -Confirm:$false')
        output_text.set("❌ GPU Disabled!\n\n" + result.stdout + result.stderr)
    refresh_status()

# Init
gpus = get_display_adapters()
gpu_map = {gpu["FriendlyName"]: gpu["InstanceId"] for gpu in gpus}

# GUI Setup
root = tk.Tk()
root.title("Dynamic GPU Toggle Switch")
root.geometry("500x400")

selected_gpu = tk.StringVar()
selected_gpu.set(next(iter(gpu_map), "No GPU Found"))

toggle_var = tk.StringVar()
status_var = tk.StringVar()
output_text = tk.StringVar()

def on_gpu_select(*args):
    refresh_status()

selected_gpu.trace("w", on_gpu_select)

tk.Label(root, text="🖥️ Select Your GPU", font=("Arial", 14)).pack(pady=10)
tk.OptionMenu(root, selected_gpu, *gpu_map.keys()).pack(pady=5)

tk.Label(root, textvariable=status_var, font=("Arial", 14)).pack(pady=5)

# Radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack(pady=10)

tk.Radiobutton(radio_frame, text="✅ Enable GPU", variable=toggle_var, value="enable",
               command=toggle_gpu, bg="green", fg="white", indicatoron=0, width=30).pack(pady=5)

tk.Radiobutton(radio_frame, text="❌ Disable GPU", variable=toggle_var, value="disable",
               command=toggle_gpu, bg="red", fg="white", indicatoron=0, width=30).pack(pady=5)

tk.Button(root, text="🔄 Refresh Status", command=refresh_status, bg="gray", fg="white", width=30).pack(pady=10)
tk.Label(root, textvariable=output_text, wraplength=450, justify="left", font=("Courier", 10)).pack(pady=10)

refresh_status()

root.mainloop()
