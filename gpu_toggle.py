import tkinter as tk
import subprocess

GPU_INSTANCE_ID = r"PCI\VEN_8086&DEV_5693&SUBSYS_138F1462&REV_05\6&2EA43C3F&0&00080008"

def run_powershell(command):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True, text=True
    )
    return result

def get_gpu_status(instance_id):
    try:
        result = run_powershell(f"(Get-PnpDevice -InstanceId '{instance_id}').Status")
        code = result.stdout.strip()
        if code == "OK":
            return "ENABLED ✅"
        else:
           return "DISABLED ❌"
    except Exception as e:
        return f"ERROR: {e}"

def refresh_status():
    status_var.set(get_gpu_status(GPU_INSTANCE_ID))

def disable_gpu():
    result = run_powershell(f'Disable-PnpDevice -InstanceId "{GPU_INSTANCE_ID}" -Confirm:$false')
    output_text.set("❌ GPU Disabled!\n\n" + result.stdout + result.stderr)
    refresh_status()

def enable_gpu():
    result = run_powershell(f'Enable-PnpDevice -InstanceId "{GPU_INSTANCE_ID}" -Confirm:$false')
    output_text.set("✅ GPU Enabled!\n\n" + result.stdout + result.stderr)
    refresh_status()

# GUI Setup
root = tk.Tk()
root.title("GPU Toggle Switch")
root.geometry("450x350")

status_var = tk.StringVar()
status_var.set(get_gpu_status(GPU_INSTANCE_ID))

tk.Label(root, text="Intel Arc A370M Status", font=("Arial", 16)).pack(pady=10)
tk.Label(root, textvariable=status_var, font=("Arial", 16)).pack(pady=5)

tk.Button(root, text="❌ Disable GPU", command=disable_gpu, bg="red", fg="white", width=30).pack(pady=10)
tk.Button(root, text="✅ Enable GPU", command=enable_gpu, bg="green", fg="white", width=30).pack(pady=10)
tk.Button(root, text="🔄 Refresh Status", command=refresh_status, bg="gray", fg="white", width=30).pack(pady=10)

output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, wraplength=400, justify="left", font=("Courier", 10)).pack(pady=10)

root.mainloop()
