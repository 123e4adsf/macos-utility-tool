import os
import sys

print("--- BẮT ĐẦU KIỂM TRA CẤU TRÚC DỰ ÁN ---")

# 1. In đường dẫn thư mục gốc của dự án
project_root = os.path.dirname(os.path.abspath(__file__))
print(f"\n[1] Thư mục gốc của dự án được xác định là:\n    '{project_root}'")

# 2. Kiểm tra sự tồn tại của các tệp và thư mục quan trọng
print("\n[2] Kiểm tra sự tồn tại của các tệp và thư mục cần thiết:")

paths_to_check = {
    "Thư mục 'src'": os.path.join(project_root, 'src'),
    "Tệp '__init__.py' trong 'src'": os.path.join(project_root, 'src', '__init__.py'),
    "Thư mục 'gui' trong 'src'": os.path.join(project_root, 'src', 'gui'),
    "Tệp '__init__.py' trong 'gui'": os.path.join(project_root, 'src', 'gui', '__init__.py'),
    "Tệp 'cua_so_chinh.py' trong 'gui'": os.path.join(project_root, 'src', 'gui', 'cua_so_chinh.py')
}

all_ok = True
for description, path in paths_to_check.items():
    if os.path.exists(path):
        print(f"    [OK]    Tìm thấy: {description}")
    else:
        print(f"    [LỖI]   KHÔNG TÌM THẤY: {description}\n            Đường dẫn đã kiểm tra: {path}")
        all_ok = False

# 3. Kết luận
print("\n--- KẾT THÚC KIỂM TRA ---")
if all_ok:
    print("\n>>> KẾT LUẬN: Cấu trúc thư mục của bạn CHÍNH XÁC. Lỗi có thể đến từ nguyên nhân khác.")
else:
    print("\n>>> KẾT LUẬN: Cấu trúc thư mục của bạn bị SAI. Vui lòng sửa lại các mục báo [LỖI] ở trên.")
    print("    Hãy đảm bảo tên tệp/thư mục được viết chính xác, không có lỗi chính tả hoặc viết hoa/thường sai.")
