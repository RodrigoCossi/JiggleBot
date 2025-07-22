
import time
import threading
import ctypes
import os
import sys
from pystray import Icon, MenuItem, Menu
from PIL import Image

# after changes, run rebundle.ps1

# Global variables
paused = False
stop_event = threading.Event()
tray_icon = None  # Global reference to the tray icon
mutex = None  # Global reference to instance


# Prevent multiple instances using a named mutex
def is_already_running():
    global mutex
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "JiggleBotMutex")
    last_error = ctypes.windll.kernel32.GetLastError()
    return last_error == 183  # ERROR_ALREADY_EXISTS


# Windows idle time detection
class IdleTime:
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    @staticmethod
    def get_idle_duration():
        lii = IdleTime.LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(IdleTime.LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0

# Simulate mouse movement
def simulate_mouse_move():
    ctypes.windll.user32.mouse_event(0x0001, 0, 1, 0, 0)

# Background thread
def monitor_idle():
    while not stop_event.is_set():
        if not paused and IdleTime.get_idle_duration() > 240:  # 4 minutes
            simulate_mouse_move()
        time.sleep(60)


# Tray icon setup
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # PyInstaller sets _MEIPASS at runtime, which is the temporary directory where bundled files are extracted
    # If not running from a bundle, use the current directory
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_image():
    return Image.open(resource_path("new_tray_icon.png"))

# Tray icon actions
def build_menu():
    return Menu(
        MenuItem("About", show_about),
        MenuItem("Resume" if paused else "Pause", toggle_pause),
        MenuItem("Quit", on_quit)
    )

def toggle_pause(icon, item):
    global paused
    paused = not paused
    tray_icon.menu = build_menu()

def show_about(icon, item):
    threading.Thread(target=lambda: show_info(
        "About", "Jiggle Bot: Programmatic Mouse Jiggler\nVersion 1.0\nBy RodrigoCossi @ GitHub")).start()

def on_quit(icon, item):
    stop_event.set()
    global mutex
    if mutex:
        ctypes.windll.kernel32.CloseHandle(mutex)
    icon.stop()

def show_info(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)  # MB_ICONINFORMATION

def show_error(title, error):
    ctypes.windll.user32.MessageBoxW(0, str(error), title, 0x10)  # MB_ICONERROR

# Main entry point
def main():
    global tray_icon

    if is_already_running():
        show_info("Jiggle Bot", "Jiggle Bot is already running in the system tray.")
        return
    
    # Startup logic moved to installer or task scheduler

    threading.Thread(target=monitor_idle, daemon=True).start()

    tray_icon = Icon("jigglebot", icon=create_image(), title="Jiggle Bot: Programmatic Mouse Jiggler")
    tray_icon.menu = build_menu()    
    tray_icon.run()

if __name__ == "__main__":
    main()
