# This was my original project, which inspired the creation of the JiggleBot App.

#Disclaimer of Liability for Misuse:
#This software is provided for educational and authorized use only. The creator of this software (@RodrigoCossi) is not responsible for any misuse, unauthorized access, or illegal activity carried out using this tool.
#By using this software, you agree to use it in compliance with all applicable laws and regulations. Any actions taken with this software are solely the responsibility of the user.
#Use at your own risk.

# Screen-Lock Blocker:
# - Programmatic mouse jiggler that prevents screen auto-lock.
# - Checks for real idle time every 60 sec. Only triggers if idle time is > 4 minutes.
# - Uses SendInput() from user32.dll to simulate actual mouse movement at the system level.
# - Works even if PowerShell runs in the background.
# - Should fully prevent screen lock, even in corporate/managed setups.
# - Lightweight, efficient and discrete.


Write-Host "Screen-Lock Blocker is running... Close terminal to stop script execution."

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class IdleTime {
    [StructLayout(LayoutKind.Sequential)]
    struct LASTINPUTINFO {
        public uint cbSize;
        public uint dwTime;
    }

    [DllImport("user32.dll")]
    static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);

    public static uint GetIdleTime() {
        LASTINPUTINFO lii = new LASTINPUTINFO();
        lii.cbSize = (uint)Marshal.SizeOf(lii);
        GetLastInputInfo(ref lii);
        return ((uint)Environment.TickCount - lii.dwTime);
    }
}
"@

# Add INPUT simulation
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class InputSimulator {
    [DllImport("user32.dll", SetLastError = true)]
    static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    [StructLayout(LayoutKind.Sequential)]
    struct MOUSEINPUT {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct INPUT {
        public int type;
        public MOUSEINPUT mi;
    }

    const int INPUT_MOUSE = 0;
    const uint MOUSEEVENTF_MOVE = 0x0001;

    public static void SimulateMouseMove() {
        INPUT[] inputs = new INPUT[1];
        inputs[0].type = INPUT_MOUSE;
        inputs[0].mi.dx = 0;
        inputs[0].mi.dy = 1; // minimal movement
        inputs[0].mi.mouseData = 0;
        inputs[0].mi.dwFlags = MOUSEEVENTF_MOVE;
        inputs[0].mi.time = 0;
        inputs[0].mi.dwExtraInfo = IntPtr.Zero;

        SendInput(1, inputs, Marshal.SizeOf(typeof(INPUT)));
    }
}
"@

while ($true) {
    $idleMs = [IdleTime]::GetIdleTime()
    if ($idleMs -ge (4 * 60 * 1000)) {
        [InputSimulator]::SimulateMouseMove()
    }
    Start-Sleep -Seconds 60
}
