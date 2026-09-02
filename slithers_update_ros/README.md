# slithers_update_ros

A ROS 2 Jazzy `ament_python` package scaffold for integrating the `slithers_update` kinematics, Lie-theory, controller, and CoppeliaSim workflows with ROS 2.

## Build

Place this repository in a ROS 2 workspace `src/` directory, then run:

```bash
source /opt/ros/jazzy/setup.bash
cd <workspace>
colcon build --packages-select slithers_update_ros
source install/setup.bash
```

## Run

```bash
ros2 launch slithers_update_ros slithers_controller.launch.py
```

The initial node subscribes to `/joint_states`. Its controller implementation, command publisher, robot-specific interfaces, and CoppeliaSim bridge are intentionally deferred to later migration commits.
