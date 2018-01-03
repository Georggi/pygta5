
import time
from directkeys import PressKey, ReleaseKey, MoveMouse
from models import otherception3 as googlenet
from getkeys import key_check
from getFrame import getFrameThread
import numpy as np

GAME_WIDTH = 1360
GAME_HEIGHT = 768

WIDTH = 680
HEIGHT = 384
LR = 1e-5
EPOCHS = 1

model = googlenet(HEIGHT, WIDTH, 3, LR, output=260)
MODEL_NAME = 'warthunder.op.georggi'
model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')


def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    frameThread = getFrameThread().start()
    frameThread.start()

    while True:
        if not paused:
            screen = np.array(frameThread.returnFrame())
            last_time = time.time()
            prediction = model.predict([screen.reshape(HEIGHT, WIDTH, 3)])[0]
            for i in range(0,256):
                if prediction[i] >= 0.5:
                    PressKey(i)
                else:
                    ReleaseKey(i)
            MoveMouse(prediction[256],prediction[257],prediction[258],prediction[259])
            sleep = 0.016 - (time.time() - last_time)
            if sleep > 0:
                time.sleep(sleep)

        keys = key_check()

        # p pauses game and can get annoying.
        if 0x50 in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                for i in range(0, 256):
                    ReleaseKey(i)
                time.sleep(1)


main()
