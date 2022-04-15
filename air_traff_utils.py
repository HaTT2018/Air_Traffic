import numpy as np
import os
import random
import torch


def mape_loss_func(preds, labels, m):
    mask = preds > m
    return np.mean(eliminate_nan(np.fabs(labels[mask]-preds[mask])/labels[mask]))


def smape_loss_func(preds, labels, m):
    mask = preds > m
    return np.mean(2*np.fabs(labels[mask]-preds[mask])/(np.fabs(labels[mask])+np.fabs(preds[mask])))


def mae_loss_func(preds, labels, m):
    mask = preds > m
    return np.mean(np.fabs((labels[mask]-preds[mask])))


def nrmse_loss_func(preds, labels, m):
    mask = preds > m
    return np.sqrt(np.sum((preds[mask] - labels[mask])**2)/preds[mask].flatten().shape[0])/(labels[mask].max() - labels[mask].min())


def nmae_loss_func(preds, labels, m):
    mask = preds > m
    return np.mean(np.fabs((labels[mask]-preds[mask]))) / (labels[mask].max() - labels[mask].min())


def eliminate_nan(b):
    a = np.array(b)
    c = a[~np.isnan(a)]
    c = c[~np.isinf(c)]
    return c


def normalize2D_tSNE(V):
    V = np.array(V)
    return ( V ) / ( V.max(0) - V.min(0) ), V.min(0), V.max(0)


def normalize2D(V):
    V = np.array(V)
    return ( V - V.min(0) ) / ( V.max(0) - V.min(0) ), V.min(0), V.max(0)


def denormalize2D(V, V_min, V_max):
    V = np.array(V)
    V_min = np.array(V_min)
    V_max = np.array(V_max)
    denormalized_V = V * (V_max - V_min) + V_min
    return denormalized_V


def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)    
    torch.backends.cudnn.deterministic = True
    np.random.seed(seed)
    random.seed(seed)


def save_model(net, name):
    num_fold = get_num_fold() + 1
    try:
        torch.save(net.state_dict(), './runs/run%i/%s.pth'%(num_fold, name))
    except:
        raise RuntimeError('No fold for this experiment created')


def get_num_fold():
    num_fold = len(next(iter(os.walk('./runs/')))[1])
    return num_fold
