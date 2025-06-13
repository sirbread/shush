import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton

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
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()

        self.clear_desktop_checkbox = QCheckBox("clear desktop")
        self.layout.addWidget(self.clear_desktop_checkbox)

        self.execute_button = QPushButton("EXECUTE")
        self.execute_button.clicked.connect(self.run_selected_actions)
        self.layout.addWidget(self.execute_button)

        self.revert_button = QPushButton("REVERT")
        self.revert_button.clicked.connect(self.revert_selected_actions)
        self.layout.addWidget(self.revert_button)

        self.setLayout(self.layout)

    def run_selected_actions(self):
        if self.clear_desktop_checkbox.isChecked():
            hide_desktop_icons()
            set_blank_wallpaper()

    def revert_selected_actions(self):
        if self.clear_desktop_checkbox.isChecked():
            show_desktop_icons()
            restore_wallpaper()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShushApp()
    window.show()
    sys.exit(app.exec_())
