# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 09:42:18 2018

@author: xiandong
"""

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 卷积池化层模板
def conv_pool(tensor, m, n, nw="WC", nb="BC"):
    """
        [5,5,m,n]：5,5表示卷积核大小，m表示通道数,例如RGB是3通道，n为卷积核的数量
        tf.nn.conv2d(x, w)：x是输入，w是参数
        strides：卷积核移动的步长，padding="SAME"：数据补0以确保输入和输出图像的尺寸一致
    """
    W_conv = tf.Variable(tf.truncated_normal([5,5,m,n], stddev=0.1, seed=1024), name=nw)
    b_conv = tf.Variable(tf.constant(0.1, shape=[n]), name=nb)
    h_conv = tf.nn.relu(tf.nn.conv2d(tensor, W_conv, strides=[1,1,1,1], padding="SAME") + b_conv)
    h_pool = tf.nn.max_pool(h_conv, ksize=[1,2,2,1], strides=[1,2,2,1], padding="SAME")
    return h_pool

def addLayer(X, n, scope, activation=None):
    with tf.variable_scope(scope):
        m = X.get_shape().as_list()[-1]
        w = tf.Variable(tf.truncated_normal([m,n], stddev=0.1, seed=1024), name="W")
        b = tf.Variable(tf.constant(0.1, shape=[n]), name="B")
        s = tf.matmul(X, w) + b
        if activation:
            return activation(s)
        else:
            return s

def LeNet5(mnist, epochs=3001, rate=1e-4):
    curve = []
    x = tf.placeholder(tf.float32, [None,250,250])
    y = tf.placeholder(tf.float32, [None,10])
    # 定义第一个卷积池化层
    # 由于输入的image数据是1D的，而CNN要求输入具有2D，因而将原始数据784转成28*28
    x_2d = tf.reshape(x, [-1,28,28,1])
    cp1 = conv_pool(x_2d, 1, 32)
    # 定义第二个卷  积池化层
    cp2 = conv_pool(cp1, 32, 64)
    # 定义密集连接层
    # 将2D转成1D，经过两次池化，图像由28*28变成7*7，卷积核数量为64
    cp2_1d = tf.reshape(cp2, [-1, 7*7*64])
    d1 = addLayer(cp2_1d, 1024, "d1", activation=tf.nn.relu)
    d2 = addLayer(d1, 256, "d2", activation=tf.nn.relu)
    d3 = addLayer(d2, 64, "d3", activation=tf.nn.relu)
    pred = addLayer(d3, 10, "pred", activation=tf.nn.softmax)
    # 定义损失函数
#    loss = -tf.reduce_sum(y*tf.log(pred))
    loss = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=[1]))
#    loss = tf.reduce_mean(tf.contrib.losses.hinge_loss(pred, labels=y))
    train = tf.train.AdamOptimizer(rate).minimize(loss)
    with tf.device("/cpu:0"):
        with tf.Session() as sess:
            # 系统参数初始化，必不可少
            sess.run(tf.global_variables_initializer())
            for i in range(epochs):
                # sess.run表示开始计算，在计算公式中存在未知量时，可加入feed_dict作为数据入口
                batch = mnist.train.next_batch(64)
                sess.run(train, feed_dict={x:batch[0], y:batch[1]})
                if i % 100 == 0:
                    # curve存储目标函数(loss)变化趋势：迭代次数和loss值
                    curve.append([i, sess.run(loss, feed_dict={x:batch[0], y:batch[1]})])
                    print(curve[-1])
            curve = pd.DataFrame(curve, columns=["epoch", "loss"])
            pred = sess.run(pred, feed_dict={x:mnist.test.images})
    return pred, curve

if __name__ == "__main__":
    path = "./mnist"
    mnist = input_data.read_data_sets(path, one_hot=True)
    pred, curve = LeNet5(mnist)
    plt.plot(curve["epoch"], curve["loss"])
    plt.show()
    with tf.Session() as sess:
        accuracy = tf.contrib.metrics.accuracy(tf.argmax(pred, 1), tf.argmax(mnist.test.labels, 1))
        print("测试集准确率为:", sess.run(accuracy))

