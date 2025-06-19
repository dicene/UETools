import sys
import os
import time
import logging
import shutil
import psutil
import subprocess

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

path = "" # path to where UE is outputting your pak
dest_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Oblivion Remastered\\OblivionRemastered\\Content\\Paks\\LogicMods\\" # path to your desired paks/LogicMods folder
old_name = "pakchunk200*" # original name of your pak
new_name = "TestMod1" # desired name of your pak
has_changes_to_push = False
oblivion_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Oblivion Remastered\\OblivionRemastered\\Binaries\\Win64\\obse64_loader.exe" # path to your Oblivion or OBSE exe

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

def tick():
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

if __name__ == "__main__":
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
        while True:
            time.sleep(1)
            tick()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()