import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory('sura_mapping')

    map_file = os.path.join(
        pkg_share,
        'maps',
        'puerto_castellon',
        'occupancy.yaml'
    )

    params_file = os.path.join(
        pkg_share,
        'config',
        'map_server.yaml'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'map',
            default_value=map_file,
            description='Path to the occupancy map YAML file'
        ),

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            namespace='blueboat',
            output='screen',
            parameters=[
                params_file,
                {'yaml_filename': LaunchConfiguration('map')}
            ]
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_mapping',
            namespace='blueboat',
            output='screen',
            parameters=[{
                'autostart': True,
                'node_names': ['map_server']
            }]
        )
    ])