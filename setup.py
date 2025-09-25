import subprocess
import sys
import shutil

def run_command(command, check=True):
    """Chạy một lệnh shell và in output."""
    print(f"▶️  Đang chạy lệnh: {' '.join(command)}")
    try:
        process = subprocess.run(command, check=check, text=True, capture_output=True, encoding='utf-8')
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            # In lỗi ra stderr để có màu đỏ trong terminal
            print(process.stderr, file=sys.stderr)
        if check and process.returncode != 0:
            print(f"❌ LỖI: Lệnh {' '.join(command)} thất bại.", file=sys.stderr)
            return False
        print("✅ Hoàn thành!")
        return True
    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy lệnh '{command[0]}'. Hãy đảm bảo nó đã được cài đặt và nằm trong PATH.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ LỖI BẤT NGỜ: {e}", file=sys.stderr)
        return False

def check_and_install_homebrew():
    """Kiểm tra xem Homebrew đã được cài đặt chưa."""
    print("\n--- 1. Kiểm tra Homebrew ---")
    if shutil.which("brew"):
        print("✅ Homebrew đã được cài đặt.")
        return True
    else:
        print("❌ LỖI: Homebrew chưa được cài đặt.", file=sys.stderr)
        print("Homebrew là cần thiết để cài đặt các công cụ hệ thống.", file=sys.stderr)
        print("Vui lòng mở Terminal và chạy lệnh sau để cài đặt Homebrew, sau đó chạy lại script này:", file=sys.stderr)
        print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', file=sys.stderr)
        return False

def install_brew_package(package_name):
    """Kiểm tra và cài đặt một gói qua Homebrew."""
    print(f"\n--- Kiểm tra công cụ '{package_name}' ---")
    if run_command(["brew", "list", package_name], check=False):
        print(f"✅ {package_name} đã được cài đặt.")
        return True
    else:
        print(f"🟡 {package_name} chưa được cài đặt. Đang tiến hành cài đặt qua Homebrew...")
        return run_command(["brew", "install", package_name])

def install_python_dependencies():
    """Cài đặt các thư viện Python từ requirements.txt."""
    print("\n--- 4. Cài đặt các thư viện Python ---")
    pip_command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    return run_command(pip_command)

def main():
    """Hàm chính để chạy toàn bộ quá trình cài đặt."""
    print("=============================================")
    print(" BẮT ĐẦU QUÁ TRÌNH TỰ ĐỘNG CÀI ĐẶT VÀ SỬA LỖI ")
    print("=============================================")

    if not check_and_install_homebrew():
        sys.exit(1)

    # Cài các gói Homebrew cần thiết
    if not install_brew_package("blueutil"): # Cho Bluetooth
        sys.exit(1)
    if not install_brew_package("portaudio"): # Cho thư viện âm thanh PyAudio
        sys.exit(1)

    # Cài các gói Python
    if not install_python_dependencies():
        sys.exit(1)

    print("\n=============================================")
    print("🎉 TẤT CẢ ĐÃ SẴN SÀNG! 🎉")
    print("Bạn có thể chạy ứng dụng ngay bây giờ bằng lệnh:")
    print("   python3 run.py")
    print("=============================================")

if __name__ == "__main__":
    main()