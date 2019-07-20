This folder contains some gifs I made from the matplotlib plots from various points in this project.

### 2D gifs

The input gif represents the lowres data fed into the CNN for SR, and the truth gif represents the ideal desired output from the CNN.

|![input gif](gifs/input_fsrcnn.gif)|![output gif](gifs/truth_fsrcnn.gif)|
|-|-|

The other gifs are outputs from different iterations of the CNN. The progression through time can be seen clearly.

|![1](gifs/neuralnet_fsrcnn%20Tue_Apr_16_13-41-30_2019.gif)|![2](gifs/neuralnet_fsrcnn%20Tue_Apr_16_14-03-18_2019.gif)|
![3](gifs/neuralnet_fsrcnn%20Tue_Apr_16_14-07-46_2019.gif)|
|-|-|-|

|![4](gifs/neuralnet_fsrcnn.gif)|![1](gifs/neuralnet.gif)|![5](gifs/neuralnet_fsrcnn%20Tue_Apr_16_14-12-14_2019.gif)|
|-|-|-|

The other gifs here include: a gif of bicubic upsampling, which actually had a higher MSE value than the CNN output (left).
and a CNN output that looks "blockier" compared to the others (right).


|![bicubic](gifs/bicubic_fsrcnn.gif)|![minecraft steve](gifs/neuralnet_fsrcnn%20Tue_Apr_16_14-40-16_2019.gif)|
|-|-|

### 3D gifs
These gifs were made by extending OpenFOAM's dambreak to 3 dimensions. Each block was extended in the Z direction but the results
were not as expected. The original plan was to make a network for 3D CFD sims but this has been put on hold as of summer 2019.
You can see that the fluid behavior is kind of strange in alpha.water.gif. (left). The other two are p (middle) and p_rgh (right).


|![alpha.water](gifs/alpha.water3D.gif)|![p](gifs/p3D.gif)|![p_rgh](gifs/p_rgh3D.gif)|
|-|-|-|
