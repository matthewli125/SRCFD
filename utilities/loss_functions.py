import numpy as np
import tensorflow.keras.backend as K
import tensorflow as tf

# this loss function calculates the difference between the sums of the phase
# fractions of two single dambreak frames. Because the interFoam solver solves
# for incompressible fluids, meaning the amount of fluid should remain constant
# with time.
def phase_fraction_loss(y_true, y_pred):
    # alpha_true_sum = tf.math.reduce_sum(tf.unstack(y_true, axis=-1)[0])
    # alpha_pred_sum = tf.math.reduce_sum(tf.unstack(y_pred, axis=-1)[0])
    alpha_true_sum = tf.math.reduce_sum(y_true)
    alpha_pred_sum = tf.math.reduce_sum(y_pred)

    size = 64 * 64

    # print(y_true.shape, y_pred.shape)
    # print(alpha_true_size, alpha_pred_size)

    return (alpha_true_sum/size - alpha_pred_sum/size)**2


def phase_magnitude_loss(y_true, y_pred):
    alpha_pred_max = tf.math.reduce_max(tf.unstack(y_pred, axis=-1)[0])
    alpha_pred_min = tf.math.reduce_min(tf.unstack(y_pred, axis=-1)[0])

    return (1 - alpha_pred_max)**2 + alpha_pred_min**2

def MSE_phase_only(y_true, y_pred):
    return tf.reduce_mean(tf.math.squared_difference(tf.unstack(y_true, axis=-1)[0], tf.unstack(y_pred, axis=-1)[0]))

def MSE(y_true, y_pred):
    # print(tf.reduce_mean(tf.math.squared_difference(y_true,y_pred)))
    return tf.reduce_mean(tf.math.squared_difference(y_true,y_pred))


#helper function that gets the velocity divergence for a given input. This function
#assumes 2D data for now, but this can be easily expanded upon in the future.
def divU(input):
    Ux = input[2]
    Uy = input[3]
    dUx_dx = np.gradient(Ux)[0]
    dUy_dy = np.gradient(Uy)[1]

    return dUx_dx + dUy_dy

def divU_tf(input):
    Ux = input[2]
    Uy = input[3]
    return tf.math.reduce_mean(ddx(Ux))

import tqdm as tqdm

@tf.function
def ddy(arr):
    arrK = np.zeros((len(arr),len(arr)))
    for i in tqdm(range(len(arr))):
        for j in range(len(arr[0])):
            if j == 0:
                arrK[i][j] = arr[i][j+1] - arr[i][j]
            elif j == len(arr)-1:
                arrK[i][j] = arr[i][j] - arr[i][j-1]
            else:
                arrK[i][j] = (arr[i][j+1] - arr[i][j-1])/2


    return tf.convert_to_tensor(arrK, dtype=tf.float32)

@tf.function
def foo(arr,i,j):
    if i == 0:
        return arr[i+1][j] - arr[i][j]
    elif i == len(arr)-1:
        return arr[i][j] - arr[i-1][j]
    else:
        return (arr[i+1][j] - arr[i-1][j])/2

@tf.function
def ddx(arr):
    arrK = [[tf.Variable(0,dtype=tf.float32) for i in range(len(arr))] for j in range(len(arr))]
    print(len(arrK))
    for i in tqdm.tqdm(range(len(arr))):
        for j in range(len(arr[0])):
            arrK[i][j].assign(foo(arr,i,j))
            # if j == 0:
            #     arrK[i][j] = arrK[i][j].assign(arr[i+1][j] - arr[i][j])
            # elif i == len(arr)-1:
            #     arrK[i][j] = arrK[i][j].assign(arr[i][j] - arr[i-1][j])
            # else:
            #     arrK[i][j] = arrK[i][j].assign((arr[i+1][j] - arr[i-1][j])/2)


    return arrK

#this loss function calculates the difference between the sum of the divergence
#values for the velocities. The divergence should ideally be zero, so minimizing
#the divergence sums should be a goal of the model.
def div_loss(y_true, y_pred):
    return (divU_tf(y_true) - divU_tf(y_pred))**2

    # print(y_true.shape, y_pred.shape)
    # loss_func = lambda x,y: (divU_tf(x) - divU_tf(y))**2
    # return [loss_func(y_true[i],y_pred[i]) for i in range(len(y_true))]


def interFoam_loss(y_true, y_pred):
    return


def master_loss(y_true, y_pred):
    # return MSE(y_true, y_pred)*1e-11 + phase_fraction_loss(y_true, y_pred)*1e-6
    # print(y_true.shape)
    # elems = (y_true, y_pred)
    #
    # loss_func = lambda elem: MSE_phase_only(elem[0], elem[1])
    # # loss_func =lambda elem: div_loss(elem[0],elem[1])
    # return tf.map_fn(loss_func, elems, dtype=tf.float32)

    # losses = [0 for i in range(len(y_true))]
    # for i in range(len(y_true)):
    #     # losses[i] = (phase_fraction_loss(y_true[i], y_pred[i]), MSE(y_true[i], y_pred[i]))
    #     losses[i] = phase_fraction_loss(y_true[i], y_pred[i])*1e-6 + MSE(y_true[i], y_pred[i])*1e-11
    #
    # return tf.reduce_sum(losses)
    #
    # return phase_fraction_loss(y_true, y_pred)# + tf.keras.losses.MSE(y_true, y_pred)
    # return phase_fraction_loss(y_true, y_pred) * 1e-9 + div_loss(y_true, y_pred)

    lambda1 = 0.85
    lambda2 = 0.15


    return lambda1*MSE(y_true, y_pred) + lambda2*phase_fraction_loss(y_true, y_pred)


def loss_demo():
    import matplotlib.pyplot as plt
    from foam_case_class import Foam_Case

    lr_path = "D:/openfoamData/dambreak_cases4/32/1.05"
    hr_path = "D:/openfoamData/dambreak_cases4/32_highres/1.05"

    lr_case = np.squeeze(np.array(np.split(Foam_Case((32,32,1), lr_path, "lowres").fetch().enum(),5,axis=-1)))
    hr_case = np.squeeze(np.array(np.split(Foam_Case((64,64,1), hr_path, "highres").fetch().enum(),5,axis=-1)))

    Ux = hr_case[2]
    Uy = hr_case[3]

    dUx_dx = np.gradient(Ux)[0]
    dUy_dy = np.gradient(Uy)[1]
    divU = dUx_dx + dUy_dy

    print(np.linalg.norm(divU))
    print(np.sum(divU))


    fig, ax = plt.subplots(nrows=2,ncols=3)

    ax[0][0].imshow(Ux)
    ax[0][1].imshow(Uy)
    ax[0][2].imshow(Ux+Uy)
    ax[1][0].imshow(dUx_dx)
    ax[1][1].imshow(dUy_dy)
    ax[1][2].imshow(divU)

    plt.show()

def div_tests():
    arr = tf.convert_to_tensor(np.random.randint(10,size =(512,512)),dtype=tf.float32)
    arrgradx = np.gradient(arr)[0]
    arrgrady = np.gradient(arr)[1]
    arrgradxtf = ddx(arr)
    arrgradytf = ddy(arr)
    print(arr)
    print("arrgradx == arrgradxtf", K.equal(arrgradx, arrgradxtf))
    print("arrgrady == arrgradytf", K.equal(arrgrady, arrgradytf))

if __name__ == "__main__":
    data1 = np.load("E:/gan_data/highres/440.npy")
    data2 = np.load("E:/gan_data/highres/444.npy")
    losses = master_loss(data1, data2)

    # for i in losses:
    #     print(i)
