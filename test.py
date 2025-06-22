

def get_startup_shortcut_path():
    startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    return os.path.join(startup_dir, "JiggleBot.lnk")

def is_in_startup():
    return os.path.exists(get_startup_shortcut_path())

def toggle_startup(icon, item):
    shortcut_path = get_startup_shortcut_path()
    if is_in_startup():
        os.remove(shortcut_path)
        item.text = "Enable Start with Windows"
    else:
        exe_path = sys.executable
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.save()
        item.text = "Disable Start with Windows"

def show_about(icon, item):
    messagebox.showinfo("About", "Jiggle Bot: Progammatic Mouse Jiggler\nVersion 1.0\nPrevents screen lock due to inactivity.\nBy RodrigoCossi @ GitHub.com")

def toggle_pause(icon, item):
    global paused
    paused = not paused
    item.text = "Resume" if paused else "Pause"

def on_exit(icon, item):
    stop_event.set()
    icon.stop()


def main():
    threading.Thread(target=monitor_idle, daemon=True).start()

    startup_item = MenuItem(
        "Disable Start with Windows" if is_in_startup() else "Enable Start with Windows",
        toggle_startup
    )

    icon = Icon("Jiggle Bot: Progammatic Mouse Jiggler")
    icon.icon = create_image()
    icon.menu = Menu(
        MenuItem("About", show_about),
        MenuItem("Pause", toggle_pause),
        startup_item,
        MenuItem("Exit", on_exit)
    )
    icon.run()

if __name__ == "__main__":
    main()
