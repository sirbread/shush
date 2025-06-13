import ctypes
import winreg
import os
import tempfile
from shutil import copyfile
import win32gui
import win32con

def _get_desktop_listview():
    progman = win32gui.FindWindow("Progman", None)
    desktop_hwnd = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)

    if not desktop_hwnd:
        workerw = win32gui.FindWindowEx(0, 0, "WorkerW", None)
        desktop_hwnd = win32gui.FindWindowEx(workerw, 0, "SHELLDLL_DefView", None)

    return desktop_hwnd

def hide_desktop_icons():
    hwnd = _get_desktop_listview()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

def show_desktop_icons():
    hwnd = _get_desktop_listview()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

def get_current_wallpaper():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
    wallpaper, _ = winreg.QueryValueEx(key, "Wallpaper")
    winreg.CloseKey(key)
    return wallpaper

def set_blank_wallpaper():
    original = get_current_wallpaper()
    temp_dir = tempfile.gettempdir()
    backup_path = os.path.join(temp_dir, "shush_wallpaper_backup.jpg")

    if original and os.path.exists(original):
        try:
            copyfile(original, backup_path)
        except Exception:
            pass  #to my wallpaper engine users, yeah sorry

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Wallpaper", 0, winreg.REG_SZ, "")
    winreg.CloseKey(key)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, "", 3)

def restore_wallpaper():
    temp_dir = tempfile.gettempdir()
    backup_path = os.path.join(temp_dir, "shush_wallpaper_backup.jpg")

    if os.path.exists(backup_path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, backup_path, 3)
