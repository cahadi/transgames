import platform
import ctypes

def optimize_for_windows():
    if platform.system() == "Windows":
        try:
            ctypes.windll.kernel32.SetPriorityClass(
                ctypes.windll.kernel32.GetCurrentProcess(),
                0x00000080  # HIGH_PRIORITY_CLASS
            )
        except:
            pass

optimize_for_windows()