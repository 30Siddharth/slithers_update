"""Simulator-neutral ROS 2 joint-trajectory controller scaffold."""

from __future__ import annotations

from typing import Dict, List, Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


DEFAULT_JOINT_NAMES = [
    'shoulder_pan_joint',
    'shoulder_lift_joint',
    'elbow_joint',
    'wrist_1_joint',
    'wrist_2_joint',
    'wrist_3_joint',
]


class SlithersController(Node):
    """Publish conservative position-hold commands from validated joint state."""

    def __init__(self) -> None:
        super().__init__('slithers_controller')
        self.declare_parameter('simulator', 'gazebo')
        self.declare_parameter('joint_state_topic', '/joint_states')
        self.declare_parameter(
            'command_topic',
            '/joint_trajectory_controller/joint_trajectory',
        )
        self.declare_parameter('joint_names', DEFAULT_JOINT_NAMES)
        self.declare_parameter('control_rate_hz', 100.0)
        self.declare_parameter('command_duration_s', 0.02)

        self.simulator = str(self.get_parameter('simulator').value)
        if self.simulator not in {'gazebo', 'mujoco'}:
            raise ValueError("The 'simulator' parameter must be 'gazebo' or 'mujoco'.")

        self.joint_names = list(self.get_parameter('joint_names').value)
        if not self.joint_names or len(set(self.joint_names)) != len(self.joint_names):
            raise ValueError('joint_names must be a non-empty list of unique names.')

        self.command_duration_s = float(
            self.get_parameter('command_duration_s').value
        )
        if self.command_duration_s <= 0.0:
            raise ValueError('command_duration_s must be positive.')

        control_rate_hz = float(self.get_parameter('control_rate_hz').value)
        if control_rate_hz <= 0.0:
            raise ValueError('control_rate_hz must be positive.')

        joint_state_topic = str(self.get_parameter('joint_state_topic').value)
        command_topic = str(self.get_parameter('command_topic').value)
        self._latest_positions: Optional[List[float]] = None

        self.create_subscription(
            JointState, joint_state_topic, self._joint_state_callback, 10
        )
        self._command_publisher = self.create_publisher(
            JointTrajectory, command_topic, 10
        )
        self.create_timer(1.0 / control_rate_hz, self._control_callback)
        self.get_logger().info(
            f'Started {self.simulator} interface: state={joint_state_topic}, '
            f'command={command_topic}'
        )

    def _joint_state_callback(self, message: JointState) -> None:
        """Cache a complete, ordered joint position vector when available."""
        positions = self._ordered_positions(message)
        if positions is not None:
            self._latest_positions = positions

    def _ordered_positions(self, message: JointState) -> Optional[List[float]]:
        """Return positions in configured order or None for incomplete state input."""
        if len(message.name) != len(message.position):
            self.get_logger().warning(
                'Ignoring JointState with different name and position lengths.'
            )
            return None
        position_by_name: Dict[str, float] = dict(zip(message.name, message.position))
        missing = [name for name in self.joint_names if name not in position_by_name]
        if missing:
            self.get_logger().debug(f'Waiting for configured joints: {missing}')
            return None
        return [float(position_by_name[name]) for name in self.joint_names]

    def _control_callback(self) -> None:
        """Publish the safe initial behavior: hold the last complete joint state."""
        if self._latest_positions is None:
            return
        command = JointTrajectory()
        command.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = self._latest_positions
        point.time_from_start.sec = int(self.command_duration_s)
        point.time_from_start.nanosec = int(
            (self.command_duration_s % 1.0) * 1_000_000_000
        )
        command.points = [point]
        self._command_publisher.publish(command)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SlithersController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
