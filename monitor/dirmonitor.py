#!/usr/bin/python3
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, os.environ.get("PROJ_ROOT"))
from urlReq import news_data_get

## ===================
# 2021-12-09
# 작성자: 김준현
## ===================
class Target:


    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦
        self.watchDir = os.environ["MONITOR_DIR"]

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir,recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
    
    @staticmethod
    def on_created(event): #파일, 디렉터리가 생성되면 실행
        filepath = event.src_path   
        print("데이터 처리 진행 ... {}".format(filepath))
        news_data_get.delay(filepath)


if __name__ == "__main__": #본 파일에서 실행될 때만 실행되도록 함
    print("감시 중...")
    w = Target()
    w.run()
