from gan import Generator, Discriminator
from loss_functions import *
from foam_case_class import Foam_Case
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tqdm import tqdm
import numpy as np
import cv2
from loss_functions import master_loss, MSE

import tensorflow as tf
import matplotlib.pyplot as plt

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

image_shape = (16,16,1)
image_shape_scaled = (64,64,1)

lr_res = (16,16,1)
hr_res = (64,64,1)

adam = Adam(lr=1E-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

def plot_comparison(gen1, gen2):
    cases = np.random.choice(listdir("E:/gan_data/ground_only/phase_only/lowres/")[5000:], 1000, replace=False)
    
    cases = [
        "40552.npy",
        "22078.npy",
        "23555.npy",
        "22139.npy",
        "46791.npy"
    ]
    
    labs = ["A", "B", "C", "D", "E"]
    i = 0
    
    for case in cases:
    
        input = np.array([np.load("E:/gan_data/ground_only/phase_only/lowres/%s" % case)])
        outputMSEphysics = gen1.predict(input)
        outputMSEonly = gen2.predict(input)
        real = np.load("E:/gan_data/ground_only/phase_only/highres/%s" % case)
    
        cubic = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_CUBIC)
        linear = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_LINEAR)
        nearest = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_NEAREST)
    
        fig,ax = plt.subplots(nrows=1, ncols=6, figsize=(18,3))
    
        im1 = ax[0].imshow(np.squeeze(input), vmin=0, vmax=1)
        im2 = ax[1].imshow(cubic, vmin=0, vmax=1)
        im3 = ax[2].imshow(linear, vmin=0, vmax=1)
        im4 = ax[3].imshow(np.squeeze(outputMSEonly), vmin=0, vmax=1)
        im5 = ax[4].imshow(np.squeeze(outputMSEphysics), vmin=0, vmax=1)
        im6 = ax[5].imshow(np.squeeze(real), vmin=0, vmax=1)
    
        ax[0].set_title("input")
        ax[1].set_title("linear")
        ax[2].set_title("bicubic")
        ax[3].set_title("GAN MSE only")
        ax[4].set_title("GAN MSE + physics")
        ax[5].set_title("ground truth")
    
        ax[0].set_xlabel("(%sA)" % labs[i])
        ax[1].set_xlabel("(%sB)" % labs[i])
        ax[2].set_xlabel("(%sC)" % labs[i])
        ax[3].set_xlabel("(%sD)" % labs[i])
        ax[4].set_xlabel("(%sE)" % labs[i])
        ax[5].set_xlabel("(%sF)" % labs[i])
    
        i+=1
    
        fig.colorbar(im1, fraction=0.046, ax=ax[0], pad=0.04)
        fig.colorbar(im2, fraction=0.046, ax=ax[1], pad=0.04)
        fig.colorbar(im3, fraction=0.046, ax=ax[2], pad=0.04)
        fig.colorbar(im4, fraction=0.046, ax=ax[3], pad=0.04)
        fig.colorbar(im5, fraction=0.046, ax=ax[4], pad=0.04)
        fig.colorbar(im6, fraction=0.046, ax=ax[5], pad=0.04)
    
        fig.tight_layout()
    
        plt.show()


def make_violinplot(gen1, gen2):
    cases = np.random.choice(listdir("E:/gan_data/ground_only/phase_only/lowres/")[5000:], 10000, replace=False)

    losses = {"nearest": [], "bicubic": [], "linear":[], "model MSE only":[], "model MSE + physics": []}
    losses_physics = {"nearest": [], "bicubic": [], "linear":[], "model MSE only":[], "model MSE + physics": []}

    for case in tqdm(cases):

    input = np.array([np.load("E:/gan_data/ground_only/phase_only/lowres/%s" % case)])
    outputMSEphysics = gen1.predict(input).astype("float64")
    outputMSEonly = gen2.predict(input).astype("float64")
    real = tf.convert_to_tensor(np.load("E:/gan_data/ground_only/phase_only/highres/%s" % case))

    cubic = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_CUBIC)
    linear = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_LINEAR)
    nearest = cv2.resize(np.squeeze(input), (64,64), interpolation = cv2.INTER_NEAREST)


    losses["nearest"].append(MSE(nearest, real).numpy())
    losses["bicubic"].append(MSE(cubic, real).numpy())
    losses["linear"].append(MSE(linear, real).numpy())
    losses["model MSE only"].append(MSE(outputMSEonly, real).numpy())
    losses["model MSE + physics"].append(MSE(outputMSEphysics, real).numpy())


    losses_physics["nearest"].append(master_loss(nearest, real).numpy())
    losses_physics["bicubic"].append(master_loss(cubic, real).numpy())
    losses_physics["linear"].append(master_loss(linear, real).numpy())
    losses_physics["model MSE only"].append(master_loss(outputMSEonly, real).numpy())
    losses_physics["model MSE + physics"].append(master_loss(outputMSEphysics, real).numpy())


    fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize =(6,12))

    v1 = ax[0].violinplot([losses[i] for i in losses])
    ax[0].set_yscale('log')
    ax[0].set_title("Comparison of Loss Values on pure MSE")

    v2 = ax[1].violinplot([losses_physics[i] for i in losses_physics])
    ax[1].set_yscale('log')
    ax[1].set_title("Comparison of Loss values on MSE + Physics")

    labels = ['Nearest Neighbor', 'Bicubic', 'Linear', 'GAN MSE only', 'GAN MSE + physics']

    def set_axis_style(ax, labels):
        ax.get_xaxis().set_tick_params(direction='out')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks(np.arange(1, len(labels) + 1))
        ax.set_xticklabels(labels, rotation = 55)
        ax.set_xlim(0.25, len(labels) + 0.75)

    for i in [ax[0],ax[1]]:
        set_axis_style(i, labels)


    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    from os import listdir
    from tqdm import tqdm

    dir = "E:/gan_data/ground_only/phase_only/"
    save_dir = "E:/gan_data/outputs/"


    generatorMSE = Generator(image_shape).generator()
    generatorMSE.compile(loss="MSE", optimizer=adam)
    generatorMSE.load_weights("MSE_only_weights/generator_weights")

    generatorMSEphysics = Generator(image_shape).generator()
    generatorMSEphysics.compile(loss="MSE", optimizer=adam)
    generatorMSEphysics.load_weights("MSE+physics_weights/generator_weights_physics")

    plot_comparison(generatorMSEphysics, generatorMSE)
    make_violinplot(generatorMSEphysics, generatorMSE)