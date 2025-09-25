import sys
import os

# Thêm thư mục gốc của src vào path để có thể import từ gui
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gui.cua_so_chinh import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()