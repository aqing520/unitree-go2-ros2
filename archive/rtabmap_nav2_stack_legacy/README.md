# RTAB-Map Legacy Archive

This directory preserves reference material from the old
`src/rtabmap_nav2_stack` migration workspace.

## What is kept here

- Legacy markdown notes and setup documents under `docs/`
- The demo mapping bag metadata under `bags/demo_mapping_bag/`
- The local `demo_mapping.db3` data file if present on the machine

## What is not kept here

- Old build/install/log outputs
- Old nested workspace scripts and wrapper build entrypoints
- Old duplicated source trees such as `livox_ros_driver2`
- The old embedded RTAB-Map core source tree

## Current supported workflow

- Build: `bash scripts/build_workspace_with_rtabmap.sh`
- Runtime: `source install/setup.bash`
- RTAB-Map core: `vendor/rtabmap_stack/rtabmap-0.23.4/install`
