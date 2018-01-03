import numpy as np
import cv2
from getFrame import getFrameThread
from getkeys import key_check

window_title_substring = "Grand Theft Auto V"
showImshows = True

HEIGHT = 1920
WIDTH = 1080

x1 = int(29 * (1080 / WIDTH))
x2 = int((29 + 270) * (1080 / WIDTH))
y1 = int(873 * (1920 / HEIGHT))
y2 = int((873 + 172) * (1920 / HEIGHT))

def process_img(image):
    original_image = image
    doStuffAroundHere()
    if showImshows == True:
        cv2.waitKey(1)
    return myValues

def main():
    frameThread = getFrameThread(x1, x2, y1, y2, window_title_substring).start()
    paused = False
    while True:
        keys = key_check()
        if 'O' in keys:
            if paused:
                print('Unpausing')
                paused = False
                time.sleep(1)
            else:
                print('Pausing')
                paused = True
                time.sleep(1)
        elif 'U' in keys:
            print('Exiting')
            if showImshows == True:
                cv2.destroyAllWindows()
            time.sleep(1)
            frameThread.stopNow()
            break
        if paused == False:
            frame = frameThread.returnFrame()
            screen = np.array(frame)
            value = process_img(screen)
                    
main()
