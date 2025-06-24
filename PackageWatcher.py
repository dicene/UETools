import sys
import os
import time
import logging
import shutil
import psutil
import subprocess
from PyQt6 import QtWidgets, QtCore, QtGui

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

path = "" # path to where UE is outputting your pak
dest_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Oblivion Remastered\\OblivionRemastered\\Content\\Paks\\LogicMods\\" # path to your desired paks/LogicMods folder
old_name = "pakchunk200*" # original name of your pak
new_name = "TestMod1" # desired name of your pak
has_changes_to_push = False
oblivion_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Oblivion Remastered\\OblivionRemastered\\Binaries\\Win64\\obse64_loader.exe" # path to your Oblivion or OBSE exe

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.count = 0
        # self.button = QtWidgets.QPushButton(f"Click Count: {self.count}", self)
        # self.button.setFixedSize(120, 60)
        # self.button.clicked.connect(self.count_clicks)
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.button)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)

        button = QtWidgets.QPushButton(self)
        button.setText("ABC")
        button.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(button)
        self.setLayout(layout)

    def start_button_clicked(self):
        # if self.timer.isActive():

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)

    # def count_clicks(self):
    #     self.count += 1
    #     self.button.setText(f"Click Count: {self.count}")
    def tick(self):
        global has_changes_to_push
        if has_changes_to_push:
            has_changes_to_push = False
            print(f"Changes have been made, re-running Oblivion... {oblivion_path}")
            already_open = False
            # os.spawnl(os.P_DETACH, oblivion_path, "")
            for proc in psutil.process_iter():
                if proc.name().find("blivion") > -1:
                    print(f"Oblivion process: {proc.name()} {proc.pid}")
                    already_open = True
                    # proc.kill()
                    # already_open = False

                # if process_name in proc.name():
                #     pid = proc.pid
                #     break
            if not already_open:
                pid = subprocess.Popen(oblivion_path, creationflags=0x8).pid

def on_modified(event):
    print(f"Modified: {event}")
    old_file_name = os.path.basename(event.src_path)
    _, old_extension = os.path.splitext(old_file_name)
    new_file_path = dest_path + new_name + old_extension
    global has_changes_to_push
    has_changes_to_push = True
    try:
        shutil.copy2(event.src_path, new_file_path)
        has_changes_to_push = True
    except Exception as e:
        print(f"Failed to copy files, looks like they're probably still in use! {e}")
    print(f"Copying ({event.src_path}) to ({new_file_path})")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    window = Window()
    window.show()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    event_handler = PatternMatchingEventHandler(patterns=[old_name], ignore_patterns=[])
    event_handler.on_modified = on_modified
    # event_handler.patterns = {"pakchunk200*"}
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    print("Starting observer...")
    print(f"dest_path: {dest_path}")
    observer.start()
    try:
        app.exec()
        # while True:
        #     time.sleep(1)
        #     if has_changes_to_push:
        #         has_changes_to_push = False
        #         print(f"Changes have been made, re-running Oblivion... {oblivion_path}")
        #         already_open = False
        #         # os.spawnl(os.P_DETACH, oblivion_path, "")
        #         for proc in psutil.process_iter():
        #             if proc.name().find("blivion") > -1:
        #                 print(f"Oblivion process: {proc.name()} {proc.pid}")
        #                 already_open = True
        #                 # proc.kill()
        #                 # already_open = False
        #
        #             # if process_name in proc.name():
        #             #     pid = proc.pid
        #             #     break
        #         if not already_open:
        #             pid = subprocess.Popen(oblivion_path, creationflags=0x8).pid
    except KeyboardInterrupt:
        observer.stop()
    observer.join()