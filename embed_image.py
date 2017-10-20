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
        with tf.Graph().as_default():
            with tf.Session() as sess:
                # Load the model
                print('Loading feature extraction model')
                facenet.load_model(args.model)
                
                # Get input and output tensors
                self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                self.embedding_size = embeddings.get_shape()[1]
                
    def embed(self, img):
        # Run forward pass to calculate embeddings
        print('Calculating features for images')
        feed_dict = { self.images_placeholder:img, self.phase_train_placeholder:False }
        emb = sess.run(embeddings, feed_dict=feed_dict)
            
imgemb = ImageEmbedding({
    "model": "20170512-110547/"
})
img = np.asarray(Image.open("shia.jpg"))
print(img.shape)
