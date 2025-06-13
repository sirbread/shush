import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt
from pynput import keyboard

from screen_cleaner.desktop_cleanup import (
    hide_desktop_icons,
    show_desktop_icons,
    set_blank_wallpaper,
    restore_wallpaper
)

class ShushApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("shush")
        self.setWindowIcon(QIcon("shush.ico"))
        self.setFixedSize(300, 250)

        self.layout = QVBoxLayout()

        self.clear_desktop_checkbox = QCheckBox("Clear Desktop")
        self.layout.addWidget(self.clear_desktop_checkbox)

        self.execute_button = QPushButton("EXECUTE (selected items)")
        self.execute_button.clicked.connect(self.run_selected_actions)
        self.layout.addWidget(self.execute_button)

        self.revert_button = QPushButton("REVERT (selected items)")
        self.revert_button.clicked.connect(self.revert_selected_actions)
        self.layout.addWidget(self.revert_button)

        self.hide_button = QPushButton("HIDE SHUSH (visible in system tray)")
        self.hide_button.clicked.connect(self.enter_stealth_mode)
        self.layout.addWidget(self.hide_button)

        self.setLayout(self.layout)

        self.is_active = False

        self.setup_tray_icon()

        self.listener_thread = threading.Thread(target=self.start_hotkey_listener, daemon=True)
        self.listener_thread.start()

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("shush.ico"))

        tray_menu = QMenu()

        show_action = QAction("show window", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)

        hide_action = QAction("hide window", self)
        hide_action.triggered.connect(self.enter_stealth_mode)
        tray_menu.addAction(hide_action)

        exit_action = QAction("exit", self)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_menu = tray_menu

        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.setVisible(True)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray_menu.exec_(QCursor.pos())

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def run_selected_actions(self):
        if self.clear_desktop_checkbox.isChecked():
            hide_desktop_icons()
            set_blank_wallpaper()

    def revert_selected_actions(self):
        if self.clear_desktop_checkbox.isChecked():
            show_desktop_icons()
            restore_wallpaper()

    def enter_stealth_mode(self):
        self.hide()

    def on_activate(self):
        if not self.is_active:
            if self.clear_desktop_checkbox.isChecked():
                self.run_selected_actions()
                self.is_active = True
        else:
            self.revert_selected_actions()
            self.is_active = False

    def start_hotkey_listener(self):
        with keyboard.GlobalHotKeys({
            '<alt>+a': self.on_activate
        }) as listener:
            listener.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShushApp()
    window.show()
    sys.exit(app.exec_())
