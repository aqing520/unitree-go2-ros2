#!/bin/bash

set -euo pipefail

REMOTE_TARGET="${1:-wheeltec@192.168.110.198:/home/wheeltec/unitree-go2-ros2/src/stacks/rtabmap_stack/rtabmap_ros/rtsp_camera_bridge/}"

rsync -r . "$REMOTE_TARGET"

echo "rsync done"
