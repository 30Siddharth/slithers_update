"""Initial ROS 2 node for slithers_update control integration."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class SlithersController(Node):
    """Subscribe to joint state and provide a safe extension point for control."""

    def __init__(self) -> None:
        super().__init__('slithers_controller')
        self.declare_parameter('joint_state_topic', '/joint_states')
        joint_state_topic = self.get_parameter('joint_state_topic').value
        self.create_subscription(JointState, joint_state_topic, self._joint_state_callback, 10)
        self.get_logger().info(f'Slithers controller listening on {joint_state_topic}')

    def _joint_state_callback(self, message: JointState) -> None:
        """Receive state; controller and command publication are added in later milestones."""
        del message


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
