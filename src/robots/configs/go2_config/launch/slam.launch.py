from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    this_package = FindPackageShare("go2_config")

    default_slam_params_file_path = PathJoinSubstitution(
        [this_package, "config", "autonomy", "slam.yaml"]
    )
    default_rtabmap_nav2_params_file_path = PathJoinSubstitution(
        [this_package, "config", "autonomy", "rtabmap_navigation.yaml"]
    )
    default_rviz_config_path = PathJoinSubstitution(
        [this_package, "rviz", "rtabmap_sim.rviz"]
    )
    default_rtabmap_database_path = [
        EnvironmentVariable("HOME"),
        "/.ros/go2_rtabmap_sim.db",
    ]

    champ_slam_launch_path = PathJoinSubstitution(
        [FindPackageShare("champ_navigation"), "launch", "slam.launch.py"]
    )
    nav2_launch_path = PathJoinSubstitution(
        [FindPackageShare("nav2_bringup"), "launch", "navigation_launch.py"]
    )
    rtabmap_launch_path = PathJoinSubstitution(
        [FindPackageShare("rtabmap_launch"), "launch", "rtabmap.launch.py"]
    )

    slam_toolbox_condition = IfCondition(
        PythonExpression(
            ["'", LaunchConfiguration("slam_backend"), "' == 'slam_toolbox'"]
        )
    )
    rtabmap_condition = IfCondition(
        PythonExpression(["'", LaunchConfiguration("slam_backend"), "' == 'rtabmap'"])
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="slam_backend",
                default_value="slam_toolbox",
                description="SLAM backend to use: slam_toolbox or rtabmap",
            ),
            DeclareLaunchArgument(
                name="slam_params_file",
                default_value=default_slam_params_file_path,
                description="slam_toolbox parameter file",
            ),
            DeclareLaunchArgument(
                name="rtabmap_nav2_params_file",
                default_value=default_rtabmap_nav2_params_file_path,
                description="Nav2 parameter file used when slam_backend=rtabmap",
            ),
            DeclareLaunchArgument(
                name="rtabmap_database_path",
                default_value=default_rtabmap_database_path,
                description="RTAB-Map database path",
            ),
            DeclareLaunchArgument(
                name="rviz_cfg",
                default_value=default_rviz_config_path,
                description="RViz configuration used when slam_backend=rtabmap",
            ),
            DeclareLaunchArgument(
                name="delete_rtabmap_db_on_start",
                default_value="false",
                description="Delete the RTAB-Map database before starting",
            ),
            DeclareLaunchArgument(
                name="rtabmap_viz",
                default_value="false",
                description="Launch rtabmap_viz when slam_backend=rtabmap",
            ),
            DeclareLaunchArgument(
                name="assemble_cloud_map",
                default_value="true",
                description="Launch rtabmap map_assembler to publish /cloud_map",
            ),
            DeclareLaunchArgument(
                name="sim",
                default_value="false",
                description="Enable use_sim_time",
            ),
            DeclareLaunchArgument(
                name="rviz",
                default_value="false",
                description="Run rviz",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(champ_slam_launch_path),
                condition=slam_toolbox_condition,
                launch_arguments={
                    "slam_params_file": LaunchConfiguration("slam_params_file"),
                    "sim": LaunchConfiguration("sim"),
                    "rviz": LaunchConfiguration("rviz"),
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(nav2_launch_path),
                condition=rtabmap_condition,
                launch_arguments={
                    "use_sim_time": LaunchConfiguration("sim"),
                    "params_file": LaunchConfiguration("rtabmap_nav2_params_file"),
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(rtabmap_launch_path),
                condition=rtabmap_condition,
                launch_arguments={
                    "namespace": "",
                    "use_sim_time": LaunchConfiguration("sim"),
                    "localization": "false",
                    "rviz": LaunchConfiguration("rviz"),
                    "rviz_cfg": LaunchConfiguration("rviz_cfg"),
                    "rtabmap_viz": LaunchConfiguration("rtabmap_viz"),
                    "depth": "false",
                    "subscribe_rgb": "false",
                    "subscribe_rgbd": "false",
                    "approx_sync": "true",
                    "frame_id": "base_footprint",
                    "map_frame_id": "map",
                    "database_path": LaunchConfiguration("rtabmap_database_path"),
                    "publish_tf_map": "true",
                    "odom_topic": "/odom",
                    "publish_tf_odom": "false",
                    "imu_topic": "/imu/data",
                    "wait_imu_to_init": "false",
                    "subscribe_scan": "false",
                    "subscribe_scan_cloud": "true",
                    "scan_cloud_topic": "/livox_points",
                    "visual_odometry": "false",
                    "icp_odometry": "false",
                    "args": PythonExpression(
                        [
                            "'-d' if '",
                            LaunchConfiguration("delete_rtabmap_db_on_start"),
                            "' == 'true' else ''",
                        ]
                    ),
                }.items(),
            ),
            Node(
                package="rtabmap_util",
                executable="map_assembler",
                name="map_assembler",
                output="screen",
                condition=IfCondition(LaunchConfiguration("assemble_cloud_map")),
                parameters=[
                    {
                        "use_sim_time": LaunchConfiguration("sim"),
                        "rtabmap": "rtabmap",
                        "regenerate_local_grids": False,
                        "cloud_output_voxelized": True,
                    }
                ],
            ),
        ]
    )
