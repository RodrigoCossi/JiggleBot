# JiggleBot for macOS. Prevents screen lock by simulating mouse movement.

"""
This version:
- Uses Quartz to detect idle time and simulate mouse movement in macOS machines.
- Quartz is a macOS framework for low-level event handling, which is part of the pyobjc library.

in order to compile this code for macOS, you need to have the following packages installed:
pip install pyobjc pystray pillow

Following that:
pip install pyinstaller (bundles this python script into a standalone macOS application)

Build the app:
pyinstaller --windowed --icon=tray_icon.icns --onefile JiggleBot-MacOS.py


The app will be located in dist/ as a .app bundle or binary

"""



import time
import threading
import Quartz
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# macOS idle time detection
class IdleTime:
    @staticmethod
    def get_idle_duration():
        return Quartz.CGEventSourceSecondsSinceLastEventType(
            Quartz.kCGEventSourceStateHIDSystemState,
            Quartz.kCGAnyInputEventType
        )

# Simulate mouse movement
def simulate_mouse_move():
    loc = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    move = Quartz.CGEventCreateMouseEvent(
        None, Quartz.kCGEventMouseMoved, (loc.x + 1, loc.y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, move)

# Background thread
def monitor_idle():
    while not stop_event.is_set():
        if IdleTime.get_idle_duration() > 240:  # 4 minutes
            simulate_mouse_move()
        time.sleep(60)

# Tray icon setup
def create_image():
    return Image.open("tray_icon.png")

def on_exit(icon, item):
    stop_event.set()
    icon.stop()

stop_event = threading.Event()
threading.Thread(target=monitor_idle, daemon=True).start()

icon = Icon("Screen-Lock Blocker")
icon.icon = create_image()
icon.menu = Menu(MenuItem("Exit", on_exit))
icon.run()




# Note: ---------------------------------------------------------------------

import os
import sys
import time
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image
import tkinter.messagebox as messagebox
from AppKit import NSWorkspace
from Quartz import CGEventCreate, CGEventPost, kCGHIDEventTap, kCGEventMouseMoved
from Quartz.CoreGraphics import CGPoint

paused = False
stop_event = threading.Event()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_image():
    return Image.open(resource_path("tray_icon.png"))

def get_idle_duration():
    # Returns idle time in seconds
    idle_time = NSWorkspace.sharedWorkspace().idleTime()
    return idle_time / 1000.0

def simulate_mouse_move():
    # Simulate a tiny mouse move to prevent sleep
    event = CGEventCreate(None)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(
        None, kCGEventMouseMoved, CGPoint(0, 1), 0))
    CGEventPost(kCGHIDEventTap, event)

def monitor_idle():
    while not stop_event.is_set():
        if not paused and get_idle_duration() > 240:
            simulate_mouse_move()
        time.sleep(60)

def show_about(icon, item):
    messagebox.showinfo("About", "Jiggle Bot: Programmatic Mouse Jiggler\nVersion 1.0\nPrevents screen lock due to inactivity.\nBy RodrigoCossi @ GitHub.com")

def toggle_pause(icon, item):
    global paused
    paused = not paused
    item.text = "Resume" if paused else "Pause"

def on_exit(icon, item):
    stop_event.set()
    icon.stop()

def main():
    threading.Thread(target=monitor_idle, daemon=True).start()

    icon = Icon("Jiggle Bot: macOS")
    icon.icon = create_image()
    icon.menu = Menu(
        MenuItem("About", show_about),
        MenuItem("Pause", toggle_pause),
        MenuItem("Exit", on_exit)
    )
    icon.run()

if __name__ == "__main__":
    main()
