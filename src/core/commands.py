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