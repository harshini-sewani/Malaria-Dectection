# -*- coding: utf-8 -*-
"""Resnet50

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EFEzrtLgOpu2IRnNxJVSa0MzO-1cTMtH

# **This is important when using google colab to mount the drive.**
"""

from google.colab import drive
drive.mount('/content/gdrive')

"""# **Importing all the packages**"""

from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.applications.resnet50 import ResNet50
from keras import Model, layers
import cv2
import matplotlib.pyplot as plt
from glob import glob

"""# **Path variable to be set to where all the cell images are present**"""

path = "/content/gdrive/My Drive/cell images"

"""# **Plot one of the infected and not infected cell image**"""

img = cv2.imread("/content/gdrive/My Drive/cell images/Parasitized/C100P61ThinF_IMG_20150918_144104_cell_162.png")
plt.imshow(img)
plt.axis("off")
plt.title("Parasitized")
plt.show()
img1 = cv2.imread("/content/gdrive/My Drive/cell images/Uninfected/C100P61ThinF_IMG_20150918_144104_cell_128.png")
plt.imshow(img1)
plt.axis("off")
plt.title("Uninfected")
plt.show()

"""# **Find size of an image and no. of classes**"""

x = img_to_array(img1)
print(x.shape)
numberOfClass = len(glob(path + "/*"))
print(numberOfClass)

"""# **Using RESNET 50 on Cell Images**"""

res_net = ResNet50(include_top = True, weights = "imagenet")
res_net.layers.pop()
res_net.layers.pop()
res_net.summary()

res_net_layer_list = res_net.layers

"""# **Adding the Dense and Dropout layer at the end of resnet50 model**"""

model = Sequential()

model_input = layers.Input(shape=(224,224,3))

x = res_net(model_input)

x = layers.Dropout(0.5)(x)

x = layers.Dense(128, activation='relu')(x) 

predictions = layers.Dense(2, activation='softmax')(x)

model = Model(model_input, predictions)
model.compile(loss = "categorical_crossentropy",
              optimizer = "rmsprop",
              metrics = ["accuracy"])
batch_size=8

"""# Generate Train and Test set also converting size of the images to 224*224 **bold text**"""

image_data_gen = ImageDataGenerator(rescale=1./255,
                                    validation_split=0.3)
train_data_gen = image_data_gen.flow_from_directory(directory=path,
                                                    target_size = (224,224),
                                                    batch_size=batch_size,
                                                    class_mode = 'categorical',
                                                    subset='training')

test_data_gen = image_data_gen.flow_from_directory(directory=path,
                                                    target_size = (224,224),
                                                    batch_size=batch_size,
                                                    class_mode = 'categorical',
                                                    subset='validation')

hist = model.fit_generator(train_data_gen,
                           steps_per_epoch=train_data_gen.n//batch_size,
                           epochs= 10,
                           validation_data=test_data_gen,
                           validation_steps= test_data_gen.n//batch_size)

print(hist.history.keys())

"""#  **Plotting Train and Test Loss **"""

plt.plot(hist.history["loss"], label = "Train Loss")
plt.plot(hist.history["val_loss"], label = "Validation Loss")
plt.legend()
plt.show()