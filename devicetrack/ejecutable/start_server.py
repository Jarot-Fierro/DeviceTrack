import os
import subprocess
import sys
import threading
import time
import tkinter as tk
import webbrowser


class ServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de Servidor Django")
        self.master.geometry("750x500")

        self.server_process = None
        self.running = False
        self.start_time = None

        if getattr(sys, 'frozen', False):
            exe_path = os.path.dirname(sys.executable)
            project_root = os.path.abspath(os.path.join(exe_path, "..", ".."))  # ← Devicetrack/devicetrack/
        else:
            current_path = os.path.abspath(__file__)
            project_root = os.path.abspath(os.path.join(current_path, "..", ".."))  # ← también Devicetrack/devicetrack/

        self.manage_py_dir = project_root
        self.venv_python = os.path.abspath(os.path.join(project_root, "..", ".venv", "Scripts", "python.exe"))

        manage_py_dir = project_root  # porque ahí está manage.py
        venv_python = os.path.abspath(os.path.join(project_root, ".venv", "Scripts", "python.exe"))

        print("project_root:", project_root)
        print("manage_py_dir:", manage_py_dir)
        print("venv_python:", venv_python)

        # Ícono (en exe también)
        ico_name = "django.ico"
        if getattr(sys, 'frozen', False):
            ico_path = os.path.join(sys._MEIPASS, ico_name)
        else:
            ico_path = os.path.join(os.path.dirname(__file__), ico_name)

        try:
            self.master.iconbitmap(ico_path)
        except Exception as e:
            print(f"[WARNING] No se pudo asignar ícono: {e}")

        # Widgets
        self.btn_toggle = tk.Button(master, text="Iniciar Servidor", command=self.toggle_server, width=20, bg='green',
                                    fg='white')
        self.btn_toggle.pack(pady=10)

        self.btn_open_browser = tk.Button(master, text="Abrir Navegador", command=self.open_browser, state='disabled')
        self.btn_open_browser.pack(pady=5)

        self.server_info = tk.Label(master, text="", fg="blue", cursor="hand2")
        self.server_info.pack()
        self.server_info.bind("<Button-1>", self.open_browser)

        self.console = tk.Text(master, height=20, bg='black', fg='white')
        self.console.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(master, text="Estado: Detenido", fg='red')
        self.status_label.pack(pady=5)

        self.time_label = tk.Label(master, text="Tiempo de ejecución: 0s")
        self.time_label.pack(pady=5)

        self.port = 8000

    def get_local_ip(self):
        return "127.0.0.1"

    def open_browser(self, event=None):
        if self.running:
            webbrowser.open(f"http://{self.get_local_ip()}:{self.port}")

    def toggle_server(self):
        if not self.running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        self.console.insert(tk.END, "Iniciando servidor...\n")
        self.console.insert(tk.END, f"Usando: {self.venv_python}\n")
        self.console.insert(tk.END, f"En directorio: {self.manage_py_dir}\n")
        self.console.see(tk.END)

        self.server_process = subprocess.Popen(
            [self.venv_python, "manage.py", "runserver", f"{self.get_local_ip()}:{self.port}"],
            cwd=self.manage_py_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        self.running = True
        self.start_time = time.time()
        self.btn_toggle.config(text="Detener Servidor", bg='red')
        self.btn_open_browser.config(state='normal')
        self.server_info.config(text=f"http://{self.get_local_ip()}:{self.port}")
        self.status_label.config(text="Estado: En ejecución", fg='green')

        threading.Thread(target=self.read_output, daemon=True).start()
        self.update_time()

    def stop_server(self):
        if self.server_process:
            self.console.insert(tk.END, "Deteniendo servidor...\n")
            self.console.see(tk.END)
            self.server_process.terminate()
            self.server_process = None
            self.running = False
            self.btn_toggle.config(text="Iniciar Servidor", bg='green')
            self.btn_open_browser.config(state='disabled')
            self.server_info.config(text="")
            self.status_label.config(text="Estado: Detenido", fg='red')

    def read_output(self):
        if self.server_process.stdout:
            for line in self.server_process.stdout:
                self.console.insert(tk.END, line)
                self.console.see(tk.END)

    def update_time(self):
        if self.running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Tiempo de ejecución: {elapsed}s")
            self.master.after(1000, self.update_time)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
