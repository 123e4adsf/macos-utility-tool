import tkinter as tk
from tkinter import ttk
import subprocess

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Trợ lý Terminal cho MacBook")
        self.geometry("400x230")
        self.configure(bg='#333333')
        self.resizable(False, False)

        style = ttk.Style(self)
        style.configure("TFrame", background="#333333")
        style.configure("TLabel", background="#333333", foreground="white", font=("Helvetica", 14, "bold"))
        style.configure("TButton", font=("Helvetica", 12), background="#4F4F4F", foreground="white", borderwidth=0, padding=10)
        style.map("TButton", background=[('active', '#666666')])

        main_frame = ttk.Frame(self, padding="20 15")
        main_frame.pack(fill="x", expand=True)

        gpu_label = ttk.Label(main_frame, text="🎮 GPU")
        gpu_label.pack(anchor="w", pady=(0, 5))

        ttk.Button(main_frame, text="Dùng GPU rời", command=self.use_discrete_gpu).pack(fill='x', pady=4)
        ttk.Button(main_frame, text="Dùng GPU tích hợp", command=self.use_integrated_gpu).pack(fill='x', pady=4)
        ttk.Button(main_frame, text="GPU chế độ tự động", command=self.use_auto_gpu).pack(fill='x', pady=4)
        ttk.Button(main_frame, text="Kiểm tra GPU", command=self.check_gpu).pack(fill='x', pady=4)

    def run_command_with_admin(self, command):
        print(f"Yêu cầu quyền quản trị để chạy: {command}")
        try:
            script = f'do shell script "{command}" with administrator privileges'
            subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
            print("Lệnh đã được thực thi thành công.")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode().strip()
            if "User canceled" in error_message:
                print("Người dùng đã hủy thao tác.")
            else:
                print(f"Lỗi khi thực thi: {error_message}")
        except FileNotFoundError:
            print("Lỗi: Lệnh 'osascript' không tìm thấy.")

    def use_discrete_gpu(self):
        self.run_command_with_admin("pmset -a gpuswitch 1")

    def use_integrated_gpu(self):
        self.run_command_with_admin("pmset -a gpuswitch 0")

    def use_auto_gpu(self):
        self.run_command_with_admin("pmset -a gpuswitch 2")

    def check_gpu(self):
        print("Đang kiểm tra trạng thái GPU...")
        try:
            result = subprocess.run("pmset -g | grep gpuswitch", shell=True, capture_output=True, text=True)
            print(result.stdout.strip())
        except Exception as e:
            print(f"Không thể kiểm tra GPU: {e}")

# Tệp này chỉ nên chứa mã Python ở trên. Mọi nội dung khác đã được xóa.