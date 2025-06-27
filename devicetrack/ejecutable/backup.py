import subprocess
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

        # Rutas ABSOLUTAS que debes cambiar según tu PC:
        self.venv_python = r"C:\Users\jarot\PycharmProjects\DeviceTrack\.venv\Scripts\activate.bat"
        self.manage_py_dir = r"C:\Users\jarot\PycharmProjects\DeviceTrack\devicetrack"

    def get_local_ip(self):
        return "127.0.0.1"

    def open_browser(self, event=None):
        if self.running:
            ip = self.get_local_ip()
            webbrowser.open(f"http://{ip}:{self.port}")

    def toggle_server(self):
        if not self.running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        self.console.insert(tk.END, "Iniciando servidor...\n")
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
