from gan import Generator, Discriminator
from foam_case_class import Foam_Case
import random
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tqdm import tqdm
from os import listdir
import numpy as np

from loss_functions import master_loss

import tensorflow as tf

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

data_file = "gan_data.h5"
np.random.seed(10)
epochs = 1
model_save_dir = "gan models"

# Remember to change image shape if you are having different size of images
image_shape = (16,16,1)
image_shape_scaled = (64,64,1)

lr_res = (16,16,1)
hr_res = (64,64,1)

adam = Adam(lr=1E-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

def get_data(ratio):
    lr_data_path = "E:/gan_data/ground_only/phase_only/lowres/"
    hr_data_path = "E:/gan_data/ground_only/phase_only/highres/"

    print("loading data into memory")

    lr_data = np.array([np.load(lr_data_path + i) for i in tqdm(listdir(lr_data_path)[:5000])])
    hr_data = np.array([np.load(hr_data_path + i) for i in tqdm(listdir(hr_data_path)[:5000])])

    print(hr_data[1].shape)

    index = int(len(lr_data) * ratio)

    return lr_data[:index], hr_data[:index], lr_data[index:], hr_data[index:]


def get_gan_network(discriminator, generator, optimizer):
    discriminator.trainable = False
    gan_input = Input(shape = image_shape)
    x = generator(gan_input)
    gan_output = discriminator(x)
    gan = Model(inputs=gan_input, outputs=[x,gan_output])
    gan.compile(loss=[master_loss, "binary_crossentropy"],
                loss_weights=[1., 1e-10],
                optimizer=optimizer)

    return gan

def train(epochs, batch_size, data_split_ratio):
    x_train_lr, x_train_hr, x_test_lr, x_test_hr = get_data(data_split_ratio)
    batch_count = int(x_train_hr.shape[0] / batch_size)

    generator = Generator(image_shape).generator()
    generator._name = "generator"
    discriminator = Discriminator(image_shape_scaled).discriminator()
    generator.compile(loss=master_loss, optimizer=adam)

    discriminator.compile(loss="binary_crossentropy", optimizer=adam)

    print(generator.summary())
    print(discriminator.summary())

    gan = get_gan_network(discriminator, generator, adam)


    for e in range(1,epochs+1):
        print ('-'*15, 'Epoch %d' % e, '-'*15)
        for batch in tqdm(range(batch_count)):

            rand_nums = np.random.randint(0, x_train_hr.shape[0], size=batch_size)

            image_batch_hr = x_train_hr[rand_nums]
            image_batch_lr = x_train_lr[rand_nums]
            generated_images_sr = generator.predict(image_batch_lr)

            real_data_Y = np.ones(batch_size) - np.random.random_sample(batch_size)*0.2
            fake_data_Y = np.random.random_sample(batch_size)*0.2

            discriminator.trainable = True

            d_loss_real = discriminator.train_on_batch(image_batch_hr, real_data_Y)
            d_loss_fake = discriminator.train_on_batch(generated_images_sr, fake_data_Y)
            discriminator_loss = 0.5 * np.add(d_loss_fake, d_loss_real)

            rand_nums = np.random.randint(0, x_train_hr.shape[0], size=batch_size)
            image_batch_hr = x_train_hr[rand_nums]
            image_batch_lr = x_train_lr[rand_nums]

            gan_Y = np.ones(batch_size) - np.random.random_sample(batch_size)*0.2
            discriminator.trainable = False
            gan_loss = gan.train_on_batch(image_batch_lr, [image_batch_hr,gan_Y])

        print("discriminator_loss : %f" % discriminator_loss)
        print("gan_loss :", gan_loss)
        gan_loss = str(gan_loss)

        loss_file = open(model_save_dir + 'losses.txt' , 'a')
        loss_file.write('epoch%d : gan_loss = %s ; discriminator_loss = %f\n' %(e, gan_loss, discriminator_loss) )
        loss_file.close()

    generator.save_weights("generator_weights_physics")
    discriminator.save_weights("discriminator_weights_physics")

def get_data_paths(path):

    print("FETCHING DATA PATHS...")

    def sortbynum(nums):
        return sorted(nums, key = lambda x: float(x.split("_")[0]))

    #this sorts all the directories in the path; each of these directories
    #is an openfoam case that has subdirectories for timesteps
    lowres = sortbynum([i for i in listdir(path) if "highres" not in i])
    highres = sortbynum([i for i in listdir(path) if "highres" in i])
    data = list(zip(lowres, highres))

    def expand(paths):
        all_sub_paths = []
        isnum = lambda x: x[0].isdigit() and float(x) != 0
        for i in tqdm(paths):
            times = sortbynum(list(filter(isnum, listdir("".join([path,"/",i])))))
            sub_paths = ["".join([path,"/",i,"/",timestep]) for timestep in times]
            all_sub_paths+=sub_paths

        return all_sub_paths

    lowres_expanded = expand(lowres)
    highres_expanded = expand(highres)

    print("DATA PATHS FETCHED")

    return list(zip(lowres_expanded, highres_expanded))


#this helper function loads the data from a given list of file directories. This
#allows the data to be loaded and unloaded on the fly, making the operation more
#memory efficient.
def load_data_batch_unbuilt(batch, res, type):
    return np.array([Foam_Case(res, file_path, type).fetch().enum() for file_path in tqdm(batch)])

# def load_data_batch(num, res, type):
#     if type == "lowres":
#         return np.load("E:/gan_data/lowres/%d.npy" % num[0])
#     else:
#         return np.load("E:/gan_data/highres/%d.npy" % num[0])

def load_data_batch(nums, res, type):
    if type == "lowres":
        return np.array([np.load("E:/gan_data/lowres_downsample/%d.npy" % i) for i in nums])
    else:
        return np.array([np.load("E:/gan_data/highres_single/%d.npy" % i) for i in nums])
#this helper function takes a loaded list of data files and deletes them, freeing
#memory.
def unload_data_batch(batch):
    [foam_case.crunch() for foam_case in batch]

def train_mem_efficient(epochs, batch_size, data_split_ratio):
    path = "E:/dambreak_cases4"
    lr_res = (16,16,1)
    hr_res = (64,64,1)

    x_train_hr = x_train_lr = np.array(range(48000))

    batch_count = int(x_train_hr.shape[0] / batch_size)


    generator = Generator(image_shape).generator()
    discriminator = Discriminator(image_shape_scaled).discriminator()
    generator.compile(loss=master_loss, optimizer=adam)
    discriminator.compile(loss="binary_crossentropy", optimizer=adam)

    gan = get_gan_network(discriminator, generator, adam)


    for e in range(1,epochs+1):
        print ('-'*15, 'Epoch %d' % e, '-'*15)
        for batch in tqdm(range(batch_count)):

            # rand_nums = np.random.randint(0, x_train_hr.shape[0], size=1) #keep size as 1 for now; each file has 60 data points
            rand_nums = np.random.randint(0, x_train_hr.shape[0], size=batch_size)
            image_batch_hr = load_data_batch(x_train_hr[rand_nums], hr_res, "highres")
            image_batch_lr = load_data_batch(x_train_lr[rand_nums], lr_res, "lowres")
            generated_images_sr = generator.predict_on_batch(image_batch_lr)

            real_data_Y = np.ones(batch_size) - np.random.random_sample(batch_size)*0.2
            fake_data_Y = np.random.random_sample(batch_size)*0.2

            discriminator.trainable = True

            d_loss_real = discriminator.train_on_batch(image_batch_hr, real_data_Y)
            d_loss_fake = discriminator.train_on_batch(generated_images_sr, fake_data_Y)
            discriminator_loss = 0.5 * np.add(d_loss_fake, d_loss_real)

            rand_nums = np.random.randint(0, x_train_hr.shape[0], size=batch_size)
            image_batch_hr = load_data_batch(x_train_hr[rand_nums], hr_res, "highres")
            image_batch_lr = load_data_batch(x_train_lr[rand_nums], lr_res, "lowres")

            gan_Y = np.ones(batch_size) - np.random.random_sample(batch_size)*0.2
            discriminator.trainable = False
            gan_loss = gan.train_on_batch(image_batch_lr, [image_batch_hr,gan_Y], return_dict=True)

        print("discriminator_loss : %f" % discriminator_loss)
        print("gan_loss :", gan_loss)
        gan_loss = str(gan_loss)

        loss_file = open(model_save_dir + 'losses.txt' , 'a')
        loss_file.write('epoch%d : gan_loss = %s ; discriminator_loss = %f\n' %(e, gan_loss, discriminator_loss) )
        loss_file.close()


    generator.save_weights("E:/gan_data/generator_weights_phase_only")
    discriminator.save_weights("E:/gan_data/discriminator_weights_phase_only")

if __name__ == "__main__":
    train(epochs=1000, batch_size=16, data_split_ratio=0.8)

    # from keras.models import load_model
    #
    # model = load_model("gan modelsdis_model2000.h5")
    # result = model.predict(np.load("E:/gan_data/lowres/50.npy"))
