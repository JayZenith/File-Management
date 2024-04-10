from os import listdir, rename
from os.path import splitext, join, exists
from shutil import move
import os
import sys
import time 
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

src_dir = "../../Downloads"
pdfs_dir = "../pdfs"
lcs_dir = "../lcs"


def makeUniqueName(dst, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dst}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(dst, file, name):
    if exists(f"{dst}/{name}"):
    #if we have duplicates 
        uniqueName = makeUniqueName(dst, name)
        oldName = join(dst, name)
        newName = join(dst, uniqueName)
        rename(oldName, newName)
    move(file, dst)


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = src_dir

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)
            onlyfiles = []
            onlyfiles = os.scandir(src_dir)
            for file in onlyfiles:
                print(file)
                name = file.name
                if name.endswith(".pdf"):
                    dst = pdfs_dir
                    move_file(dst, file, name)
                elif name.endswith(".lc"):
                    dst = lcs_dir
                    move_file(dst, file, name)
        '''
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            #onlyfiles = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
            onlyfiles = []
            onlyfiles = os.scandir(src_dir)
            for file in onlyfiles:
                print(file)
                name = file.name
                if name.endswith(".pdf"):
                    dst = pdfs_dir
                    move_file(dst, file, name)
                elif name.endswith(".lc"):
                    dst = lcs_dir
                    move_file(dst, file, name)
        '''
            

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()



if __name__ == "__main__":
    #Set the format for logging info
   logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(message)s',
                       datefmt='%Y-%m-%d %H:%M:%S')
  #set format for displaying path
   path = src_dir
   # Initialize logging event handler 
   event_handler = Handler()

   #initialize observer 
   observer = Observer()
   observer.schedule(event_handler, path, recursive=True)

   # start observer 
   observer.start()
   try:
       while True:
        #set thread sleep time 
           time.sleep(1)
   except KeyboardInterrupt:
       observer.stop()
   observer.join()
