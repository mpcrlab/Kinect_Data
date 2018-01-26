import tensorflow as tf
import numpy as np
import detect_face
from scipy import misc
from PIL import Image, ImageDraw

with tf.Graph().as_default():
    sess = tf.Session()
    with sess.as_default():
        with tf.variable_scope('pnet'):
            data = tf.placeholder(tf.float32, (None,None,None,3), 'input')
            pnet = detect_face.PNet({'data':data})
            pnet.load('det1.npy', sess)
        with tf.variable_scope('rnet'):
            data = tf.placeholder(tf.float32, (None,24,24,3), 'input')
            rnet = detect_face.RNet({'data':data})
            rnet.load('det2.npy', sess)
        with tf.variable_scope('onet'):
            data = tf.placeholder(tf.float32, (None,48,48,3), 'input')
            onet = detect_face.ONet({'data':data})
            onet.load('det3.npy', sess)
            
        pnet_fun = lambda img : sess.run(('pnet/conv4-2/BiasAdd:0', 'pnet/prob1:0'), feed_dict={'pnet/input:0':img})
        rnet_fun = lambda img : sess.run(('rnet/conv5-2/conv5-2:0', 'rnet/prob1:0'), feed_dict={'rnet/input:0':img})
        onet_fun = lambda img : sess.run(('onet/conv6-2/conv6-2:0', 'onet/conv6-3/conv6-3:0', 'onet/prob1:0'), feed_dict={'onet/input:0':img})

def detect(img):
    img = np.reshape(img, [1080, 1920, 4])[:, :, :3]
    img = misc.imresize(img, [108, 192])
    bounding_boxes, points = detect_face.detect_face(img, 20, pnet_fun, rnet_fun, onet_fun, [0.6, 0.7, 0.7], 0.709)


    if len(bounding_boxes) > 0:
        bb = bounding_boxes[0][:4]
        bb = [(bb[0] * 10, bb[1] * 10), ((bb[2] * 10) - (bb[0] * 10), (bb[3] * 10) - (bb[1] * 10))]
        return bb, points
    return [], []
