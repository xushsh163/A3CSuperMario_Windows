import threading
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.slim as slim
import scipy.signal
import os

from A3C import AC_Network
from A3CWorker import *

from random import choice
from time import sleep
from time import time

import matplotlib.pyplot as plt
from game_wrapper import Wrapper
import win32pipe, win32file, win32api, win32con, win32job

COMPLEX_MOVEMENT = Wrapper.ACTION_MAP

max_episode_length = 2100
gamma = .99 # discount rate for advantage estimation and reward discounting
s_size = 224 * 256 # Observations are greyscale frames of 250 * 250 * 1

a_size = len(Wrapper.ACTION_MAP) # Agent can move Left, Right, or Fire
load_model = False
model_path = './A3C/model'
gif_path = './A3C/frames'

tf.reset_default_graph()

if not os.path.exists(model_path):
    os.makedirs(model_path)
    
#Create a directory to save episode playback gifs to
if not os.path.exists(gif_path):
    os.makedirs(gif_path)

# with tf.device("/gpu:0"): 
global_episodes = tf.Variable(0,dtype=tf.int32,name='global_episodes',trainable=False)
trainer = tf.train.AdamOptimizer(learning_rate=1e-4)
master_network = AC_Network(s_size,a_size,'global',None) # Generate global network
num_workers = 3 #multiprocessing.cpu_count() # Set workers to number of available CPU threads, max value is multiprocessing.cpu_count()
workers = []
# Create worker classes
for i in range(num_workers):
    workers.append(Worker('SuperMarioBros-v0', COMPLEX_MOVEMENT,i,s_size,a_size,trainer,model_path,global_episodes))
saver = tf.train.Saver(max_to_keep=5)

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    if load_model == True:
        print ('Loading Model...')
        ckpt = tf.train.get_checkpoint_state(model_path)
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        sess.run(tf.global_variables_initializer())
        
    # This is where the asynchronous magic happens.
    # Start the "work" process for each worker in a separate threat.
    worker_threads = []
    for worker in workers:
        worker_work = lambda: worker.work(max_episode_length,gamma,sess,coord,saver)
        t = threading.Thread(target=(worker_work))
        t.start()
        sleep(0.5)
        worker_threads.append(t)
    coord.join(worker_threads)
