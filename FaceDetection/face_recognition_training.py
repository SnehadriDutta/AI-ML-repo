# -*- coding: utf-8 -*-
"""Face-Recognition-Training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mIlCOJWKbNGGG6Mydmx-Wi0tM9EqRqQz
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

Image_Size = [244,244,3]

folders = glob("drive/MyDrive/ImageDataset/train/*")
print(len(folders))

vgg = VGG16(input_shape=Image_Size, weights='imagenet', include_top=False)

for layer in vgg.layers:
  layer.trainable = False

x = Flatten()(vgg.output)
output = Dense(len(folders), activation = 'softmax')(x)
model = Model(inputs= vgg.input, outputs = output)
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator( rescale = 1./255, shear_range = 0.2,
                                   zoom_range = 0.2, horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

train_set = train_datagen.flow_from_directory("drive/MyDrive/ImageDataset/train", target_size = (244,244),
                                              batch_size = 32, class_mode = 'categorical')
test_set = train_datagen.flow_from_directory("drive/MyDrive/ImageDataset/test", target_size = (244,244),
                                              batch_size = 32, class_mode = 'categorical')

print(len(train_set))
print(len(test_set))

r = model.fit_generator(train_set, validation_data = test_set, epochs = 5,
                        steps_per_epoch = len(train_set), validation_steps = len(test_set))

# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()

plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()

model.save("face-recognization.h5")

