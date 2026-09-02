from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    simulator = LaunchConfiguration('simulator')
    config_file = LaunchConfiguration('config_file')
    return LaunchDescription([
        DeclareLaunchArgument('simulator', default_value='gazebo'),
        DeclareLaunchArgument(
            'config_file',
            default_value='config/gazebo_params.yaml',
            description='Package-relative controller parameter file.',
        ),
        Node(
            package='slithers_update_ros',
            executable='controller',
            name='slithers_controller',
            output='screen',
            parameters=[config_file, {'simulator': simulator}],
        ),
    ])
