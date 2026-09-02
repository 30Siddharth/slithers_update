# slithers_update_ros

A ROS 2 Jazzy `ament_python` package scaffold for integrating the `slithers_update` control workflow with Gazebo or MuJoCo through a simulator-neutral ROS interface.

## Build

Place this repository in a ROS 2 workspace `src/` directory, then run:

```bash
source /opt/ros/jazzy/setup.bash
cd <workspace>
colcon build --packages-select slithers_update_ros
source install/setup.bash
```

## Run the controller

Gazebo profile:

```bash
ros2 launch slithers_update_ros slithers_controller.launch.py \
  simulator:=gazebo \
  config_file:=$(ros2 pkg prefix slithers_update_ros)/share/slithers_update_ros/config/gazebo_params.yaml
```

MuJoCo profile:

```bash
ros2 launch slithers_update_ros slithers_controller.launch.py \
  simulator:=mujoco \
  config_file:=$(ros2 pkg prefix slithers_update_ros)/share/slithers_update_ros/config/mujoco_params.yaml
```

The initial controller subscribes to `JointState` and publishes safe, rate-limited position-hold `JointTrajectory` commands after receiving a complete configured state. See `SIMULATOR_INTERFACE.md` for the required topic, joint-order, units, frame, and integration contract.

## Validation

```bash
colcon test --packages-select slithers_update_ros
colcon test-result --verbose
```

The package is simulator-neutral; Gazebo and MuJoCo launch/physics assets remain separate integration work. The repository's current URDF files under `robot_models/UR/urdf/` are the recommended shared robot-description starting point.
