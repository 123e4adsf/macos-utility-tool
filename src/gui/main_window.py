# main_window.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
  
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS Utility Tool")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to the macOS Utility Tool", self)
        layout.addWidget(self.label)

        self.gif_button = QPushButton("Create GIF", self)
        self.gif_button.clicked.connect(self.create_gif)
        layout.addWidget(self.gif_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_gif(self):
        # Logic to create GIF will be implemented here
        self.label.setText("GIF creation functionality is not yet implemented.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# (Nội dung tệp này rất dài, tôi sẽ giữ nguyên phiên bản hoàn chỉnh từ lần trả lời trước của mình.
# Nếu bạn chưa cập nhật, hãy sao chép lại từ phản hồi trước đó.)
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.core import commands

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Công cụ tiện ích cho macOS")
        self.geometry("860x600")
        self.configure(bg='#333333')
        self.all_buttons = []
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", padding=8, font=('Helvetica', 10), background="#4F4F4F", foreground="white", borderwidth=0)
        style.map("TButton", background=[('active', '#666666')])
        style.configure("TFrame", background="#333333")
        style.configure("TLabel", background="#333333", foreground="white")
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(main_frame, textvariable=search_var, font=("Helvetica", 11))
        search_entry.pack(fill="x", padx=4, pady=(0, 10))
        search_var.trace_add('write', lambda *_: self.filter_buttons(search_var.get()))
        
        columns_frame = ttk.Frame(main_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)

        sections = {
            "📁 File & Folder": [("Hiện file ẩn", commands.show_hidden), ("Ẩn file ẩn", commands.hide_hidden), ("Liệt kê Desktop", commands.list_desktop)],
            "🎮 GPU": [("Dùng GPU rời", commands.use_discrete_gpu), ("Dùng GPU tích hợp", commands.use_integrated_gpu), ("GPU tự động", commands.use_auto_gpu), ("Kiểm tra GPU", commands.check_gpu)],
            "🧠 RAM & Hệ thống": [("Dọn RAM", commands.purge_ram), ("Xem uptime", commands.check_uptime), ("Xem tiến trình", commands.check_processes), ("Kiểm tra pin", commands.check_battery), ("Tốc độ mạng", commands.network_speed), ("Thông tin máy", commands.system_info), ("Phiên bản macOS", commands.check_mac_version)],
            "📷 Ảnh màn hình": [("Lưu ảnh về Desktop", commands.set_screenshot_location), ("Định dạng JPG", commands.set_screenshot_format_jpg), ("Tắt âm chụp ảnh", commands.disable_screenshot_sound)],
            "🖥️ Dock": [("Tự ẩn Dock", commands.dock_autohide_on), ("Hiện Dock cố định", commands.dock_autohide_off), ("Khôi phục Dock", commands.dock_reset)],
            "📡 Wi-Fi & Bluetooth": [("Bật Wi-Fi", commands.wifi_on), ("Tắt Wi-Fi", commands.wifi_off), ("Quét Wi-Fi", commands.wifi_scan), ("Bật Bluetooth", commands.bluetooth_on), ("Tắt Bluetooth", commands.bluetooth_off)],
            "🔊 Âm lượng & Web": [("Tăng âm lượng", commands.volume_up), ("Giảm âm lượng", commands.volume_down), ("Mở Google", commands.open_google)],
            "🛠️ Công cụ Dự án": [
                ("Tạo Môi trường ảo", commands.create_virtual_environment),
                ("Cấu hình VS Code", commands.setup_vscode_project),
                ("Gợi ý Extensions", commands.show_recommended_extensions)
            ]
        }

        num_columns = 4
        columns = [ttk.Frame(columns_frame) for _ in range(num_columns)]
        for i, col in enumerate(columns):
            columns_frame.columnconfigure(i, weight=1)
            col.grid(row=0, column=i, sticky="nsew", padx=5)
        
        for i, (title, actions) in enumerate(sections.items()):
            col_index = i % num_columns
            self.add_section(columns[col_index], title, actions)

    def add_section(self, parent, title, actions):
        frame = ttk.Frame(parent, padding=5)
        frame.pack(fill="x", pady=5)
        ttk.Label(frame, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        for name, func in actions:
            def action_wrapper(f=func, n=name): self.run_action_thread(f, n)
            btn = ttk.Button(frame, text=name, command=action_wrapper)
            btn.pack(fill="x", pady=2)
            btn.action_name = name
            self.all_buttons.append(btn)

    def run_action_thread(self, func, name):
        def target():
            print(f"Đang thực thi: {name}...")
            result = func()
            print(f"Kết quả: {result}")
            self.after(0, lambda: messagebox.showinfo(f"Kết quả: {name}", result or "Hoàn thành!"))
        threading.Thread(target=target, daemon=True).start()

    def filter_buttons(self, keyword):
        keyword = keyword.lower().strip()
        for btn in self.all_buttons:
            if keyword in btn.action_name.lower():
                btn.pack(fill="x", pady=2)
            else:
                btn.pack_forget()

def main():
    app = MainApplication()
    app.mainloop()