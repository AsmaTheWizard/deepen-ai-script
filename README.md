# deepen-ai-script

The project goal is to extract GPS data from Labels (generated from LiDar files), run a simulation and control a car using PID controller. We built on the work of Jeremey [here](https://github.com/JeremyBYU/airsimgeo)

##### The project diveded into 3 main parts:

1- Unreal Engine and Airsim
2- Cesium Plugin
3- This repo(Python project) where you can extrat GPS, and run a PID controller.

## Installation

### Unreal Engine and Airsim

The engine we use is [Unreal Engine](https://www.unrealengine.com/en-US) version 4.27, and we use [Airsim](https://microsoft.github.io/AirSim/), which is an open-source simulator project from Microsoft for drones and cars.

##### Install Airsim

follow this instruction till "Build Unreal Project" section [Download and Install Airsim](https://microsoft.github.io/AirSim/build_windows/).By end of "Build Unreal Project" section, you will have both Unreal Engine and Airsim installed in your system.

### Cesium

[Cesium](https://cesium.com/platform/cesium-for-unreal/) is an open-source visualization plugin. We use it to provide the globe 3D represenation and GPS data.

##### Install Cesium

To install cesium, follow [this link](https://cesium.com/learn/unreal/unreal-quickstart/) but instead of creating a new project, you should open the Airsim project and go to this path to install Cesium there

```
\AirSim\Unreal\Environments\Blocks
```

### Deepen AI script project

This project has two main functionality, First extract GPS data, and Second is to build the PID controller to control the car.

##### Install Deepen AI script

Clone the porject and install libs in requirement.txt file, if you use Windows, you will face issue installing pyproj, to solve this issue follow [the instruction here](https://stackoverflow.com/a/71346374).

## Running the project

Open the AirSim Unreal Project in following folder

```
\AirSim\Unreal\Environments\Blocks
```

You should have an internet connection, otherwise Cesium won't be able to load 3D map.

If you have an internet connection and followed all instructions above, your sceen should be like below image(except the middle screen ofcourse)

![](</img/Screenshot%20(4).png>)

Then, go to CesiumGeoRefrence, and enter Lat and Lon as shown below, make sure that the height is on the ground, otherwise the car will act weirdly.
![](</img/Screenshot%20(5).png>)

Hit Play button from the top menu.
![](</img/Screenshot%20(6).png>)

Run the PID.py file in a terminal, the car will move.

![](/img/result.png)
