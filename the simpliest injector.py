import tkinter as tk
from tkinter import filedialog
import psutil
import os
import sys
import platform

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info = proc.info
            processes.append((info['pid'], info['name']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def select_process(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        picked = widget.get(selection[0])
        process_id, _ = picked.split(" - ")
        process_id_entry.delete(0, tk.END)
        process_id_entry.insert(0, process_id)

def select_dll():
    dll_path = filedialog.askopenfilename(title="Select DLL/SO file", filetypes=[("DLL/SO files", "*.dll *.so")])
    if dll_path:
        if platform.system() == "Linux":
            inject_dll_linux_ldpreload(dll_path, int(process_id_entry.get()))

def inject_dll_linux_ldpreload(so_path, process_id):
    try:
        os.environ['LD_PRELOAD'] = so_path

        exe_path = '/proc/{}/exe'.format(process_id)

        os.execl(exe_path, exe_path)
    except Exception as e:
        print(f"Error injecting DLL: {e}")

root = tk.Tk()
root.title("Simpliest DLL Injector")

processes = get_running_processes()

process_id_label = tk.Label(root, text="Process ID:")
process_id_label.pack()

process_id_entry = tk.Entry(root, width=20)
process_id_entry.pack()

process_list_label = tk.Label(root, text="Running Processes:")
process_list_label.pack()

process_list = tk.Listbox(root, width=40, height=10)
process_list.pack()
for pid, name in processes:
    process_list.insert(tk.END, f"{pid} - {name}")
process_list.bind("<<ListboxSelect>>", select_process)

platform_label = tk.Label(root, text="Platform:")
platform_label.pack()

platform_var = tk.StringVar(root)
platform_var.set("Linux")

platform_options = ["Linux"]
platform_menu = tk.OptionMenu(root, platform_var, *platform_options)
platform_menu.pack()

injection_method_label = tk.Label(root, text="Injection Method:")
injection_method_label.pack()

injection_method_var = tk.StringVar(root)
injection_method_var.set("LD_PRELOAD")

injection_method_options = ["LD_PRELOAD"]
injection_method_menu = tk.OptionMenu(root, injection_method_var, *injection_method_options)
injection_method_menu.pack()

select_dll_button = tk.Button(root, text="Select DLL/SO file", command=select_dll)
select_dll_button.pack()

root.mainloop()