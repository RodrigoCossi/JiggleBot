# JiggleBot - Programmatic Mouse Jiggler


JiggleBot is a lightweight Windows utility that prevents your computer from locking or going to sleep due to inactivity. It works by simulating periodic mouse movements, keeping your session active without manual intervention.

## Disclaimer of Liability for Misuse

This software is provided for educational and authorized use only. The creator of this software (@RodrigoCossi) is not responsible for any misuse, unauthorized access, or illegal activity carried out using this tool.

By using this software, you agree to use it in compliance with all applicable laws and regulations. Any actions taken with this software are solely the responsibility of the user.

**Use at your own risk.**


## Features

- Runs silently in the system tray.
- Prevents screen lock by simulating mouse movement every few minutes.
- Pause/Resume functionality via tray menu.
- "About" dialog for app information.
- Clean exit from tray menu.

## How It Works

JiggleBot monitors your system's idle time. If no user input is detected for 4 minutes, it simulates a small mouse movement to reset the idle timer. This keeps your computer awake and prevents automatic locking.

## Usage

1. It can be run as a stand-alone shell script `Original-PS-Script.ps1` or as a bundled executable `JiggleBot-Windows.exe` app.
2. The bundled executable app, will appear as an icon in your system tray.
3. Right-click the tray icon for options:
    - **About**: View app info.
    - **Pause/Resume**: Temporarily stop or restart the jiggling.
    - **Quit**: Exit the app.

## Installation

- Requires Python 3 and Pip pre-installed. If you already have Python3 and Pip, run `Install_dependencies_for_bundling.ps1`, and then the `rebundle.ps1` script.
- This will generate a `dist` folder, containing `JiggleBot-Windows.exe`.


## Launch on Login with Task Scheduler

To have JiggleBot start automatically when you log in:

1. Open **Task Scheduler** and select **Create Task**.
2. Under the **Actions** tab, set the action to start `JiggleBot-Windows.exe`.
3. In the **Triggers** tab, set the trigger to **At log on**.
4. (Optional) Check **Run with highest privileges** if needed.



## License

Licensed under the Apache License, Version 2.0. See [LICENSE.txt](LICENSE.txt) for details.

---

By RodrigoCossi @ GitHub