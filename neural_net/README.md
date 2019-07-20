This folder contains the code for training and testing the neural networks used in this project. This list will grow as continue
to experiment with different network architectures and models.

The code for the NNs is written in Keras with a tensorflow backend. All training and testing was run on and will be
run on an Nvidia Quadro P6000 GPU as of (7/20/2019). I might try to convince my professor to upgrade our hardware to something
from the Volta or Turing micro-architecture if my networks become more resource-intensive.

Below will be details for each network architecture used, in reverse chronological order.

# Neural Networks

### FSRCNN (4/16/2019)

FSRCNN stands for "Fast Super-Resolution Convolutional Neural Network". The authors' page can be found here (http://mmlab.ie.cuhk.edu.hk/projects/FSRCNN.html).
This architecture can achieve high accuracy at faster speeds, and requires no data-preprocessing, as opposed to the original SRCNN
architecture, which requires the input image to be bicubically upsampled. FSRCNN is fast, accurate, and requires less work on my
part, making it an ideal choice.

![FSRCNN](readme_imgs/FSRCNN.png)
