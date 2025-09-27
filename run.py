import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.gui.main_window import main as start_gui

    start_gui()
except ImportError as e:
    print("LỖI: Không thể khởi chạy ứng dụng. Có vẻ cấu trúc dự án bị sai.")
    print("Hãy thử chạy lệnh sau để tự động cài đặt và sửa lỗi:")
    print("   python3 setup.py")
    print(f"\nChi tiết lỗi: {e}")
    sys.exit(1)
