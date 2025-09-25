import os

# ======= CẤU HÌNH THƯ MỤC =======
folders = [
    ".vscode",
    "docs",
    "scripts",
    "utils",
    "src/core"
]

files_content = {
    # VS CODE CONFIG FILES
    ".vscode/settings.json": """{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.analysis.typeCheckingMode": "basic",
    "files.exclude": {
        "**/__pycache__": true,
        "**/.git": true,
        "**/.venv": true,
        "**/node_modules": true,
        "**/dist": true,
        "**/build": true
    },
    "editor.tabSize": 4,
    "editor.rulers": [80, 120],
    "editor.wordWrap": "on",
    "editor.minimap.enabled": true,
    "python.terminal.activateEnvironment": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.analysis.completeFunctionParens": true,
    "workbench.colorTheme": "Default Dark+",
    "workbench.iconTheme": "material-icon-theme",
    "python.analysis.memory.keepLibraryAst": true,
    "python.analysis.memory.keepLibrarySymbols": true
}""",

    ".vscode/launch.json": """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run App (Main GUI)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/core/app.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Run Export Script",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/scripts/runcom.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Debug Specific File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}""",

    ".vscode/tasks.json": """{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Export Video",
            "type": "shell",
            "command": "python scripts/runcom.py",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": []
        },
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "pip install -r requirements.txt",
            "problemMatcher": []
        },
        {
            "label": "Clean Cache",
            "type": "shell",
            "command": "find . -type d -name '__pycache__' -exec rm -rf {} +",
            "problemMatcher": []
        }
    ]
}""",

    # REQUIREMENTS
    "requirements.txt": """# Core Python Libraries
numpy
Pillow
opencv-python
ffmpeg-python

# GUI
# tkinter is a built-in library, no need to list it here.
PyQt5

# AI/ML
torch
torchvision
scikit-learn
mediapipe

# Utilities
tqdm
requests

# Dev Tools
pytest
black
autopep8
""",

    # README
    "docs/README.md": """# Video Editor Project

Dự án chỉnh sửa video với các tính năng:
- Cắt / nối clip
- Filter & AI smoothing
- Transition
- Export video
- GUI bằng Tkinter hoặc PyQt

## Cấu trúc thư mục

## Hướng dẫn cài đặt

1.  Tạo môi trường ảo:
    ```bash
    python -m venv venv
    ```

2.  Kích hoạt môi trường ảo:
    -   Windows: `venv\\Scripts\\activate`
    -   macOS/Linux: `source venv/bin/activate`

3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

## Cách chạy

- Mở project bằng VS Code.
- Chạy cấu hình "Run App (Main GUI)" từ tab "Run and Debug" (hoặc nhấn F5).
""",
}

def create_project_structure():
    """Tạo các thư mục và tệp dựa trên cấu hình ở trên."""
    print("Bắt đầu tạo cấu trúc dự án...")

    # Tạo thư mục
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"  [OK] Đã tạo thư mục: {folder}")
        except OSError as e:
            print(f"  [LỖI] Không thể tạo thư mục {folder}: {e}")

    # Tạo tệp
    for file_path, content in files_content.items():
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Đã tạo tệp: {file_path}")
        except IOError as e:
            print(f"  [LỖI] Không thể tạo tệp {file_path}: {e}")

    print("\nHoàn thành!")

if __name__ == "__main__":
    # Chạy hàm để tạo dự án
    # create_project_structure()
    print("Tệp này dùng để tạo cấu trúc cho một dự án mới.")
    print("Để sử dụng, hãy bỏ bình luận dòng 'create_project_structure()' và chạy lại.")
