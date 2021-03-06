# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:23:20 2021

@author: xinying-zheng
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

def getData(filename, labels):
    """
    Parameters
    ----------
    filename : str
        csv file.
    labels : list
        classes e.g. [0, 1] for LR.

    Returns
    -------
    X : np.array
        data each row is 784 feature vector.
    Y : np.array
        labels e.g. [0s,1s] for LR.
    splits : list
        the split of classes.

    """
    print('loading data ...')
    df = pd.read_csv(filename)
    X = []
    Y = []
    splits = []
    for i, label in enumerate(labels):
        rows = np.where(df['label'] == label)  #will find the row index for lable 
        
        data = np.array([df.iloc[row][1:].tolist() for row in rows[0]])
        X = np.vstack((X, data)) if i > 0 else data
        Y = np.hstack((Y, np.array([label-1] * data.shape[0]))) if i > 0 \
            else np.array([label-1] * data.shape[0])
        splits.append(X.shape[0])
    
    X = X / 255
    print('finish loading ...')
    return X, Y, splits


def sigmoid(x):
    # this func. can generate a 'sigmoid array' for x array, not the single x value.
    """
    Parameters
    ----------
    x : np.array
        X.dot(W).

    Returns
    -------
    np.array
        sigmoid value.

    note:
        To avoid overflow (for too small or large np.exp(i))
    """
    # because the objective function of logistics regression can be formulated by a sigmoid func.
    return np.array([np.exp(i) / (1 + np.exp(i)) if i < 0 else 1 / (1 + np.exp(-i)) for i in x])

def Ew(X, W, Y):
    """
    Parameters
    ----------
    X : np.array
        data.
    W : np.array
        weight.
    Y : np.array
        labels.

    Returns
    -------
    float
        error.

    """
    with np.errstate(divide='ignore'):
        y = predict(X, W)
        
        res1 = np.log(y)
             
        res2 = np.log(1-y)

    res1[np.isneginf(res1)] = 0.0
    res2[np.isneginf(res2)] = 0.0
    # The above code set the negative infinity to zero.
    return -(Y.dot(res1) + (1-Y).dot(res2))

def gradient(X, W, Y):
    return (sigmoid(X.dot(W)) - Y).T.dot(X)

def predict(X, W):

    return sigmoid(X.dot(W))

def confusion_M(X, W, Y):
    n = X.shape[0]
    predictions = predict(X, W)
    predictions = (np.round(predictions))
    res = np.zeros((2, 2))
    for i in range(n):
        # cout the number of "0->0", "0->1", "1->1" and "1->0"
        res[int(predictions[i])][int(Y[i])] += 1
    
    return res

def plot_M(M, title):
    f, ax = plt.subplots()
    sn.heatmap(M, annot=True, ax=ax)
    ax.set_title(title)

    
def logistics_regression(X, Y, X_test, Y_test, lr = 1e-4, iterations=100):
    feature_len = X.shape[1]
    W = np.zeros(feature_len)
    loss = []
    
    # gradient decent
    for i in range(iterations):
        loss.append(Ew(X, W, Y))
        print('{} th iteration : [loss : {:.3}]'.format(i, loss[-1]))
        W -= lr * gradient(X, W, Y)
    
    plt.figure()
    plt.plot(loss)
    plt.show()
    
    print('testing : [loss : {:.3}]'.format(Ew(X_test, W, Y_test)))
    
    # plot confusion matrix
    M_train = confusion_M(X, W, Y)
    M_test = confusion_M(X_test, W, Y_test)
    
    plot_M(M_train, 'On training set')
    plot_M(M_test, 'On testing set')

# this LDA implementation is based on fisher's discrimination of projection 
# and not used in this assignment
def LDA(X, Y, split_train, X_test, Y_test, split_test, dim=2, colors=['blue', 'red', 'yellow']):
    feature_len = X.shape[1]
    mean_all = np.mean(X, axis=0)
    S_t = (X - mean_all).T.dot(X - mean_all)
    
    S_w = np.zeros((feature_len, feature_len))
    begin = 0
    for end in split_train:
        X_i = X[begin:end]
        mean_i = np.mean(X_i, axis=0)
        S_w += (X_i - mean_i).T.dot(X_i - mean_i)
        begin = end
        
    S_b = S_t - S_w
    
    #return S_w, S_b
    eigenvalue, eigenvector = np.linalg.eig(np.linalg.pinv(S_w).dot(S_b))
    idx = np.argsort(eigenvalue)[-dim:]
    projection = X.dot(eigenvector[:, idx]).astype(np.float64)
    
    begin = 0
    plt.figure()
    for i, end in enumerate(split_train):
        plt.scatter(projection[begin:end, 0], projection[begin:end, 1], c=colors[i])
        begin = end
    
    return projection

if __name__ == '__main__':
    X, Y, split_train = getData('train.csv', [1, 2])
    X_test, Y_test, split_test = getData('test.csv', [1, 2])
    logistics_regression(X, Y, X_test, Y_test)
    
    # this part for LDA dimension reduction and visualization
# =============================================================================
#     X, Y, split_train = getData('train.csv', [0, 1, 2])
#     X_test, Y_test, split_test = getData('test.csv', [0, 1, 2])
#     LDA(X, Y, split_train, X_test, Y_test, split_test)
# =============================================================================



