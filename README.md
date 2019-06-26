# SRCFD
#### Matthew Li
mwl5628@psu.edu

Hello there! 

This repo contains all the components for a Super Resolution in Computation Fluid Dynamics project, with data processing as well
as network training and testing. CFD is very important in the field of engineering, but solving CFD problems can be very computationally
intensive. It is a problem that cannot be easily scaled to more CPU or GPU cores making it very difficult to parallelize. This project
proposes a novel method of solving CFD problems by applying a neural network super-resolution to lower resolution CFD simulations.


### OpenFOAM

![alt text](https://github.com/matthewli125/SRCFD/blob/master/readme_imgs/openfoam.png "OpenFOAM")

CFD data was gathered from simulations run in the OpenFOAM software platform. The data used in this project comes from the OpenFOAM dambreak tutorial (https://cfd.direct/openfoam/user-guide/v6-dambreak/), which was modified to have uniform point density as well as randomized fluid properties.

#### OpenFOAM file format
The most essential files for an OpenFOAM simulation are the blockMeshDict, controlDict, as well as g, transportProperties, and turbulenceProperties. blockMeshDict defines the geometry of the simulation, controlDict defines the time properties, and other 3 modify
fluid properties. An example folder has been included that contains all of these files and more.

#### BlockMeshDict
The geometry of an OpenFOAM simulation is made up of rectangular blocks, defined by a set of vertices. Each block contains a set of vertices as well and a point density.

Vertices List for a sample blockMeshDict

![alt text](https://github.com/matthewli125/SRCFD/blob/master/readme_imgs/vertices.png "Vertices List")

Block List for a sample blockMeshDict

![alt text](https://github.com/matthewli125/SRCFD/blob/master/readme_imgs/blocks.png "Block List")

Each block consists of a set of vertices and a set of block densities for the x,y,z directions.

#### Data
The data comes from files in each timestep directory that the solver produces. This comes in the form of a list of points that must
be assembled from left to right, bottom to top. This makes the assembly slightly more complicated.

For example, if we had a block of 8 points, it would be assembled like this:

![alt text](https://github.com/matthewli125/SRCFD/blob/master/readme_imgs/block example.png "Block Example")


Each case was ran for 5 seconds, with timesteps of 0.05, and both a highres and lowres version. 400
different cases were ran, each with two versions of 101 data points each, resulting in 80,800 total data points.
