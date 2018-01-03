import numpy as np
import time
from getkeys import key_check, keylist
import os
from MouseThread import *
from getFrame import getFrameThread
import _thread
starting_value = 1

while True:
    file_name = 'E:/Programming/training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        
        break


def keys_to_output(keys):
    output = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for n in keylist:
        for i in keys:
            if i == n:
                output[n] = 1
                break

    return output


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    print('STARTING!!!')
    frameThread = getFrameThread().start()

    mousecache = [0, 0, 0, 0]
    mthr = MouseThread(mousecache)
    mthr.start()
    while True:
        last_time = time.time()
        if not paused:
            screen = frameThread.returnFrame()
            keys = key_check()
            output = keys_to_output(keys)
            output[256] = mousecache[0] / 256
            output[257] = mousecache[1] / 256
            output[258] = mousecache[2] / 256
            output[259] = mousecache[3] / 256

            training_data.append([screen, output])
            mousecache[0] = 0
            mousecache[1] = 0
            mousecache[2] = 0
            mousecache[3] = 0

            if len(training_data) % 64 == 0:
                print(len(training_data))
                
                if len(training_data) == 256:
                    _thread.start_new_thread(np.save, (file_name, training_data))
                    print('SAVED ' + file_name)
                    np.empty(training_data)
                    training_data = []
                    starting_value += 1
                    file_name = 'E:/Programming/training_data-{}.npy'.format(starting_value)
                    #print("Loop took", time.time() - last_time)
            sleep = 0.04-(time.time() - last_time)
            if sleep > 0:
                time.sleep(sleep)
        keys = key_check()
        if 0x50 in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(file_name, starting_value)
