import os

def create_project_structure(base_path):
    """Tạo cấu trúc dự án Video Editor tại một đường dẫn được chỉ định."""
    
    folders = [
        ".vscode", "docs", "scripts", "utils", "src/core", "src/gui"
    ]

    files_content = {
        ".vscode/settings.json": """{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}""",
        ".vscode/launch.json": """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/core/app.py"
        }
    ]
}""",
        "requirements.txt": """# Core Libraries
numpy
Pillow
opencv-python
ffmpeg-python

# GUI
PyQt5

# Dev Tools
pytest
black
""",
        "docs/README.md": """# Video Editor Project
Dự án được tạo tự động.
""",
        "src/core/app.py": """print("Hello from the new Video Editor project!")""",
        "src/gui/main_window.py": """# Tệp định nghĩa giao diện chính
from PyQt5 import QtWidgets
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Editor')
        self.setGeometry(100, 100, 800, 600)

def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
""",
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class

# Environment
.venv
venv/
ENV/
"""
    }

    print(f"Bắt đầu tạo dự án tại: {base_path}")
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for folder in folders:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"  Đã tạo thư mục: {full_path}")

    for file_path, content in files_content.items():
        full_path = os.path.join(base_path, file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Đã tạo tệp: {full_path}")
    
    print("\nHoàn thành tạo dự án!")
