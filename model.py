import numpy as np
import pandas as pd
import struct
import random
import os
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import matplotlib.pyplot as plt
import gzip
import pickle
import joblib
labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
folder = str(os.fspath(Path(__file__).resolve().parent / "data"))

def load_data(path):
    print("Getting data..")
    with gzip.open(path, 'rb') as f:
        z,dtype,dim = struct.unpack(">HBB",f.read(4))
        shape = tuple(struct.unpack(">I",f.read(4))[0] for d in range(dim))
        print(shape)
        return np.frombuffer(f.read(),dtype=np.uint8).reshape(shape)

def load_emnist():
    train_img = folder +'/emnist-byclass-train-images-idx3-ubyte.gz'
    train_lab = folder +'/emnist-byclass-train-labels-idx1-ubyte.gz'
    test_img = folder +'/emnist-byclass-test-images-idx3-ubyte.gz'
    test_lab = folder +'/emnist-byclass-test-labels-idx1-ubyte.gz'

    train_x = load_data(train_img)
    train_y = load_data(train_lab)
    test_x = load_data(test_img)
    test_y = load_data(test_lab)
    return train_x, train_y, test_x, test_y

train_x, train_y, test_x, test_y = load_emnist()

train_x = train_x / 255.0
test_x = test_x/255.0

plt.imshow(test_x[55].T,cmap = "gray")
plt.colorbar()
plt.show()

class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if logs.get('accuracy') is not None and logs.get('accuracy') > 0.99:
                print("\nReached 99% accuracy so cancelling training!") 
                self.model.stop_training = True


callbacks = myCallback()

model = tf.keras.models.Sequential([ 
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(len(labels), activation=tf.nn.softmax)
]) 
model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy']) 

model.fit(train_x, train_y, epochs=2, callbacks=[callbacks])
joblib.dump(model, 'model.pkl')
# file = open('model.pkl', 'wb')
# pickle.dump(model, file) 
    
# classes = model.predict(test_x[55], verbose = 1)

# print(classes[0])
# print(labels[int(classes[0])])
  
plt.imshow(test_x[55].T,cmap = "gray")
plt.colorbar()
plt.show()

