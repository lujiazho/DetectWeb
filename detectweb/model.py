import sys
import time
import io
import os

import random
import string
import datetime

import base64
from PIL import Image, ImageFile

from flask import request, jsonify, Flask, url_for

import numpy as np
import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.compat.v1.disable_eager_execution()

from detectweb import label_image

model_file = 'static/tf_files/retrained_graph.pb'
label_file = 'static/tf_files/retrained_labels.txt'
input_height = 224
input_width = 224
input_mean = 128
input_std = 128
input_layer = "input"
output_layer = "final_result"

g = tf.Graph()
with g.as_default():
    graph = label_image.load_graph(model_file)

