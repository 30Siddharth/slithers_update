from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='slithers_update_ros',
            executable='controller',
            name='slithers_controller',
            output='screen',
            parameters=['config/controller_params.yaml'],
        ),
    ])
