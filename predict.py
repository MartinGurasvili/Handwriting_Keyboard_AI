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
import joblib
labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


model = joblib.load("model.pkl")
folder = str(os.fspath(Path(__file__).resolve().parent / "data"))

def load_data(path):
    print("Getting data..")
    with gzip.open(path, 'rb') as f:
        z,dtype,dim = struct.unpack(">HBB",f.read(4))
        shape = tuple(struct.unpack(">I",f.read(4))[0] for d in range(dim))
        print(shape)
        return np.frombuffer(f.read(),dtype=np.uint8).reshape(shape)


test_img = folder +'/emnist-byclass-test-images-idx3-ubyte.gz'
test_x = load_data(test_img)

test_x = test_x/255.0

num = random.randint(0,len(test_x))
# print(None,test_x[55])

plt.imshow(test_x[num].T,cmap = "gray")
plt.colorbar()
plt.show()

classes = model.predict(np.array([test_x[num]]))
temp = np.round(classes)
print(int(list(np.where(temp==1))[1]))
print(labels[int(list(np.where(temp==1))[1])])
  

    