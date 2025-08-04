<p align="center">
  <img src="gamer.ico" alt="app  Logo" width="200" >
</p>



# ⚙️ GPU Toggle Utility

A sleek, one-click tool to **enable or disable your GPU** with a clean GUI and smart tray support.  
Perfect for laptops with **iGPU + dGPU**, especially when Windows won’t stop sipping your battery like a Capri Sun.


🆕 [**Download Latest Release (.exe)**](https://github.com/jztchl/gpu_switch/releases)  
---

## 🚀 Features

- 🔘 **One-click GPU Enable/Disable**
- 🖥️ **Minimal GUI** built with `tkinter`
- 🧲 **System Tray Integration** (via `pystray`) – app minimizes to tray!
- 🔒 **Auto Admin Elevation** (UAC prompt on launch)
- 🧿 **Custom App Icon**
- 📦 **One-file Executable** using PyInstaller (~20MB)

---

## 💻 Real-World Use Case: Laptops with iGPU + dGPU

For laptops without a MUX switch, **Windows often keeps the dGPU active**, tanking your battery even when you’re just watching YouTube.  
Use this app to:

✅ **Disable dGPU** during light tasks to save power  
✅ **Re-enable** it when gaming, editing, or running heavy stuff  
⚠️ **Never disable all GPUs** — unless you want to embrace darkness (literally)

---

## 🛠 Tech Stack

- **Language**: Python 3.x  
- **GUI**: `tkinter`  
- **Tray**: `pystray`  
- **Command Execution**: `subprocess` with PowerShell  
- **Bundler**: PyInstaller  
- **Icon Format**: `.ico`

---

## 🧪 Known Issues
 
- Brief **PowerShell flash** during toggling is normal  
- **Windows only** (requires PnP and GPU instance IDs)  
- ⚠️ App does **not prevent disabling all GPUs** – be careful!

---

## 🧾 How to Use

1. **Run `GPU_Toggle.exe` as administrator**
2. Use the GUI to **enable or disable** the GPU
3. Minimize to tray anytime — right-click tray icon for Exit

To build a standalone `.exe` file from `gpu_toggle.py`, run:
```bash
 pyinstaller --onefile --windowed --icon=gamer.ico  --add-data "gamer.ico;." gpu_toggle.py
 ``` 

🪄 *Powershell will handle device control under the hood. Expect a short blue flash.*

---

## 💡 Planned Features

- 🛡️ **Failsafe logic** to prevent disabling all GPUs
- 🔋 **Battery-aware toggling**

---


## 🧠 Author

Built by [**jztchl**](https://github.com/jztchl)

---

## 🖤 License

**MIT License**  
Do whatever you want. Break it. Improve it. Ship it.  
Just don’t come crying if you blackscreen your whole system.

---

