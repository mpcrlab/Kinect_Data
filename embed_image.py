from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import facenet
import os
import sys
import math
import sklearn
from PIL import Image

class ImageEmbedding():
    def __init__(self, args):
        tf.Graph().as_default()
        self.sess = tf.Session()

        # Load the model
        print('Loading feature extraction model')
        facenet.load_model(args["model"], self.sess)
        
        # Get input and output tensors
        self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        self.embedding_size = self.embeddings.get_shape()[1]
                
    def embed(self, img):
        # Run forward pass to calculate embeddings
        print('Calculating features for images')
        feed_dict = { self.images_placeholder:img, self.phase_train_placeholder:False }
        emb = self.sess.run(self.embeddings, feed_dict=feed_dict)
        return emb        

imgemb = ImageEmbedding({
    "model": "20170512-110547/"
})
img = Image.open("shia.jpg")
img = img.resize((160, 160))
img = np.asarray(img)
img = np.reshape(img, [1, 160, 160, 3])
print(img.shape)

print(imgemb.embed(img))
