# SRCFD
#### Matthew Li
mwl5628@psu.edu

Hello! 

This repo contains all the components for a Super Resolution in Computation Fluid Dynamics project, with data processing as well
as network training and testing. CFD is very important in the field of engineering, but solving CFD problems can be very computationally
intensive. It is a problem that cannot be easily scaled to more CPU or GPU cores making it very difficult to parallelize. This project
proposes a novel method of solving CFD problems by applying a neural network super-resolution to lower resolution CFD simulations.


### OpenFOAM

CFD data was gathered from simulations run in the OpenFOAM software platform. The data used in this project comes from the dambreak
tutorial, which was modified to have uniform point density as well as randomized fluid properties. Each 
