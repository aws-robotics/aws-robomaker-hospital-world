# AWS RoboMaker Hospital World ROS package

**Visit the [AWS RoboMaker website](https://aws.amazon.com/robomaker/) to learn more about building intelligent robotic applications with Amazon Web Services.**

![Model: Buckets](docs/images/hospital_world.png)

## 3D Models included in this Gazebo World

| Model (/models)       | Picture           |
| :------------- |:-------------:|
| **aws_robomaker_hospital_elevator_01_car, aws_robomaker_hospital_elevator_01_door, aws_robomaker_hospital_elevator_01_portal**     | ![Model: Elevator](docs/images/elevator.png) |
| **aws_robomaker_hospital_curtain_closed_01, aws_robomaker_hospital_curtain_half_open_01, aws_robomaker_hospital_curtain_open_01**     | ![Model: Curtains](docs/images/curtains.png) |
| **aws_robomaker_hospital_nursesstation_01**    | ![Model: Nurses Station](docs/images/nurses_station.png)
| **aws_robomaker_hospital_hospitalsign_01**    | ![Model: Hospital Sign](docs/images/hospital_sign.png)
| **aws_robomaker_hospital_floor_01_floor**    | ![Model: Hospital Floor](docs/images/hospital_floor.png)
| **aws_robomaker_hospital_floor_01_walls**    | ![Model: Hospital Walls and Layout](docs/images/hospital_walls.png)
| **aws_robomaker_hospital_floor_01_ceiling**    | ![Model: Ceiling](docs/images/hospital_ceiling.png)

We also reference the following models from https://app.ignitionrobotics.org/fuel/models:

*MopCart3, AdjTable, BedTable, FemaleVisitorSit, VisitorKidSit, ElderMalePatient, OfficeChairBlack, ElderLadyPatient, MaleVisitorSit, FemaleVisitor, BedsideTable, SurgicalTrolleyMed, AnesthesiaMachine, VendingMachine, TrolleyBox2, TrolleyBox1, Toilet, Shower, PatientFSit, Nurse, MaleVisitorOnPhone, MalePatientBed, KitchenSink, Male visitor, HOSPI, WhiteChipChair, WalkingCane, Walker, VisitorChair, TrolleyBedPatient, SurgicalTrolleyGuards, SurgicalTrolley, StorageRackCovered, StorageRackCoverOpen, StorageRack, SmallTrolley, RollingWalker, PotatoChipChair, PatientWheelChair, ParkingTrolleyMin, ParkingTrolleyMax, OrangeDoors, OpScrubs, MetalCabinetYellow, MetalCabinet, ManualFireAlarmButton, MainTable, InstrumentCart2, InstrumentCart1, HospitalPillow, Handrail, GarbagePileV2, GarbagePileV1, FreezerCondenser, FreezerComp, Extinguisher cabinet, ExitSign, ElectronicsRecycling, ColBumper, CGMClassic, BedsideTable2, TrolleyBed*

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

