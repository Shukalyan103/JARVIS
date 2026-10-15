import os
import sys
import cv2
import base64
from PIL import ImageGrab
from colorama import Fore, Style, init

# Ensure UTF-8 output when possible on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

init(autoreset=True)

# Path to data directory for saving snapshots
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def capture_webcam(filename="camera_view.jpg"):
    """
    Captures a single frame from the default webcam (camera index 0).
    Saves the image to the data directory and returns its absolute path.
    Returns None if webcam is unavailable or capture fails.
    """
    save_path = os.path.join(DATA_DIR, filename)
    print(Fore.YELLOW + "[Eyes]: Initializing optical camera sensor...", end="", flush=True)

    cap = None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("\r" + Fore.RED + "[Eyes]: Unable to access webcam (device not found or in use).")
            return None

        # Warm up sensor by reading a throwaway frame
        cap.read()
        ret, frame = cap.read()

        if ret and frame is not None:
            cv2.imwrite(save_path, frame)
            print("\r" + Fore.GREEN + f"[Eyes]: Image captured successfully -> {save_path}")
            return save_path
        else:
            print("\r" + Fore.RED + "[Eyes]: Failed to grab a frame from webcam.")
            return None
    except Exception as e:
        print("\r" + Fore.RED + f"[Eyes]: Camera error: {e}")
        return None
    finally:
        if cap is not None:
            cap.release()


def capture_screen(filename="screen_view.jpg"):
    """
    Captures the current desktop screen display.
    Saves the image to the data directory and returns its absolute path.
    Returns None if screenshot capture fails.
    """
    save_path = os.path.join(DATA_DIR, filename)
    print(Fore.YELLOW + "[Eyes]: Scanning desktop display...", end="", flush=True)

    try:
        screenshot = ImageGrab.grab()
        # Convert to RGB if needed (e.g. RGBA on some displays)
        if screenshot.mode in ("RGBA", "P"):
            screenshot = screenshot.convert("RGB")
        screenshot.save(save_path, "JPEG", quality=85)
        print("\r" + Fore.GREEN + f"[Eyes]: Display captured successfully -> {save_path}")
        return save_path
    except Exception as e:
        print("\r" + Fore.RED + f"[Eyes]: Screen capture error: {e}")
        return None


def encode_image(image_path):
    """
    Encodes an image file on disk into a base64 UTF-8 string for OpenRouter/OpenAI API.
    """
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(Fore.RED + f"[Eyes] Image encoding error: {e}")
        return None


if __name__ == "__main__":
    print(Fore.CYAN + "=== Testing JARVIS Eyes Module ===")
    print("1. Testing Screen Capture...")
    sc_path = capture_screen("test_screen.jpg")
    if sc_path:
        print(f"Screen encoded size: {len(encode_image(sc_path))} chars")

    print("\n2. Testing Webcam Capture...")
    cam_path = capture_webcam("test_cam.jpg")
    if cam_path:
        print(f"Cam encoded size: {len(encode_image(cam_path))} chars")
