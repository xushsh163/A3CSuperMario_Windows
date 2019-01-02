import threading
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.slim as slim
import scipy.signal
from A3C import AC_Network
from A3CHelper import *
from game_wrapper import Wrapper
import config
import math
import matplotlib.pyplot as plt
import threading


lock = threading.Lock()

class Worker():
    def __init__(self,game, movement, name,s_size,a_size,trainer,model_path,global_episodes):
        self.name = "worker_" + str(name)
        self.number = name        
        self.model_path = model_path
        self.trainer = trainer
        self.global_episodes = global_episodes
        self.increment = self.global_episodes.assign_add(1)
        self.episode_rewards = []
        self.episode_lengths = []
        self.episode_mean_values = []
        # self.summary_writer = tf.summary.FileWriter("./SuperMario_m/A3C/train/train_"+str(self.number),)
        self.summary_path = "./A3C/train/train_"+str(self.number)
        #Create the local copy of the network and the tensorflow op to copy global paramters to local network
        self.local_AC = AC_Network(s_size,a_size,self.name,trainer)
        self.update_local_ops = update_target_graph('global',self.name)        
        
        self.env = Wrapper(self.name, config.FRAME_GAP)
        self.movement = movement

        
        #End Doom set-up
        # self.env:BinarySpaceToDiscreteSpaceEnv = game
        
    def train(self,rollout,sess,gamma,bootstrap_value):
        rollout = np.array(rollout)
        observations = rollout[:,0]
        actions = rollout[:,1]
        rewards = rollout[:,2]
        next_observations = rollout[:,3]
        values = rollout[:,5]
        
        # Here we take the rewards and values from the rollout, and use them to 
        # generate the advantage and discounted returns. 
        # The advantage function uses "Generalized Advantage Estimation"
        self.rewards_plus = np.asarray(rewards.tolist() + [bootstrap_value])
        discounted_rewards = discount(self.rewards_plus,gamma)[:-1]
        self.value_plus = np.asarray(values.tolist() + [bootstrap_value])
        advantages = rewards + gamma * self.value_plus[1:] - self.value_plus[:-1]
        advantages = discount(advantages,gamma)

        # Update the global network using gradients from loss
        # Generate network statistics to periodically save
        feed_dict = {self.local_AC.target_v:discounted_rewards,
            self.local_AC.inputs:np.vstack(observations),
            self.local_AC.actions:actions,
            self.local_AC.advantages:advantages,
            self.local_AC.state_in[0]:self.batch_rnn_state[0],
            self.local_AC.state_in[1]:self.batch_rnn_state[1]}
        v_l,p_l,e_l,g_n,v_n, self.batch_rnn_state,_ = sess.run([self.local_AC.value_loss,
            self.local_AC.policy_loss,
            self.local_AC.entropy,
            self.local_AC.grad_norms,
            self.local_AC.var_norms,
            self.local_AC.state_out,
            self.local_AC.apply_grads],
            feed_dict=feed_dict)
        return v_l / len(rollout),p_l / len(rollout),e_l / len(rollout), g_n,v_n
        
    def test(self,max_episode_length,gamma,sess,coord,saver):
        episode_count = 0
        total_steps = 0
        # max_reward = 10
        print ("Starting tester " + str(self.number))
        #game = gsm.make(self.game)
        #self.env = BinarySpaceToDiscreteSpaceEnv(game, self.movement)
        self.env.init()
        # self.actions = np.arange(len(self.movement))
        with sess.as_default(), sess.graph.as_default():
            sess.run(self.update_local_ops)                 
            while not coord.should_stop():
                episode_buffer = []
                episode_values = []
                episode_frames = []
                episode_reward = 0
                episode_step_count = 0
                
                # reset level
                self.env.set_level(0)
                # get initial state
                state, reward, d, info = self.env.step(self.env.ACTION_MAP[random.randrange(len(self.env.ACTION_MAP))])
                s = rgb2gray(state)
                episode_frames.append(s)
                s = process_frame(s)
                rnn_state = self.local_AC.state_init
                self.batch_rnn_state = rnn_state
                d = False
                while d == False:
                    #Take an action using probabilities from policy network output.
                    a_dist,v,rnn_state = sess.run([self.local_AC.policy,self.local_AC.value,self.local_AC.state_out], 
                        feed_dict={self.local_AC.inputs:[s],
                        self.local_AC.state_in[0]:rnn_state[0],
                        self.local_AC.state_in[1]:rnn_state[1]})
                    #print("{} = {}".format("a_dist", str(a_dist)))
                    a = np.random.choice(a_dist[0],p=a_dist[0])
                    # a = np.max(a_dist[0])
                    #print("{} = {}".format("a", str(a)))
                    a = np.argmax(a_dist == a)
                    #print("{} = {}".format("a_max", str(a)))
                    # lock.acquire()
                    state, r, d, info = self.env.step(self.env.ACTION_MAP[a])
                    # lock.release()
                    #if self.name == 'worker_0':
                    #    self.env.render()
                    if d == False:
                        s1 = rgb2gray(state)
                        episode_frames.append(s1)
                        s1 = process_frame(s1)
                    else:
                        s1 = s
                    
                    # r += self.env.get_game_variable(GameVariable.HEALTH)/5000 # + self.env.get_game_variable(GameVariable.KILLCOUNT)/100 # + 
                    episode_buffer.append([s,a,r,s1,d,v[0,0]])
                    episode_values.append(v[0,0])

                    episode_reward += r
                    s = s1                    
                    total_steps += 1
                    episode_step_count += 1
                                            
                                
                print("[{}]reward:{} coins: {} score:{}".format(self.name, episode_reward, info['coins'], info['score']))

                if episode_count % 100 == 0 and episode_count != 0 and self.name == 'worker_0':
                    time_per_step = 0.05
                    images = np.array(episode_frames)
                    make_gif(images,'./A3C/frames/image_test_'+str(episode_count) + '_' + self.name + '_' + str(math.floor(episode_reward)) +'.gif',
                        duration=len(images)*time_per_step,true_image=True,salience=False)

                episode_count += 1
        self.env.close()

    def work(self,max_episode_length,gamma,sess,coord,saver):
        episode_count = sess.run(self.global_episodes)
        total_steps = 0
        # max_reward = 10
        print ("Starting worker " + str(self.number))
        #game = gsm.make(self.game)
        #self.env = BinarySpaceToDiscreteSpaceEnv(game, self.movement)
        self.summary_writer = tf.summary.FileWriter(self.summary_path, sess.graph)
        self.env.init()
        self.actions = np.arange(len(self.movement))
        with sess.as_default(), sess.graph.as_default():                 
            while not coord.should_stop():
                sess.run(self.update_local_ops)
                episode_buffer = []
                episode_values = []
                episode_frames = []
                episode_reward = 0
                episode_step_count = 0
                       
                # reset level
                self.env.set_level(0)
                # get initial state
                state, r, d, info = self.env.step(self.env.ACTION_MAP[random.randrange(len(self.env.ACTION_MAP))])
                s = rgb2gray(state)
                episode_frames.append(s)
                s = process_frame(s)
                rnn_state = self.local_AC.state_init
                self.batch_rnn_state = rnn_state
                old_s = int(info['score'])
                d = False
                while d == False:
                    #Take an action using probabilities from policy network output.
                    a_dist,v,rnn_state = sess.run([self.local_AC.policy,self.local_AC.value,self.local_AC.state_out], 
                        feed_dict={self.local_AC.inputs:[s],
                        self.local_AC.state_in[0]:rnn_state[0],
                        self.local_AC.state_in[1]:rnn_state[1]})

                    a = np.random.choice(a_dist[0],p=a_dist[0])
                    a = np.argmax(a_dist == a)

                    state, r, d, info = self.env.step(self.env.ACTION_MAP[a])

                    if d == False:
                        s1 = rgb2gray(state)
                        episode_frames.append(s1)
                        s1 = process_frame(s1)
                    else:
                        s1 = s
                    
                    # modify reword algorithm will change AI behaviors
                    #if int(info['is_dead']) == 1:
                    #    r -= 1
                    #r += (int(info['score']) - old_s)/100.0
                    old_s = int(info['score'])
                    episode_buffer.append([s,a,r,s1,d,v[0,0]])
                    episode_values.append(v[0,0])

                    episode_reward += r
                    s = s1                    
                    total_steps += 1
                    episode_step_count += 1
                    
                    # If the episode hasn't ended, but the experience buffer is full, then we
                    # make an update step using that experience rollout.
                    if len(episode_buffer) == 30 and d != True and episode_step_count != max_episode_length - 1:
                        # Since we don't know what the true final return is, we "bootstrap" from our current
                        # value estimation.
                        v1 = sess.run(self.local_AC.value, 
                            feed_dict={self.local_AC.inputs:[s],
                            self.local_AC.state_in[0]:rnn_state[0],
                            self.local_AC.state_in[1]:rnn_state[1]})[0,0]
                        v_l,p_l,e_l,g_n,v_n = self.train(episode_buffer,sess,gamma,v1)
                        episode_buffer = []
                        sess.run(self.update_local_ops)
                    if d == True:
                        break
                                            
                self.episode_rewards.append(episode_reward)
                self.episode_lengths.append(episode_step_count)
                self.episode_mean_values.append(np.mean(episode_values))
                
                # Update the network using the episode buffer at the end of the episode.
                if len(episode_buffer) != 0:
                    v_l,p_l,e_l,g_n,v_n = self.train(episode_buffer,sess,gamma,0.0)
                                
                print("[{}]reward:{} coins: {} score:{}".format(self.name, episode_reward, info['coins'], info['score']))

                # Periodically save gifs of episodes, model parameters, and summary statistics.
                if episode_count % 5 == 0 and episode_count != 0:
                    if episode_count % 1000 == 0 and self.name == 'worker_0':
                        saver.save(sess,self.model_path+'/model-'+str(episode_count)+'.cptk')
                        print ("Saved Model")

                    mean_reward = np.mean(self.episode_rewards[-5:])
                    mean_length = np.mean(self.episode_lengths[-5:])
                    mean_value = np.mean(self.episode_mean_values[-5:])
                    summary = tf.Summary()
                    summary.value.add(tag='Perf/Reward', simple_value=float(mean_reward))
                    summary.value.add(tag='Perf/Length', simple_value=float(mean_length))
                    summary.value.add(tag='Perf/Value', simple_value=float(mean_value))
                    summary.value.add(tag='Losses/Value Loss', simple_value=float(v_l))
                    summary.value.add(tag='Losses/Policy Loss', simple_value=float(p_l))
                    summary.value.add(tag='Losses/Entropy', simple_value=float(e_l))
                    summary.value.add(tag='Losses/Grad Norm', simple_value=float(g_n))
                    summary.value.add(tag='Losses/Var Norm', simple_value=float(v_n))
                    self.summary_writer.add_summary(summary, episode_count)

                    self.summary_writer.flush()

                if episode_count % 100 == 0 and episode_count != 0 and self.name == 'worker_0':
                    time_per_step = 0.05
                    images = np.array(episode_frames)
                    make_gif(images,'./A3C/frames/image'+str(episode_count) + '_' + self.name + '_' + str(math.floor(episode_reward)) +'.gif',
                        duration=len(images)*time_per_step,true_image=True,salience=False)

                    
                if self.name == 'worker_0':
                    sess.run(self.increment)

                episode_count += 1
        self.env.close()