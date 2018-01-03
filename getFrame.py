from threading import Thread
from PIL import ImageGrab
import cv2
import numpy as np

class getFrameThread:
    def __init__(self):

        self.printscreen = cv2.cvtColor(cv2.resize(np.array(ImageGrab.grab(bbox=(0, 0, 1359, 767))),(680, 384)), cv2.COLOR_BGR2RGB)
        self.stop = False

    def start(self):
        Thread(target=self.getFrame, args=()).start()
        return self

    def getFrame(self):
        while True:
            if self.stop == True:
                break
            self.printscreen = cv2.cvtColor(cv2.resize(np.array(ImageGrab.grab(bbox=(0, 0, 1359, 767))),(680, 384)), cv2.COLOR_BGR2RGB)

    def returnFrame(self):

        return self.printscreen

    def stopNow(self):

        self.stop = True
"""from threading import Thread
from grabscreen2 import grab_screen2
import time


class getFrameThread:
    def __init__(self, width, height, window_title_substring):

        self.printscreen = grab_screen2(window_title=window_title_substring,
                                       region=(width, height))
        self.stop = False
        self.width = width
        self.height = height
        self.window_title_substring = window_title_substring

    def start(self):
        Thread(target=self.getFrame, args=()).start()
        return self

    def getFrame(self):
        render_last_time = time.time()
        render_frame_times = []
        while True:
            last_time = time.time()
            if self.stop == True:
                break
            self.printscreen = grab_screen2(window_title=self.window_title_substring,
                                            region=(self.width, self.height))
            ##            print('Frame took {} seconds'.format(time.time()-render_last_time))
            render_frame_times.append(time.time() - render_last_time)
            render_frame_times = render_frame_times[-20:]
            render_last_time = time.time()

    def returnFrame(self):
        return self.printscreen

    def stopNow(self):
        self.stop = True"""
