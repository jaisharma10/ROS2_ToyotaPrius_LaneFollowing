# Lane Following Simulation of a Toyota Prius 

**Goal -->** The goal of this project is to simulate a Lane Detection and Lane Following Toyota Prius in a Gazebo environment. All programs are written, tested and simulated using ROS 2 - Foxy Fitzroy.

<p align="center">
  <img src = "Images/img5.png" width = "400" >
</p>

## System Requirements
- Ubuntu 20.04
- ROS2 Foxy

## RQT Graph

<p align="center">
  <img src = "Images/nodeGraph.png" width = "600" >
</p>

## Perception Pipeline

Lane Detection and Lane Following:
- Perform Image Segmentation
- Perform CannyEdge Method
- Compare Lane center to Camera Frame center
- Calculate Orientation Error
- Correct Path by publishing updated velocities

## Images

<p align="center">
  <img src = "Images/img1.png" width = "500" >
  <img src = "Images/img2.png" width = "500" >
  <img src = "Images/img3.png" width = "500" >
  <img src = "Images/img4.png" width = "500" >
  <img src = "Images/img6.png" width = "500" >
  <img src = "Images/img7.png" width = "500" >
</p>

## Results

The final result can be found in this [Video Link](https://drive.google.com/file/d/13d53jG-qHz8MxfdAAgOHgRX02tFpSac2/view?usp=sharing) 

<p align="center">
  <img src = "Images/priusTake1_AdobeExpress.gif" width = "300" >
</p>

## Acknowledgements

 - Inspired by work done in this [Github Repo](https://github.com/noshluk2/ROS2-Ultimate-Mobile-Robotics-Course-for-Beginners-OpenCV)
 - [Gazebo Models](https://github.com/osrf/gazebo_models)
 - ROS 2 Foxy Fitzroy - [Tutorials](https://docs.ros.org/en/foxy/Tutorials.html)

## Support
For any questions, email me at jaisharm@umd.edu
