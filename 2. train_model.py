import numpy as np
from models import otherception3 as googlenet
from random import shuffle

FILE_I_END = 59

WIDTH = 680
HEIGHT = 384
LR = 1e-5
EPOCHS = 1

MODEL_NAME = 'warthunder.op.georggi'
PREV_MODEL = 'warthunder.op.georggi'

LOAD_MODEL = True

model = googlenet(HEIGHT, WIDTH, 3, LR, output=260, model_name=MODEL_NAME)

if LOAD_MODEL:
    model.load(PREV_MODEL)
    print('We have loaded a previous model!!!!')
    

# iterates through the training files
for e in range(EPOCHS):
    data_order = [i for i in range(1, FILE_I_END+1)]
    shuffle(data_order)
    for count,i in enumerate(data_order):
        try:
            file_name = 'E:/Programming/training_data-{}.npy'.format(i)
            # full file info
            train_data = np.load(file_name)
            print('training_data-{}.npy'.format(i),len(train_data))

            train = train_data[:-50]
            test = train_data[-50:]

            X = np.array([i[0] for i in train]).reshape(-1,HEIGHT,WIDTH ,3)
            Y = [i[1] for i in train]

            test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT,WIDTH ,3)
            test_y = [i[1] for i in test]

            model.fit({'input': X}, {'targets': Y}, n_epoch=1, batch_size=32, validation_set=({'input': test_x}, {'targets': test_y}),
                snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)
            if count%10 == 0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)

        except Exception as e:
            print(str(e))

model.save(MODEL_NAME)

#

#tensorboard --logdir=foo:C:/Users/domin/PyCharmProjects/pygta5/log

