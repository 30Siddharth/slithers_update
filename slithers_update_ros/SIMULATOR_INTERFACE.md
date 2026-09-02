# Simulator interface contract

`slithers_update_ros` keeps its controller independent of the physics back end. Select `simulator:=gazebo` or `simulator:=mujoco`; both back ends must expose the same ROS-facing contract.

## Required inputs and outputs

- State input: `sensor_msgs/msg/JointState` on `joint_state_topic`, default `/joint_states`.
- Command output: `trajectory_msgs/msg/JointTrajectory` on `command_topic`, default `/joint_trajectory_controller/joint_trajectory`.
- Joint order: exactly the order configured in `joint_names`; the controller maps incoming joint states by name before publishing.
- Units: radians, radians/s, radians/s^2, meters, seconds, and SI inertial quantities.
- Frame convention: ROS REP-103 right-handed frames. Frame IDs and TF publication remain the responsibility of the robot/simulator description.

## Gazebo

Use an URDF/Xacro-based description and a `ros2_control` configuration with a trajectory controller whose command topic matches `command_topic`. The existing URDF sources are in `../robot_models/UR/urdf/`. A complete Gazebo deployment still requires transmissions, hardware/simulator plugins, inertial/collision validation, and a world/launch integration appropriate to the chosen Gazebo distribution.

## MuJoCo

Convert or maintain the selected URDF as an MJCF model, resolving mesh paths and defining actuators that accept the configured command interface. Use a ROS 2 bridge or MuJoCo integration that publishes `JointState` and consumes a `JointTrajectory` compatible command stream, or adapt its native control topic to this contract. The controller itself does not import MuJoCo and can therefore be tested independently of the simulator.

## Conservative baseline

Until model-based control is implemented, the controller publishes a position hold only after it receives a complete joint state for every configured joint. It neither synthesizes a trajectory nor issues a command while state is incomplete.
