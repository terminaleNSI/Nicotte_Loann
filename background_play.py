# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 16:44:32 2021

@author: loann
"""

import threading
import time
import fonctions_utiles as FU


def start_time():
    while thread_time.state:
        time.sleep(1)
        FU.update_time_played()


class time_stat(threading.Thread):
    def __init__(self):
        super().__init__()
        self.state = True

    def run(self) -> None:
        start_time()
        self.state = False


thread_time = time_stat()
thread_time.start()
