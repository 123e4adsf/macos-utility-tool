import subprocess

# --- Hàm cơ bản ---
def run_command(command):
    """Thực thi một lệnh shell và trả về kết quả."""
    try:
        # Chạy lệnh và chờ hoàn thành, lấy output
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Nếu lệnh trả về lỗi, trả về thông báo lỗi đó
        return e.stderr.strip() or f"Lệnh thất bại với mã lỗi {e.returncode}"
    except Exception as e:
        return f"Lỗi không xác định: {e}"

def run_command_with_admin(command):
    """Thực thi lệnh yêu cầu quyền quản trị (sudo)."""
    script = f'do shell script "{command}" with administrator privileges'
    return run_command(f"osascript -e '{script}'")

# --- Định nghĩa tất cả các chức năng ---

# File & Folder
show_hidden = lambda: run_command("defaults write com.apple.finder AppleShowAllFiles TRUE && killall Finder")
hide_hidden = lambda: run_command("defaults write com.apple.finder AppleShowAllFiles FALSE && killall Finder")
list_desktop = lambda: run_command("ls -la ~/Desktop")

# GPU
use_discrete_gpu = lambda: run_command_with_admin("pmset -a gpuswitch 1")
use_integrated_gpu = lambda: run_command_with_admin("pmset -a gpuswitch 0")
use_auto_gpu = lambda: run_command_with_admin("pmset -a gpuswitch 2")
check_gpu = lambda: run_command("system_profiler SPDisplaysDataType")

# RAM & System
purge_ram = lambda: run_command_with_admin("purge")
check_uptime = lambda: run_command("uptime")
check_processes = lambda: run_command("top -l 1 -o cpu -n 10") # Lấy 10 tiến trình top
check_battery = lambda: run_command("pmset -g batt")
network_speed = lambda: run_command("networkQuality")
system_info = lambda: run_command("system_profiler SPHardwareDataType")
check_mac_version = lambda: run_command("sw_vers")

# Screenshot
set_screenshot_location = lambda: run_command("defaults write com.apple.screencapture location ~/Desktop && killall SystemUIServer")
set_screenshot_format_jpg = lambda: run_command("defaults write com.apple.screencapture type jpg && killall SystemUIServer")
disable_screenshot_sound = lambda: run_command("defaults write com.apple.screencapture disable-shadow -bool true && killall SystemUIServer")

# Dock
dock_autohide_on = lambda: run_command("defaults write com.apple.dock autohide -bool true && killall Dock")
dock_autohide_off = lambda: run_command("defaults write com.apple.dock autohide -bool false && killall Dock")
dock_reset = lambda: run_command("defaults delete com.apple.dock && killall Dock")

# Wi-Fi & Bluetooth
wifi_on = lambda: run_command("networksetup -setairportpower en0 on")
wifi_off = lambda: run_command("networksetup -setairportpower en0 off")
wifi_scan = lambda: run_command("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s")
bluetooth_on = lambda: run_command("blueutil --power 1") # Cần cài: brew install blueutil
bluetooth_off = lambda: run_command("blueutil --power 0") # Cần cài: brew install blueutil

# Volume & Web
volume_up = lambda: run_command("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
volume_down = lambda: run_command("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
open_google = lambda: run_command("open https://www.google.com")

# --- Chức năng mới: Công cụ dự án ---
def create_virtual_environment():
    """Tạo môi trường ảo Python (venv) trong thư mục hiện tại."""
    import sys
    import os
    
    venv_path = os.path.join(os.getcwd(), "venv")
    if os.path.exists(venv_path):
        return "✅ Môi trường ảo 'venv' đã tồn tại."

    # Dùng sys.executable để đảm bảo dùng đúng phiên bản python đang chạy script
    command_str = f'"{sys.executable}" -m venv venv'
    result = run_command(command_str)
    
    # Kiểm tra kết quả
    if "Lỗi" in result:
        return f"❌ Không thể tạo môi trường ảo.\n\nChi tiết lỗi:\n{result}"
    else:
        return (
            "✅ Đã tạo thành công môi trường ảo 'venv'.\n\n"
            "Để kích hoạt, hãy mở Terminal và chạy lệnh:\n"
            "source venv/bin/activate"
        )

def install_dependencies():
    """Cài đặt các thư viện từ requirements.txt sử dụng môi trường ảo nếu có."""
    import sys
    import os
    
    # Ưu tiên dùng python trong venv nếu có, nếu không thì dùng python đang chạy script
    python_executable = sys.executable
    project_root = os.getcwd()
    venv_python = os.path.join(project_root, "venv", "bin", "python")

    if os.path.exists(venv_python):
        python_executable = venv_python
    
    command_str = f'"{python_executable}" -m pip install -r requirements.txt'
    result = run_command(command_str)

    if "Lỗi" not in result and "error" not in result.lower():
        return f"✅ Đã cài đặt/cập nhật thành công các thư viện."
    else:
        return f"❌ Có lỗi xảy ra trong quá trình cài đặt.\n\nChi tiết:\n{result}"

def show_recommended_extensions():
    """Trả về danh sách các extension VS Code được đề xuất."""
    return """Các extension VS Code được đề xuất cho lập trình Python:

• Python (ms-python.python):
  Hỗ trợ debug, chạy code, linting.

• Pylance (ms-python.pylance):
  Gợi ý code thông minh (IntelliSense).

• Black Formatter (ms-python.black-formatter):
  Tự động format code theo chuẩn Black.

• GitLens (eamodio.gitlens):
  Tích hợp Git sâu hơn, xem lịch sử từng dòng code.

• Material Icon Theme (PKief.material-icon-theme):
  Bộ icon đẹp cho các loại tệp, dễ phân biệt.

• Better Comments (aaron-bond.better-comments):
  Làm nổi bật các loại chú thích khác nhau bằng màu sắc.

• Live Share (ms-vsliveshare.vsliveshare):
  Lập trình chung với người khác trong thời gian thực.
"""

def install_vscode_extensions():
    """Tự động cài đặt các extension VS Code được đề xuất."""
    import shutil
    
    # Kiểm tra xem lệnh 'code' của VS Code có tồn tại không
    if not shutil.which("code"):
        return (
            "❌ LỖI: Lệnh 'code' không tìm thấy.\n\n"
            "Để sửa lỗi này, hãy:\n"
            "1. Mở Visual Studio Code.\n"
            "2. Nhấn Command+Shift+P.\n"
            "3. Gõ 'Shell Command' và chọn 'Install \\'code\\' command in PATH'.\n"
            "4. Khởi động lại Terminal và thử lại."
        )

    extensions = [
        "ms-python.python",           # Python
        "ms-python.pylance",          # Pylance
        "ms-python.black-formatter",  # Black Formatter
        "eamodio.gitlens",            # GitLens
        "PKief.material-icon-theme",  # Material Icon Theme
        "aaron-bond.better-comments", # Better Comments
        "ms-vsliveshare.vsliveshare"  # Live Share
    ]
    
    command_parts = ["code"]
    for ext in extensions:
        command_parts.extend(["--install-extension", ext])
    
    # Chạy lệnh trong một chuỗi duy nhất để cài đặt tất cả
    result = run_command(" ".join(command_parts))
    
    if "successfully" in result.lower():
        return "✅ Đã cài đặt thành công các extension được đề xuất!"
    else:
        return f"🟡 Có thể đã xảy ra lỗi trong quá trình cài đặt.\n\nChi tiết:\n{result}"

def setup_vscode_project():
    """Tạo các tệp cấu hình VS Code tối ưu cho dự án Python hiện tại."""
    import os
    project_root = os.getcwd()
    vscode_dir = os.path.join(project_root, ".vscode")

    files_to_create = {
        # Tệp cài đặt chính cho VS Code
        "settings.json": """{
    // --- Cấu hình cho Python ---
    // Tự động trỏ đến môi trường ảo (venv) của dự án
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    // Tự động kích hoạt môi trường ảo khi mở Terminal
    "python.terminal.activateEnvironment": true,

    // --- Tự động Format Code ---
    // Sử dụng 'black' để format code
    "python.formatting.provider": "black",
    // Tự động format khi lưu tệp
    "editor.formatOnSave": true,

    // --- Kiểm tra lỗi (Linting) ---
    // Bật tính năng kiểm tra lỗi
    "python.linting.enabled": true,
    // Sử dụng 'pylint' để kiểm tra
    "python.linting.pylintEnabled": true,

    // --- Giao diện và hiệu suất ---
    // Ẩn các tệp/thư mục không cần thiết khỏi cây thư mục
    "files.exclude": {
        "**/__pycache__": true,
        "**/.git": true,
        "**/.venv": true,
        "venv": true,
        "**/node_modules": true,
        "**/dist": true,
        "**/build": true
    },
    "editor.rulers": [88] // Thêm một đường kẻ ở cột 88 để giới hạn độ dài dòng
}""",

        # Tệp cấu hình để Chạy và Gỡ lỗi (Debug)
        "launch.json": """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run: Main App (run.py)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Debug: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}""",

        # Tệp cấu hình các tác vụ tự động
        "tasks.json": """{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Install/Update Dependencies",
            "type": "shell",
            // Dùng đúng trình thông dịch python của venv để cài đặt
            "command": "${command:python.interpreterPath} -m pip install -r requirements.txt",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Clean Cache",
            "type": "shell",
            "command": "find . -path '*/__pycache__*' -delete && find . -name '*.pyc' -delete",
            "problemMatcher": []
        }
    ]
}"""
    }

    try:
        os.makedirs(vscode_dir, exist_ok=True)
        for filename, content in files_to_create.items():
            file_path = os.path.join(vscode_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return f"Đã tạo thành công bộ cấu hình VS Code tối ưu trong thư mục:\\n{vscode_dir}"
    except Exception as e:
        return f"Lỗi khi tạo tệp cấu hình: {e}"

# --- Giao diện người dùng: Menu chính ---
def main_menu():
    """Hiển thị menu chính và xử lý lựa chọn của người dùng."""
    import os

    while True:
        # Xóa màn hình terminal
        os.system("clear" if os.name == "posix" else "cls")

        print("🏠 Menu Chính - Công cụ Tối ưu Hóa MacOS & Dự án Python")
        print("Chọn một tùy chọn để tiếp tục:")
        print("1. 🚀 Tối ưu hóa MacOS")
        print("2. 🛠️ Công cụ Dự án")
        print("3. 📦 Cài đặt Thư viện")
        print("4. ⚙️ Cài đặt VS Code")
        print("0. ❌ Thoát")

        choice = input("\nNhập số tùy chọn của bạn: ")

        if choice == "1":
            optimize_macos_menu()
        elif choice == "2":
            project_tools_menu()
        elif choice == "3":
            install_dependencies()
        elif choice == "4":
            setup_vscode_project()
        elif choice == "0":
            print("Cảm ơn bạn đã sử dụng công cụ này. Hẹn gặp lại!")
            break
        else:
            input("Lựa chọn không hợp lệ. Nhấn Enter để tiếp tục...")

# --- Tối ưu hóa MacOS ---
def optimize_macos_menu():
    """Menu con để tối ưu hóa MacOS."""
    import os

    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("🍏 Tối ưu hóa MacOS")
        print("Chọn một tùy chọn để tiếp tục:")
        print("1. Hiện/Ẩn tệp ẩn")
        print("2. Đặt lại Dock về mặc định")
        print("3. Tắt âm thanh chụp màn hình")
        print("4. Kiểm tra GPU")
        print("5. Chuyển đổi GPU rời/không rời")
        print("6. Xóa bộ nhớ RAM cache")
        print("7. Kiểm tra thời gian hoạt động")
        print("8. Kiểm tra tiến trình đang chạy")
        print("9. Kiểm tra thông tin pin")
        print("10. Kiểm tra tốc độ mạng")
        print("11. Kiểm tra thông tin hệ thống")
        print("12. Kiểm tra phiên bản MacOS")
        print("0. Quay lại menu chính")

        choice = input("\nNhập số tùy chọn của bạn: ")

        if choice == "1":
            toggle_show_hidden_files()
        elif choice == "2":
            reset_dock()
        elif choice == "3":
            toggle_screenshot_sound()
        elif choice == "4":
            check_gpu()
        elif choice == "5":
            switch_gpu()
        elif choice == "6":
            purge_ram()
        elif choice == "7":
            check_uptime()
        elif choice == "8":
            check_processes()
        elif choice == "9":
            check_battery()
        elif choice == "10":
            network_speed()
        elif choice == "11":
            system_info()
        elif choice == "12":
            check_mac_version()
        elif choice == "0":
            break
        else:
            input("Lựa chọn không hợp lệ. Nhấn Enter để tiếp tục...")

def toggle_show_hidden_files():
    """Chuyển đổi giữa việc hiện và ẩn các tệp ẩn trong Finder."""
    current_setting = run_command("defaults read com.apple.finder AppleShowAllFiles")
    
    if current_setting == "1":
        hide_hidden()
        print("✅ Đã ẩn các tệp ẩn.")
    else:
        show_hidden()
        print("✅ Đã hiện các tệp ẩn.")

    input("Nhấn Enter để tiếp tục...")

def reset_dock():
    """Đặt lại Dock về cài đặt mặc định."""
    dock_reset()
    print("✅ Đã đặt lại Dock về cài đặt mặc định.")
    input("Nhấn Enter để tiếp tục...")

def toggle_screenshot_sound():
    """Bật hoặc tắt âm thanh chụp màn hình."""
    current_setting = run_command("defaults read com.apple.screencapture disable-shadow")
    
    if current_setting == "1":
        disable_screenshot_sound()
        print("✅ Đã tắt âm thanh chụp màn hình.")
    else:
        run_command("defaults write com.apple.screencapture disable-shadow -bool false && killall SystemUIServer")
        print("✅ Đã bật âm thanh chụp màn hình.")

    input("Nhấn Enter để tiếp tục...")

def switch_gpu():
    """Chuyển đổi giữa GPU rời và không rời (nếu có nhiều GPU)."""
    current_gpu = run_command("pmset -g | grep 'Graphics'")

    if "Integrated" in current_gpu:
        use_discrete_gpu()
        print("✅ Đã chuyển sang sử dụng GPU rời.")
    else:
        use_integrated_gpu()
        print("✅ Đã chuyển sang sử dụng GPU không rời.")

    input("Nhấn Enter để tiếp tục...")

# --- Công cụ Dự án ---
def project_tools_menu():
    """Menu con cho các công cụ dự án."""
    import os

    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("🛠️ Công cụ Dự án")
        print("Chọn một tùy chọn để tiếp tục:")
        print("1. Tạo Môi trường ảo")
        print("2. Cài đặt Dependencies")
        print("3. Cấu hình VS Code")
        print("4. Gợi ý Extensions")
        print("5. Cài Extensions Đề xuất")
        print("0. Quay lại menu chính")

        choice = input("\nNhập số tùy chọn của bạn: ")

        if choice == "1":
            print(create_virtual_environment())
        elif choice == "2":
            print(install_dependencies())
        elif choice == "3":
            print(setup_vscode_project())
        elif choice == "4":
            print(show_recommended_extensions())
            input("Nhấn Enter để tiếp tục...")
        elif choice == "5":
            print(install_vscode_extensions())
        elif choice == "0":
            break
        else:
            input("Lựa chọn không hợp lệ. Nhấn Enter để tiếp tục...")

# Khởi động chương trình
main_menu()