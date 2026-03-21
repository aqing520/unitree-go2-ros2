from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    this_package = FindPackageShare("go2_config")

    gazebo_launch_path = PathJoinSubstitution([this_package, "launch", "gazebo_livox.launch.py"])
    slam_launch_path = PathJoinSubstitution([this_package, "launch", "slam.launch.py"])
    default_world_path = PathJoinSubstitution([this_package, "worlds", "outdoor.world"])
    default_rtabmap_database_path = [
        EnvironmentVariable("HOME"),
        "/.ros/go2_rtabmap_sim.db",
    ]

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="world",
                default_value=default_world_path,
                description="Gazebo world path",
            ),
            DeclareLaunchArgument(
                name="gui",
                default_value="true",
                description="Launch Gazebo GUI",
            ),
            DeclareLaunchArgument(
                name="rviz",
                default_value="true",
                description="Run rviz",
            ),
            DeclareLaunchArgument(
                name="rtabmap_viz",
                default_value="false",
                description="Run rtabmap_viz",
            ),
            DeclareLaunchArgument(
                name="rtabmap_database_path",
                default_value=default_rtabmap_database_path,
                description="RTAB-Map database path",
            ),
            DeclareLaunchArgument(
                name="delete_rtabmap_db_on_start",
                default_value="true",
                description="Delete the RTAB-Map database before starting a new mapping session",
            ),
            GroupAction(
                scoped=True,
                actions=[
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(gazebo_launch_path),
                        launch_arguments={
                            "use_sim_time": "true",
                            "rviz": "false",
                            "world": LaunchConfiguration("world"),
                            "gui": LaunchConfiguration("gui"),
                        }.items(),
                    )
                ],
            ),
            GroupAction(
                scoped=True,
                actions=[
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(slam_launch_path),
                        launch_arguments={
                            "slam_backend": "rtabmap",
                            "sim": "true",
                            "rviz": LaunchConfiguration("rviz"),
                            "rtabmap_viz": LaunchConfiguration("rtabmap_viz"),
                            "rtabmap_database_path": LaunchConfiguration("rtabmap_database_path"),
                            "delete_rtabmap_db_on_start": LaunchConfiguration(
                                "delete_rtabmap_db_on_start"
                            ),
                        }.items(),
                    )
                ],
            ),
        ]
    )
