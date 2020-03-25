import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import Model
from tqdm import tqdm
import os
import pandas as pd
import numpy as np
import time
# import skimage.io
import pickle

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

dtype = 'float16'
K.set_floatx(dtype)
K.set_epsilon(1e-4)


"""
TO-DO
1) Write own generator. Currently using ImageDataGenerator in Keras
"""

# def feature_extraction(exp_name, patch_dir, target_size=(299, 299)):
#
# 	# Load imagenet pre-trained InceptionV3
# 	base_model = InceptionV3(weights='imagenet')
# 	model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
# 	patch_list = os.listdir(patch_dir)
# 	image_features_df = pd.DataFrame(index=patch_list, columns=list(range(2048)), dtype='float16')
#
# 	for patch in tqdm(patch_list):
# 	    img = image.load_img(os.path.join(patch_dir,patch), target_size=(299, 299))
# 	    x = image.img_to_array(img, dtype='float16')/255
# 	    x = np.expand_dims(x, axis=0)
# 	    feature_vec = model.predict(x)
# 	    image_features_df.loc[patch] = feature_vec[0]
#
#
# 	image_features_df.to_csv('{}.csv'.format(exp_name), index_label='File')

class InceptionV3Vectorizer:
    def __init__(self, batch_size=200):
        base_model = InceptionV3(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
        self.batch_size = batch_size

    def generate_vectors(self, imgs):
    	print('Generating vectors on {} images'.format(len(imgs)))
    	imgs = np.array(imgs)
    	imgs = preprocess_input(imgs)
    	features = self.model.predict(imgs)
    	return features
