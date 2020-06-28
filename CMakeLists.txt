cmake_minimum_required(VERSION 2.8.3)
project(aws_robomaker_hospital_world)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
)

catkin_package()

install(DIRECTORY launch models worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
