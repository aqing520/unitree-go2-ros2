# RTAB-Map Stack Layout

This directory groups the RTAB-Map ROS integration packages that are built as
part of the outer `unitree-go2-ros2` workspace.

## Included packages

- `rtabmap_ros/`
- `robot_localization/`
- `rtabmap_stack_env/` (environment hook package, not an algorithm package)

## Excluded from this source group

- Real hardware lidar/driver packages such as `livox_ros_driver2`
- The RTAB-Map core C++ source tree

## Prebuilt RTAB-Map core

The RTAB-Map core library is reused from the vendor install at:

`vendor/rtabmap_stack/rtabmap-0.23.4/install`

This is the prebuilt C++ core/runtime install used by the ROS packages in this
workspace. It is not a ROS source package tree.

Use the outer workspace helper script to build against it:

```bash
bash scripts/build_workspace_with_rtabmap.sh
```

## Legacy migration workspace

The old nested `src/rtabmap_nav2_stack` workspace has been removed from `src/`.
Historical notes and the demo bag were archived under:

`archive/rtabmap_nav2_stack_legacy`
