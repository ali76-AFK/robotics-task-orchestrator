from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    is_sim = LaunchConfiguration("is_sim")

    command_interface_node = Node(
        package="arduinobot_remote",
        executable="command_interface.py",
        output="screen",
        parameters=[{"use_sim_time": is_sim}],
    )

    vision_bridge_node = Node(
        package="arduinobot_remote",
        executable="vision_bridge.py",
        output="screen",
        parameters=[{"use_sim_time": is_sim}],
    )

    vla_policy_node = Node(
        package="arduinobot_remote",
        executable="vla_policy.py",
        output="screen",
        parameters=[{"use_sim_time": is_sim}],
    )

    execution_bridge_node = Node(
        package="arduinobot_remote",
        executable="execution_bridge.py",
        output="screen",
        parameters=[{"use_sim_time": is_sim}],
    )

    return LaunchDescription([
        is_sim_arg,
        command_interface_node,
        vision_bridge_node,
        vla_policy_node,
        execution_bridge_node,
    ])
