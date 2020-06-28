# AWS RoboMaker Hospital World ROS package

**Visit the [AWS RoboMaker website](https://aws.amazon.com/robomaker/) to learn more about building intelligent robotic applications with Amazon Web Services.**

# Include the world from another package

* Update .rosinstall to clone this repository and run `rosws update`
```
- git: {local-name: src/aws-robomaker-hospital-world, uri: 'https://github.com/aws-robotics/aws-robomaker-hospital-world.git', version: master}
```
* Add the following to your launch file:
```xml
<launch>
  <!-- Launch World -->
  <include file="$(find aws_robomaker_hospital_world)/launch/hospital.launch"/>
  ...
</launch>
```

# Load directly into Gazebo (without ROS)
```bash
chmod +x setup.sh
./setup.sh
export GAZEBO_MODEL_PATH=`pwd`/models:`pwd`/fuel_models
gazebo worlds/hospital.world
```

# ROS Launch with Gazebo viewer (without a robot)
```bash
# build for ROS
rosdep install --from-paths . --ignore-src -r -y
colcon build

# run in ROS
source install/setup.sh
roslaunch aws_robomaker_hospital_world view_hospital.launch
```

# Building
Include this as a .rosinstall dependency in your SampleApplication simulation workspace. `colcon build` will build this repository.

To build it outside an application, note there is no robot workspace. It is a simulation workspace only.

```bash
$ rosws update
$ rosdep install --from-paths . --ignore-src -r -y
$ chmod +x setup.sh
$ ./setup.sh
$ colcon build
```

